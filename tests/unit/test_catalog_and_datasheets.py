"""Unit tests for theenriched multi-supplier catalogs, datasheets, mission specification sheets, and offscreen GUI rendering."""

import os
from ssb.catalog.database import CatalogDatabase
from ssb.catalog.datasheet import build_datasheet
from ssb.core.mission import MissionSpecification
from ssb.core.paths import catalogs_dir, images_dir, missions_dir
from ssb.core.orbit import OrbitDefinition
from ssb.core.project import SystemConfiguration, SelectedOption
from ssb.system.evaluator import SystemEvaluator, CheckStatus


def test_enriched_catalog_counts_and_datasheets():
    db = CatalogDatabase()
    db.load_from_directory(catalogs_dir())

    assert len(db.suppliers) >= 18
    assert len(db.platforms) >= 16
    assert len(db.payloads) >= 33
    assert len(db.equipments) >= 31
    assert len(db.launchers) >= 8

    plat_suppliers = db.suppliers_for("platform")
    assert len(plat_suppliers) == 5
    for sup in plat_suppliers:
        items = db.items_by_supplier(sup.id, "platform")
        assert len(items) >= 3, f"Supplier {sup.id} should have at least 3 platforms"

    orbit = OrbitDefinition(altitude_km=550.0, inclination_deg=97.6)
    img_root = images_dir()
    for coll in (db.platforms, db.payloads, db.equipments, db.launchers):
        for item in coll.values():
            assert item.description, f"Missing short description on {item.id}"
            assert len(item.long_description) >= 80, f"Long description too short on {item.id}"
            assert len(item.key_features) >= 3, f"Missing key features on {item.id}"
            assert item.image and (img_root / item.image).exists(), f"Missing image for {item.id}"

            ds = build_datasheet(item, orbit)
            assert ds.name == item.name
            assert len(ds.sections) >= 2
            assert any(len(s.rows) > 0 for s in ds.sections)


