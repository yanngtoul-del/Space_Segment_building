"""Test SAR performance models, optical communication budgets, and CONOPS simulation."""

from pathlib import Path
from ssb.core.orbit import OrbitDefinition
from ssb.core.mission import GroundStationTarget, MissionSpecification
from ssb.core.project import SystemConfiguration, SelectedOption
from ssb.catalog.database import CatalogDatabase
from ssb.payload.sar_model import SarModel
from ssb.payload.comm_model import OpticalCommModel, RadioCommModel
from ssb.orbit.propagator import OrbitPropagator
from ssb.orbit.station_access import StationAccessCalculator
from ssb.system.evaluator import SystemEvaluator
from ssb.conops.simulator import ConopsSimulator, OperationalMode


def test_sar_model_azimuth_and_nesz():
    db = CatalogDatabase()
    db.load_from_directory("data/catalogs")
    sar_pl = db.payloads["pl_sar_xband_micro"]

    orbit = OrbitDefinition(altitude_km=500.0)
    perf = SarModel.compute(sar_pl, orbit, incidence_angle_deg=35.0)

    # For a 3.2 m antenna, theoretical stripmap azimuth resolution is L/2 = 1.6 m
    assert perf.azimuth_resolution_stripmap_m == 1.6
    # Slant range at 500 km altitude and 35 deg incidence is ~610 km
    assert 550.0 < perf.slant_range_mid_swath_km < 650.0
    # X-Band NESZ for this micro-SAR configuration with 2 kW peak power:
    assert -25.0 < perf.nesz_db < 0.0
    # Wavelength for 9.6 GHz should be ~3.12 cm
    assert 0.03 < perf.wavelength_m < 0.035


def test_optical_and_radio_link_budgets():
    # 1. Optical link LEO (1000 km) with 1 W TX, 10 cm TX aperture, 80 cm OGS RX aperture
    opt_link = OpticalCommModel.compute_leo_to_ground_link(
        tx_power_w=1.0,
        tx_aperture_m=0.10,
        rx_aperture_m=0.80,
        wavelength_nm=1550.0,
        slant_range_km=1000.0,
        pointing_error_urad=2.0,
    )
    assert opt_link.margin_db > 3.0  # Link closed with positive margin
    assert opt_link.achievable_data_rate_gbps == 2.5

    # 2. X-Band Downlink budget: 10 W RF, 8.2 GHz, 12 dBi sat antenna, 7.3 m ground dish
    rf_link = RadioCommModel.compute_downlink_budget(
        rf_power_w=10.0,
        carrier_freq_ghz=8.2,
        satellite_antenna_gain_dbi=12.0,
        ground_antenna_diameter_m=7.3,
        data_rate_mbps=500.0,
        slant_range_km=1200.0,
    )
    assert rf_link.link_margin_db > 3.0
    assert rf_link.eb_over_n0_db > 9.0


def test_conops_multi_orbit_timeline():
    db = CatalogDatabase()
    db.load_from_directory("data/catalogs")
    evaluator = SystemEvaluator(db)

    orbit = OrbitDefinition(altitude_km=500.0, inclination_deg=97.4)
    mission = MissionSpecification(
        id="M-CONOPS",
        title="CONOPS Test",
        context="",
        mission_type="optical_eo",
        max_budget_meur=20.0,
    )

    config = SystemConfiguration(
        orbit=orbit,
        platform_id="plat_astra_flex150",
        selected_options=[
            SelectedOption(slot_function="payload_downlink", equipment_id="downlink_xband_tx"),
            SelectedOption(slot_function="mass_memory", equipment_id="mass_mem_512gb"),
        ],
        selected_payload_ids=["pl_opt_submeter_highres"],
        launcher_id="ln_rideshare_sso",
    )

    budgets = evaluator.evaluate(config, mission)

    # Propagate 2 orbits (~3 hours)
    sim = OrbitPropagator.simulate(orbit, duration_orbits=2.0, samples_per_orbit=60)
    svalbard = GroundStationTarget(
        id="svalbard",
        name="Svalbard",
        latitude_deg=78.22,
        longitude_deg=15.40,
        min_elevation_deg=5.0,
    )
    passes = StationAccessCalculator.find_passes(sim.ground_track, svalbard)

    conops_rep = ConopsSimulator.simulate(
        budgets=budgets,
        orbit=orbit,
        ground_track=sim.ground_track,
        passes=passes,
        imaging_duty_cycle_sunlit_pct=20.0,
    )

    assert conops_rep.duration_days > 0.1
    # Battery state of charge should remain healthy (>60%)
    assert conops_rep.min_battery_soc_pct > 60.0
    assert conops_rep.total_data_acquired_gb > 0.0
    assert len(conops_rep.time_series) == len(sim.ground_track) - 1
