"""Test evaluation of SAR and QKD missions against their specific mission requirements."""

from ssb.core.orbit import OrbitDefinition
from ssb.core.mission import MissionSpecification
from ssb.core.project import SystemConfiguration, SelectedOption
from ssb.catalog.database import CatalogDatabase
from ssb.system.evaluator import SystemEvaluator, CheckStatus


def test_sar_mission_evaluation_pass():
    db = CatalogDatabase()
    db.load_from_directory("data/catalogs")
    evaluator = SystemEvaluator(db)

    # Load the SAR exam mission
    import json
    with open("data/missions/exam_sar_surveillance.mission.json", "r", encoding="utf-8") as f:
        m_data = json.load(f)
    sar_mission = MissionSpecification.model_validate(m_data)

    # Student config: ApexBus-500 + MicroSAR-X + Ka-Band downlink + dedicated launcher
    orbit = OrbitDefinition(altitude_km=500.0, inclination_deg=97.4)
    config = SystemConfiguration(
        orbit=orbit,
        platform_id="plat_apex_pro500",
        selected_options=[
            SelectedOption(slot_function="propulsion", equipment_id="prop_electric_hall_1kw"),
            SelectedOption(slot_function="payload_downlink", equipment_id="downlink_kaband_tx_2gbps"),
            SelectedOption(slot_function="mass_memory", equipment_id="mass_mem_2tb_highrel"),
            SelectedOption(slot_function="adcs", equipment_id="adcs_cmg_agility_pack"),
        ],
        selected_payload_ids=["pl_sar_xband_micro"],
        launcher_id="ln_dedicated_medium",
    )

    budgets = evaluator.evaluate(config, sar_mission)
    # 1. Mass within 240 kg payload capability (MicroSAR is 55 kg)
    assert budgets.mass.payloads_mass_kg == 55.0
    # 2. Check SAR requirements:
    # REQ-SAR-AZ-01: Azimuth resolution <= 2.0 m
    # REQ-SAR-SWATH-01: Swath >= 15.0 km
    req_checks = {c.rule_id: c for c in budgets.compliance_checks}
    assert req_checks["REQ-SAR-AZ-01"].status == CheckStatus.PASS
    assert req_checks["REQ-SAR-SWATH-01"].status == CheckStatus.PASS


def test_qkd_mission_evaluation_pass():
    db = CatalogDatabase()
    db.load_from_directory("data/catalogs")
    evaluator = SystemEvaluator(db)

    import json
    with open("data/missions/exam_qkd_secure_links.mission.json", "r", encoding="utf-8") as f:
        m_data = json.load(f)
    qkd_mission = MissionSpecification.model_validate(m_data)

    orbit = OrbitDefinition(altitude_km=500.0, inclination_deg=97.4)
    config = SystemConfiguration(
        orbit=orbit,
        platform_id="plat_astra_flex150",
        selected_options=[
            SelectedOption(slot_function="adcs", equipment_id="adcs_high_accuracy_pack"),
        ],
        selected_payload_ids=["pl_qkd_terminal_decoy"],
        launcher_id="ln_rideshare_sso",
    )

    budgets = evaluator.evaluate(config, qkd_mission)
    req_checks = {c.rule_id: c for c in budgets.compliance_checks}
    assert req_checks["REQ-QKD-QBER-01"].status == CheckStatus.PASS
    assert req_checks["REQ-QKD-SKR-01"].status == CheckStatus.PASS
    assert req_checks["REQ-POINTING-QKD"].status == CheckStatus.PASS