def test_mission_specification_sheets_and_solutions():
    db = CatalogDatabase()
    db.load_from_directory(catalogs_dir())
    evaluator = SystemEvaluator(db)

    mfiles = sorted(missions_dir().glob("*.mission.json"))
    assert len(mfiles) >= 6

    missions: dict[str, MissionSpecification] = {}
    for mf in mfiles:
        ms = MissionSpecification.model_validate_json(mf.read_text(encoding="utf-8"))
        assert ms.max_budget_meur > 0
        assert len(ms.context) >= 50
        assert len(ms.primary_objective) >= 80
        assert len(ms.domain_label) >= 10
        assert len(ms.requirements) >= 2
        missions[ms.id] = ms

    # Reference valid student solutions for the new mission sheets:
    solutions = [
        # 1. Optical EO (budget 18 M€, GSD <= 1.0 m, swath >= 10 km, SNR >= 80)
        (
            "EXAM-2026-EO-OPT",
            SystemConfiguration(
                orbit=OrbitDefinition(altitude_km=500.0, inclination_deg=97.4),
                platform_id="plat_sstl_mini150",
                selected_options=[
                    SelectedOption(slot_function="ttc", equipment_id="ttc_sband_transceiver"),
                    SelectedOption(slot_function="mass_memory", equipment_id="mass_mem_512gb"),
                    SelectedOption(slot_function="adcs", equipment_id="adcs_high_accuracy_pack"),
                ],
                selected_payload_ids=["pl_opt_stellara_35cm"],
                launcher_id="ln_rideshare_sso",
            ),
        ),
        # 2. Atmosphere GHG (budget 16.5 M€, spectral_resolution <= 1.0 nm, max_wl >= 1650 nm, GSD <= 10 m, SNR >= 50)
        (
            "EXAM-2026-ATMO-GHG",
            SystemConfiguration(
                orbit=OrbitDefinition(altitude_km=500.0, inclination_deg=97.4),
                platform_id="plat_sstl_mini150",
                selected_options=[
                    SelectedOption(slot_function="ttc", equipment_id="ttc_sband_transceiver"),
                    SelectedOption(slot_function="mass_memory", equipment_id="mass_mem_512gb"),
                ],
                selected_payload_ids=["pl_spec_ghg_sounder"],
                launcher_id="ln_rideshare_sso",
            ),
        ),
        # 3. Cosmology deep field (budget 32 M€, aperture >= 0.60 m, diffraction <= 0.65 m, pointing <= 0.004 deg)
        (
            "EXAM-2026-COSMO",
            SystemConfiguration(
                orbit=OrbitDefinition(altitude_km=500.0, inclination_deg=97.4),
                platform_id="plat_sstl_midi300",
                selected_options=[
                    SelectedOption(slot_function="propulsion", equipment_id="prop_green_5n"),
                    SelectedOption(slot_function="ttc", equipment_id="ttc_sband_transceiver"),
                    SelectedOption(slot_function="payload_downlink", equipment_id="downlink_xband_tx"),
                    SelectedOption(slot_function="mass_memory", equipment_id="mass_mem_1tb"),
                    SelectedOption(slot_function="adcs", equipment_id="adcs_agile_wheels_medium"),
                ],
                selected_payload_ids=["pl_opt_stellara_60cm"],
                launcher_id="ln_rideshare_sso",
            ),
        ),
        # 4. High throughput laser datalink (budget 15 M€, rate >= 25 Gbps, margin >= 6 dB, pointing <= 0.008 deg)
        (
            "EXAM-2026-DATARATE",
            SystemConfiguration(
                orbit=OrbitDefinition(altitude_km=500.0, inclination_deg=97.4),
                platform_id="plat_sstl_micro50",
                selected_options=[
                    SelectedOption(slot_function="ttc", equipment_id="ttc_sband_transceiver"),
                    SelectedOption(slot_function="mass_memory", equipment_id="mass_mem_512gb"),
                    SelectedOption(slot_function="adcs", equipment_id="adcs_high_accuracy_pack"),
                ],
                selected_payload_ids=["pl_opt_comm_isl_25g"],
                launcher_id="ln_rideshare_sso",
            ),
        ),
        # 5. Low-cost CubeSat RF/IoT (budget 1.6 M€, rate >= 15 Mbps, margin >= 3 dB)
        (
            "EXAM-2026-CUBESAT-RF",
            SystemConfiguration(
                orbit=OrbitDefinition(altitude_km=500.0, inclination_deg=97.4),
                platform_id="plat_aeromicro_6u",
                selected_options=[
                    SelectedOption(slot_function="ttc", equipment_id="ttc_uhf_cubesat"),
                    SelectedOption(slot_function="mass_memory", equipment_id="mass_mem_64gb"),
                    SelectedOption(slot_function="adcs", equipment_id="adcs_cubesat_precision"),
                ],
                selected_payload_ids=["pl_rf_ais_adsb"],
                launcher_id="ln_cubesat_deployer",
            ),
        ),
    ]

    for mid, cfg in solutions:
        ms = missions[mid]
        b = evaluator.evaluate(cfg, ms)
        failed = [c for c in (b.compliance_checks + b.rule_checks) if c.status == CheckStatus.FAIL]
        assert not failed, f"Mission {mid} failed checks: {[(c.rule_id, c.message) for c in failed]}"


def test_student_and_teacher_gui_offscreen():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtWidgets import QApplication
    from ssb.student_app.main_window import StudentMainWindow
    from ssb.teacher_app.main_window import TeacherMainWindow

    app = QApplication.instance() or QApplication([])
    win = StudentMainWindow()
    assert win.current_budgets is not None
    assert win.cmb_preset_missions.count() >= 6
    assert win.browser_payloads.list_suppliers.count() > 5
    assert win.browser_platforms.list_suppliers.count() == 6

    # Switch between mission specification sheets in the student window
    for idx in range(win.cmb_preset_missions.count()):
        win.cmb_preset_missions.setCurrentIndex(idx)
        assert win.mission_sheet_view.t_reqs.rowCount() >= 3

    win.browser_payloads.list_suppliers.setCurrentRow(1)
    assert win.browser_payloads.list_items.count() >= 1

    second_pl = win.catalog.payloads["pl_opt_comm_terminal_10g"]
    win._add_payload_from_browser(second_pl)
    assert len(win.project.configuration.selected_payload_ids) == 2

    twin = TeacherMainWindow()
    assert twin.tabs.count() == 3
    assert twin.cmb_existing_missions.count() >= 7
    twin.cmb_existing_missions.setCurrentIndex(1)
    win.close()
    twin.close()
    assert app is not None
