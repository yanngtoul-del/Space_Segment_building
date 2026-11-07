"""Test catalog loading, slot configuration, optical model, and system budgets."""

from pathlib import Path
from ssb.catalog.database import CatalogDatabase
from ssb.core.orbit import OrbitDefinition, OrbitType
from ssb.core.mission import (
    MissionSpecification,
    MissionRequirement,
    RequirementType,
    RequirementOperator,
)
from ssb.core.project import SystemConfiguration, SelectedOption
from ssb.system.evaluator import SystemEvaluator, CheckStatus


def test_catalog_load_and_validation():
    db = CatalogDatabase()
    cat_dir = Path("data/catalogs")
    db.load_from_directory(cat_dir)

    assert len(db.platforms) >= 2
    assert len(db.equipments) >= 5
    assert len(db.payloads) >= 3
    assert len(db.launchers) >= 2
    assert "plat_aeromicro_16u" in db.platforms
    assert "plat_astra_flex150" in db.platforms


def test_orbit_sso_inclination():
    # 500 km altitude SSO inclination should be around 97.4 deg
    inc = OrbitDefinition.compute_sso_inclination(500.0)
    assert 97.0 < inc < 98.0

    # 700 km altitude SSO inclination should be around 98.2 deg
    inc_700 = OrbitDefinition.compute_sso_inclination(700.0)
    assert 98.0 < inc_700 < 98.5


def test_platform_slot_resolution_and_rules():
    db = CatalogDatabase()
    db.load_from_directory("data/catalogs")
    evaluator = SystemEvaluator(db)

    # 1. Test case: MicroBus-16U with EagleEye-45 (too heavy: 48 kg > 10 kg capability)
    config_fail = SystemConfiguration(
        orbit=OrbitDefinition(altitude_km=500.0),
        platform_id="plat_aeromicro_16u",
        selected_payload_ids=["pl_opt_submeter_highres"],
        launcher_id="ln_rideshare_sso",
    )
    mission = MissionSpecification(
        id="M-TEST",
        title="Test Mission",
        context="Evaluation of mass overrun",
        mission_type="optical_eo",
        max_budget_meur=20.0,
        requirements=[
            MissionRequirement(
                id="REQ-GSD",
                title="GSD requirement",
                description="GSD <= 1.0 m",
                req_type=RequirementType.PAYLOAD_PERF,
                parameter="gsd_nadir_m",
                operator=RequirementOperator.LE,
                threshold=1.0,
                unit="m",
            )
        ],
    )

    budgets_fail = evaluator.evaluate(config_fail, mission)
    assert budgets_fail.has_blocking_errors
    # Verify the mass error was caught
    mass_checks = [c for c in budgets_fail.rule_checks if c.rule_id == "RULE_MASS_PAYLOAD_MAX"]
    assert len(mass_checks) == 1
    assert mass_checks[0].status == CheckStatus.FAIL

    # 2. Test case: AstraFlex-150 with EagleEye-45 + propulsion + downlink + ADCS pack
    config_pass = SystemConfiguration(
        orbit=OrbitDefinition(altitude_km=500.0),
        platform_id="plat_astra_flex150",
        selected_options=[
            SelectedOption(slot_function="propulsion", equipment_id="prop_electric_hall_100w"),
            SelectedOption(slot_function="payload_downlink", equipment_id="downlink_xband_tx"),
            SelectedOption(slot_function="adcs", equipment_id="adcs_high_accuracy_pack"),
        ],
        selected_payload_ids=["pl_opt_submeter_highres"],
        launcher_id="ln_rideshare_sso",
    )

    budgets_pass = evaluator.evaluate(config_pass, mission)
    # GSD for EagleEye-45 at 500 km: 6.5 um * 500 km / 4.2 m = 0.77 m <= 1.0 m -> PASS
    gsd_checks = [c for c in budgets_pass.compliance_checks if c.rule_id == "REQ-GSD"]
    assert len(gsd_checks) == 1
    assert gsd_checks[0].status == CheckStatus.PASS
    assert gsd_checks[0].current_value < 1.0

    # Verify Mass and Budget
    assert budgets_pass.mass.payloads_mass_kg == 48.0
    assert budgets_pass.cost.space_segment_total_meur == 16.0
    assert budgets_pass.cost.space_segment_total_meur <= mission.max_budget_meur
    assert not budgets_pass.has_blocking_errors
