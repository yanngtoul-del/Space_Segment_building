"""Overall system budget calculations and rule verification."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from ssb.core.orbit import OrbitDefinition
from ssb.core.project import SystemConfiguration, Launcher
from ssb.core.mission import MissionSpecification, RequirementOperator
from ssb.core.payload import BasePayload, OpticalImagerPayload, PayloadType
from ssb.catalog.database import CatalogDatabase
from ssb.system.configurator import PlatformConfigurator, ConfiguredPlatform
from ssb.payload.optical_model import OpticalImagerModel, OpticalImagerPerformance


class CheckStatus(str, Enum):
    PASS = "pass"
    WARNING = "warning"
    FAIL = "fail"


@dataclass
class RuleCheckResult:
    rule_id: str
    category: str
    status: CheckStatus
    message: str
    current_value: float | str | None = None
    target_value: float | str | None = None
    unit: str = ""


@dataclass
class MassBudget:
    platform_dry_kg: float
    options_mass_kg: float
    payloads_mass_kg: float
    system_dry_mass_kg: float
    propellant_mass_kg: float
    system_wet_mass_kg: float
    margin_pct: float
    launch_mass_with_margin_kg: float
    platform_capacity_kg: float


@dataclass
class PowerBudget:
    platform_avg_power_w: float
    options_avg_power_w: float
    payloads_avg_power_w: float
    total_avg_consumption_w: float
    platform_generation_w: float
    power_margin_w: float
    power_margin_pct: float
    peak_consumption_w: float


@dataclass
class CostBudget:
    platform_base_meur: float
    options_total_meur: float
    payloads_total_meur: float
    launcher_meur: float
    space_segment_total_meur: float
    mission_budget_limit_meur: float
    cost_margin_meur: float


@dataclass
class SystemBudgets:
    configured_platform: ConfiguredPlatform
    mass: MassBudget
    power: PowerBudget
    cost: CostBudget
    payload_performances: dict[str, Any] = field(default_factory=dict)
    rule_checks: list[RuleCheckResult] = field(default_factory=list)
    compliance_checks: list[RuleCheckResult] = field(default_factory=list)

    @property
    def has_blocking_errors(self) -> bool:
        return any(
            c.status == CheckStatus.FAIL
            for c in (self.rule_checks + self.compliance_checks)
        )


class SystemEvaluator:
    """Evaluates the complete satellite architecture against physics, platform limits, and mission specs."""

    def __init__(self, catalog: CatalogDatabase) -> None:
        self.catalog = catalog
        self.configurator = PlatformConfigurator(catalog)

    def evaluate(
        self, config: SystemConfiguration, mission: MissionSpecification
    ) -> SystemBudgets:
        rule_checks: list[RuleCheckResult] = []
        compliance_checks: list[RuleCheckResult] = []

        if not config.platform_id or config.platform_id not in self.catalog.platforms:
            raise ValueError("No valid platform selected in configuration")

        conf_plat = self.configurator.configure(
            config.platform_id, config.selected_options
        )
        for err in conf_plat.validation_errors:
            rule_checks.append(
                RuleCheckResult(
                    rule_id="RULE_PLAT_CONFIG",
                    category="Platform Configuration",
                    status=CheckStatus.FAIL,
                    message=err,
                )
            )

        plat_base = conf_plat.base

        # Resolve selected payloads
        payloads: list[BasePayload] = []
        for pid in config.selected_payload_ids:
            if pid in self.catalog.payloads:
                payloads.append(self.catalog.payloads[pid])
            else:
                rule_checks.append(
                    RuleCheckResult(
                        rule_id="RULE_PAYLOAD_MISSING",
                        category="Payload",
                        status=CheckStatus.FAIL,
                        message=f"Selected payload '{pid}' not found in catalog",
                    )
                )

        # 1. Mass Budget
        pl_mass = sum(p.mass_kg for p in payloads)
        opt_mass = sum(opt.final_mass_kg for opt in conf_plat.resolved_options)

        # Look for propellant in options
        prop_mass = 0.0
        for opt in conf_plat.resolved_options:
            if opt.equipment.function.value == "propulsion":
                prop_mass += opt.equipment.specs.get("propellant_mass_kg", 0.0)

        sys_dry_kg = plat_base.dry_mass_kg + opt_mass + pl_mass
        wet_mass_kg = sys_dry_kg + prop_mass
        margin_pct = 20.0  # standard phase A/B margin
        launch_mass_with_margin_kg = wet_mass_kg * (1.0 + margin_pct / 100.0)

        mass_b = MassBudget(
            platform_dry_kg=plat_base.dry_mass_kg,
            options_mass_kg=round(opt_mass, 2),
            payloads_mass_kg=round(pl_mass, 2),
            system_dry_mass_kg=round(sys_dry_kg, 2),
            propellant_mass_kg=round(prop_mass, 2),
            system_wet_mass_kg=round(wet_mass_kg, 2),
            margin_pct=margin_pct,
            launch_mass_with_margin_kg=round(launch_mass_with_margin_kg, 2),
            platform_capacity_kg=plat_base.max_payload_mass_kg,
        )

        # Platform Payload Mass Limit check
        if pl_mass > plat_base.max_payload_mass_kg:
            rule_checks.append(
                RuleCheckResult(
                    rule_id="RULE_MASS_PAYLOAD_MAX",
                    category="Mass",
                    status=CheckStatus.FAIL,
                    message=f"Total payload mass ({pl_mass:.1f} kg) exceeds platform capability ({plat_base.max_payload_mass_kg:.1f} kg)",
                    current_value=pl_mass,
                    target_value=plat_base.max_payload_mass_kg,
                    unit="kg",
                )
            )
        else:
            rule_checks.append(
                RuleCheckResult(
                    rule_id="RULE_MASS_PAYLOAD_MAX",
                    category="Mass",
                    status=CheckStatus.PASS,
                    message=f"Payload mass ({pl_mass:.1f} kg) within platform capability ({plat_base.max_payload_mass_kg:.1f} kg)",
                    current_value=pl_mass,
                    target_value=plat_base.max_payload_mass_kg,
                    unit="kg",
                )
            )

        # 2. Power Budget
        # Payload operational power is drawn during imaging passes (e.g. ~25% duty cycle nominal)
        pl_power_avg = sum(p.operational_power_w for p in payloads) * 0.25

        # For options: propulsion uses standby power during nominal orbit, operational during burns
        opt_power_avg = 0.0
        for opt in conf_plat.resolved_options:
            if opt.equipment.function.value == "propulsion":
                opt_power_avg += opt.equipment.standby_power_w
            else:
                opt_power_avg += opt.equipment.power_w

        total_cons_avg = opt_power_avg + pl_power_avg
        power_margin_w = plat_base.payload_avg_power_w - total_cons_avg
        power_margin_pct = (power_margin_w / plat_base.payload_avg_power_w) * 100.0 if plat_base.payload_avg_power_w > 0 else 0.0

        peak_cons = sum(p.peak_power_w for p in payloads) + sum(
            opt.equipment.peak_power_w for opt in conf_plat.resolved_options
        )

        power_b = PowerBudget(
            platform_avg_power_w=plat_base.orbit_avg_power_w,
            options_avg_power_w=round(opt_power_avg, 1),
            payloads_avg_power_w=round(pl_power_avg, 1),
            total_avg_consumption_w=round(total_cons_avg, 1),
            platform_generation_w=plat_base.payload_avg_power_w,
            power_margin_w=round(power_margin_w, 1),
            power_margin_pct=round(power_margin_pct, 1),
            peak_consumption_w=round(peak_cons, 1),
        )

        if power_margin_w < 0:
            rule_checks.append(
                RuleCheckResult(
                    rule_id="RULE_POWER_AVG_DEFICIT",
                    category="Power",
                    status=CheckStatus.FAIL,
                    message=f"Average consumption ({total_cons_avg:.1f} W) exceeds available platform power ({plat_base.payload_avg_power_w:.1f} W)",
                    current_value=total_cons_avg,
                    target_value=plat_base.payload_avg_power_w,
                    unit="W",
                )
            )
        elif power_margin_pct < 15.0:
            rule_checks.append(
                RuleCheckResult(
                    rule_id="RULE_POWER_MARGIN_LOW",
                    category="Power",
                    status=CheckStatus.WARNING,
                    message=f"Power margin is tight ({power_margin_pct:.1f}% < 15% recommended)",
                    current_value=power_margin_pct,
                    target_value=15.0,
                    unit="%",
                )
            )
        else:
            rule_checks.append(
                RuleCheckResult(
                    rule_id="RULE_POWER_OK",
                    category="Power",
                    status=CheckStatus.PASS,
                    message=f"Power margin healthy ({power_margin_pct:.1f}%)",
                    current_value=power_margin_pct,
                    target_value=15.0,
                    unit="%",
                )
            )

        # 3. Cost Budget
        launcher_cost = 0.0
        if config.launcher_id and config.launcher_id in self.catalog.launchers:
            ln = self.catalog.launchers[config.launcher_id]
            launcher_cost = ln.price_base_meur + (
                ln.price_per_kg_meur * launch_mass_with_margin_kg
            )
        elif config.launcher_id:
            rule_checks.append(
                RuleCheckResult(
                    rule_id="RULE_LAUNCHER_MISSING",
                    category="Cost",
                    status=CheckStatus.FAIL,
                    message=f"Selected launcher '{config.launcher_id}' not found in catalog",
                )
            )

        plat_cost = plat_base.base_price_meur
        opt_cost = sum(opt.final_price_meur for opt in conf_plat.resolved_options)
        pl_cost = sum(p.price_meur for p in payloads)
        total_cost = plat_cost + opt_cost + pl_cost + launcher_cost
        cost_margin = mission.max_budget_meur - total_cost

        cost_b = CostBudget(
            platform_base_meur=round(plat_cost, 2),
            options_total_meur=round(opt_cost, 2),
            payloads_total_meur=round(pl_cost, 2),
            launcher_meur=round(launcher_cost, 2),
            space_segment_total_meur=round(total_cost, 2),
            mission_budget_limit_meur=mission.max_budget_meur,
            cost_margin_meur=round(cost_margin, 2),
        )

        if total_cost > mission.max_budget_meur:
            compliance_checks.append(
                RuleCheckResult(
                    rule_id="REQ_BUDGET_EXCEEDED",
                    category="Mission Budget",
                    status=CheckStatus.FAIL,
                    message=f"Total cost ({total_cost:.2f} M€) exceeds mission ceiling ({mission.max_budget_meur:.2f} M€)",
                    current_value=total_cost,
                    target_value=mission.max_budget_meur,
                    unit="M€",
                )
            )
        else:
            compliance_checks.append(
                RuleCheckResult(
                    rule_id="REQ_BUDGET_OK",
                    category="Mission Budget",
                    status=CheckStatus.PASS,
                    message=f"Total cost ({total_cost:.2f} M€) within budget ({mission.max_budget_meur:.2f} M€)",
                    current_value=total_cost,
                    target_value=mission.max_budget_meur,
                    unit="M€",
                )
            )

        # 4. Pointing Compatibility Check
        # Effective platform pointing accuracy takes into account high-accuracy ADCS packs if installed
        effective_pointing_accuracy_deg = plat_base.pointing_accuracy_deg
        for opt in conf_plat.resolved_options:
            if opt.equipment.function.value == "adcs":
                adcs_acc = opt.equipment.specs.get("pointing_accuracy_deg")
                if adcs_acc is not None and adcs_acc < effective_pointing_accuracy_deg:
                    effective_pointing_accuracy_deg = adcs_acc

        for pl in payloads:
            if effective_pointing_accuracy_deg > pl.required_pointing_accuracy_deg:
                rule_checks.append(
                    RuleCheckResult(
                        rule_id=f"RULE_POINTING_{pl.id}",
                        category="ADCS Compatibility",
                        status=CheckStatus.FAIL,
                        message=f"Platform pointing accuracy ({effective_pointing_accuracy_deg}°) is worse than required by '{pl.name}' ({pl.required_pointing_accuracy_deg}°)",
                        current_value=effective_pointing_accuracy_deg,
                        target_value=pl.required_pointing_accuracy_deg,
                        unit="deg",
                    )
                )
            else:
                rule_checks.append(
                    RuleCheckResult(
                        rule_id=f"RULE_POINTING_{pl.id}",
                        category="ADCS Compatibility",
                        status=CheckStatus.PASS,
                        message=f"Pointing accuracy ({effective_pointing_accuracy_deg}°) meets requirement for '{pl.name}' ({pl.required_pointing_accuracy_deg}°)",
                        current_value=effective_pointing_accuracy_deg,
                        target_value=pl.required_pointing_accuracy_deg,
                        unit="deg",
                    )
                )

        # 5. Payload Performances & Mission Requirements Verification
        payload_perfs: dict[str, Any] = {}
        for pl in payloads:
            if pl.payload_type == PayloadType.OPTICAL_IMAGER:
                assert isinstance(pl, OpticalImagerPayload)
                perf = OpticalImagerModel.compute(pl, config.orbit)
                payload_perfs[pl.id] = perf

                # Check against mission requirements
                for req in mission.requirements:
                    if req.parameter == "gsd_nadir_m":
                        pass_req = (
                            perf.gsd_nadir_m <= float(req.threshold)
                            if req.operator == RequirementOperator.LE
                            else False
                        )
                        compliance_checks.append(
                            RuleCheckResult(
                                rule_id=req.id,
                                category="Mission Requirement",
                                status=CheckStatus.PASS if pass_req else CheckStatus.FAIL,
                                message=f"{req.title}: computed GSD = {perf.gsd_nadir_m:.2f} m (threshold: {req.threshold} m)",
                                current_value=perf.gsd_nadir_m,
                                target_value=float(req.threshold),
                                unit="m",
                            )
                        )
                    elif req.parameter == "swath_width_km":
                        pass_req = (
                            perf.swath_width_km >= float(req.threshold)
                            if req.operator == RequirementOperator.GE
                            else False
                        )
                        compliance_checks.append(
                            RuleCheckResult(
                                rule_id=req.id,
                                category="Mission Requirement",
                                status=CheckStatus.PASS if pass_req else CheckStatus.FAIL,
                                message=f"{req.title}: computed Swath = {perf.swath_width_km:.1f} km (threshold: {req.threshold} km)",
                                current_value=perf.swath_width_km,
                                target_value=float(req.threshold),
                                unit="km",
                            )
                        )

        return SystemBudgets(
            configured_platform=conf_plat,
            mass=mass_b,
            power=power_b,
            cost=cost_b,
            payload_performances=payload_perfs,
            rule_checks=rule_checks,
            compliance_checks=compliance_checks,
        )
