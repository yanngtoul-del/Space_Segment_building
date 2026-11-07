"""CONOPS time-series simulation: modes, battery state of charge, memory buffer, ground contact."""

import math
from dataclasses import dataclass, field
from enum import Enum
from ssb.core.orbit import OrbitDefinition
from ssb.orbit.propagator import OrbitStatePoint, OrbitPropagator
from ssb.orbit.station_access import GroundStationPass, StationAccessCalculator
from ssb.system.evaluator import SystemBudgets


class OperationalMode(str, Enum):
    LEOP = "leop"
    NOMINAL_STANDBY = "nominal_standby"
    ACQUISITION = "acquisition"
    DOWNLINK = "downlink"
    ORBIT_MANEUVER = "orbit_maneuver"
    SAFE = "safe"


@dataclass
class ConopsStepLog:
    time_s: float
    mode: OperationalMode
    in_eclipse: bool
    battery_soc_pct: float
    memory_used_gb: float
    cumulative_downlinked_gb: float
    active_station_id: str | None = None


@dataclass
class ConopsSimulationReport:
    duration_days: float
    min_battery_soc_pct: float
    max_memory_used_gb: float
    total_data_acquired_gb: float
    total_data_downlinked_gb: float
    data_loss_overflow_gb: float
    time_series: list[ConopsStepLog] = field(default_factory=list)


class ConopsSimulator:
    """Simulates dynamic satellite operations over multi-orbit timelines."""

    @classmethod
    def simulate(
        cls,
        budgets: SystemBudgets,
        orbit: OrbitDefinition,
        ground_track: list[OrbitStatePoint],
        passes: list[GroundStationPass],
        imaging_duty_cycle_sunlit_pct: float = 20.0,
    ) -> ConopsSimulationReport:
        plat = budgets.configured_platform.base

        # Battery parameters:
        batt_cap_wh = plat.battery_capacity_wh
        soc_wh = batt_cap_wh  # Start fully charged

        # Storage capacity (find from options or use base)
        mem_cap_gb = 512.0
        for opt in budgets.configured_platform.resolved_options:
            if opt.equipment.function.value == "mass_memory":
                mem_cap_gb = opt.equipment.specs.get("capacity_bol_gb", 512.0)

        # Downlink rate from payload downlink transmitter
        downlink_rate_gbps = 0.5  # default 500 Mbps = ~0.0625 GB/s
        for opt in budgets.configured_platform.resolved_options:
            if opt.equipment.function.value == "payload_downlink":
                downlink_rate_gbps = (opt.equipment.specs.get("max_data_rate_mbps", 500.0) / 8.0) / 1000.0

        # Acquisition rate
        acq_rate_gbps = 0.1  # default 800 Mbps = 0.1 GB/s
        if budgets.payload_performances:
            first_perf = next(iter(budgets.payload_performances.values()))
            if hasattr(first_perf, "data_rate_compressed_mbps"):
                acq_rate_gbps = (first_perf.data_rate_compressed_mbps / 8.0) / 1000.0

        # Power numbers:
        p_gen_sunlit_w = plat.orbit_avg_power_w * 1.5  # solar array peak in sun
        p_base_bus_w = plat.dry_mass_kg * 0.4  # base platform avionics
        p_acq_extra_w = sum(p.operational_power_w for p in budgets.configured_platform.base.dry_mass_kg and [])
        p_dl_extra_w = 40.0

        current_mem_gb = 0.0
        total_acq_gb = 0.0
        total_dl_gb = 0.0
        overflow_gb = 0.0
        min_soc_pct = 100.0
        max_mem_gb = 0.0

        logs: list[ConopsStepLog] = []

        # Build lookup for station pass intervals:
        pass_intervals: list[tuple[float, float, str]] = [
            (p.start_time_s, p.end_time_s, p.station_id) for p in passes
        ]

        for i in range(len(ground_track) - 1):
            pt = ground_track[i]
            dt_s = ground_track[i + 1].time_s - pt.time_s
            dt_hours = dt_s / 3600.0

            # Determine operational mode:
            # 1. Is there an active ground station pass?
            active_sta = None
            for p_start, p_end, sta_id in pass_intervals:
                if p_start <= pt.time_s <= p_end:
                    active_sta = sta_id
                    break

            if active_sta and current_mem_gb > 0:
                mode = OperationalMode.DOWNLINK
            elif not pt.in_eclipse and (i % int(100.0 / imaging_duty_cycle_sunlit_pct) == 0):
                mode = OperationalMode.ACQUISITION
            else:
                mode = OperationalMode.NOMINAL_STANDBY

            # Data state update
            if mode == OperationalMode.ACQUISITION:
                data_in = acq_rate_gbps * dt_s
                total_acq_gb += data_in
                if current_mem_gb + data_in > mem_cap_gb:
                    overflow_gb += (current_mem_gb + data_in - mem_cap_gb)
                    current_mem_gb = mem_cap_gb
                else:
                    current_mem_gb += data_in

            elif mode == OperationalMode.DOWNLINK:
                data_out = downlink_rate_gbps * dt_s
                actual_out = min(current_mem_gb, data_out)
                current_mem_gb -= actual_out
                total_dl_gb += actual_out

            if current_mem_gb > max_mem_gb:
                max_mem_gb = current_mem_gb

            # Power state update
            p_gen = 0.0 if pt.in_eclipse else p_gen_sunlit_w
            p_cons = p_base_bus_w
            if mode == OperationalMode.ACQUISITION:
                p_cons += p_acq_extra_w
            elif mode == OperationalMode.DOWNLINK:
                p_cons += p_dl_extra_w

            p_net = p_gen - p_cons
            soc_wh = max(0.0, min(batt_cap_wh, soc_wh + (p_net * dt_hours)))
            soc_pct = (soc_wh / batt_cap_wh) * 100.0
            if soc_pct < min_soc_pct:
                min_soc_pct = soc_pct

            logs.append(
                ConopsStepLog(
                    time_s=pt.time_s,
                    mode=mode,
                    in_eclipse=pt.in_eclipse,
                    battery_soc_pct=round(soc_pct, 1),
                    memory_used_gb=round(current_mem_gb, 2),
                    cumulative_downlinked_gb=round(total_dl_gb, 2),
                    active_station_id=active_sta,
                )
            )

        total_days = ground_track[-1].time_s / 86400.0
        return ConopsSimulationReport(
            duration_days=round(total_days, 3),
            min_battery_soc_pct=round(min_soc_pct, 1),
            max_memory_used_gb=round(max_mem_gb, 2),
            total_data_acquired_gb=round(total_acq_gb, 2),
            total_data_downlinked_gb=round(total_dl_gb, 2),
            data_loss_overflow_gb=round(overflow_gb, 2),
            time_series=logs,
        )
