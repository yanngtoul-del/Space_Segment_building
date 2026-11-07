"""Unit tests for the enriched multi-supplier catalogs, datasheets, mission specification sheets, and offscreen GUI rendering."""

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

    assert len(db.suppliers) >= 35
    assert len(db.platforms) >= 16
    assert len(db.payloads) >= 50
    assert len(db.equipments) >= 31
    assert len(db.launchers) >= 8

    plat_suppliers = db.suppliers_for("platform")
    assert len(plat_suppliers) == 5
    for sup in plat_suppliers:
        items = db.items_by_supplier(sup.id, "platform")
        assert len(items) >= 3, f"Supplier {sup.id} should have at least 3 platforms"

    # Every payload type must have at least 4 distinct suppliers (and SAR / radio_comm at least 5)
    suppliers_by_ptype: dict[str, set[str]] = {}
    for p in db.payloads.values():
        suppliers_by_ptype.setdefault(p.payload_type.value, set()).add(p.supplier_id)
    for ptype in ("optical_imager", "spectrometer", "sar", "optical_comm", "qkd", "radio_comm"):
        assert len(suppliers_by_ptype.get(ptype, set())) >= 4, (
            f"Payload type {ptype} should have at least 4 distinct suppliers"
        )
    assert len(suppliers_by_ptype["sar"]) >= 5
    assert len(suppliers_by_ptype["radio_comm"]) >= 5

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

    # Reference valid student solutions across multiple competing suppliers,
    # strictly satisfying technical requirements and ESA Member State geographic return quotas:
    solutions = [
        # 1. Optical EO (budget 18 M€, GSD <= 1.0 m, swath >= 10 km, SNR >= 55)
        # Geo-return: France [35-55%], Italie [25-45%], Allemagne [8-25%]
        (
            "EXAM-2026-EO-OPT",
            SystemConfiguration(
                orbit=OrbitDefinition(altitude_km=500.0, inclination_deg=97.4),
                platform_id="plat_astra_flex150",
                selected_options=[
                    SelectedOption(slot_function="propulsion", equipment_id="prop_electric_hemp_de"),
                    SelectedOption(slot_function="ttc", equipment_id="ttc_sband_gallia_fr"),
                    SelectedOption(slot_function="mass_memory", equipment_id="mass_mem_1tb_de"),
                    SelectedOption(slot_function="adcs", equipment_id="adcs_sodern_auriga_fr"),
                ],
                selected_payload_ids=["pl_opt_stellara_35cm"],
                launcher_id="ln_rideshare_sso",
            ),
        ),
        # 2. SAR surveillance — Solution with Aegis Radar institutional SAR
        # Geo-return: Allemagne [40-65%], France [30-50%], Italie [3-15%]
        (
            "EXAM-2026-SAR",
            SystemConfiguration(
                orbit=OrbitDefinition(altitude_km=500.0, inclination_deg=97.4),
                platform_id="plat_astra_flex300",
                selected_options=[
                    SelectedOption(slot_function="ttc", equipment_id="ttc_sband_aurora_it"),
                    SelectedOption(slot_function="payload_downlink", equipment_id="downlink_xband_milan_it"),
                ],
                selected_payload_ids=["pl_sar_aegis_x_tactical"],
                launcher_id="ln_rideshare_sso",
            ),
        ),
        # 3. Atmosphere GHG — AtmoSonde Scientific Instruments (SWIR 1720 nm)
        # Geo-return: France [35-60%], Allemagne [10-30%], Espagne [5-20%]
        (
            "EXAM-2026-ATMO-GHG",
            SystemConfiguration(
                orbit=OrbitDefinition(altitude_km=500.0, inclination_deg=97.4),
                platform_id="plat_sstl_mini150",
                selected_options=[
                    SelectedOption(slot_function="propulsion", equipment_id="prop_electric_hemp_de"),
                    SelectedOption(slot_function="ttc", equipment_id="ttc_xband_tmtc"),
                    SelectedOption(slot_function="mass_memory", equipment_id="mass_mem_1tb"),
                    SelectedOption(slot_function="adcs", equipment_id="adcs_high_accuracy_pack"),
                ],
                selected_payload_ids=["pl_spec_atmo_tropo_ghg"],
                launcher_id="ln_rideshare_sso",
            ),
        ),
        # 4. Cosmology deep field (budget 32 M€, aperture >= 0.60 m, diffraction <= 0.72 m, pointing <= 0.004 deg)
        # Geo-return: Italie [40-65%], France [25-50%], Allemagne [4-18%]
        (
            "EXAM-2026-COSMO",
            SystemConfiguration(
                orbit=OrbitDefinition(altitude_km=500.0, inclination_deg=97.4),
                platform_id="plat_astra_flex300",
                selected_options=[
                    SelectedOption(slot_function="propulsion", equipment_id="prop_electric_hemp_de"),
                    SelectedOption(slot_function="ttc", equipment_id="ttc_sband_dual_redundant"),
                    SelectedOption(slot_function="payload_downlink", equipment_id="downlink_xband_tx"),
                    SelectedOption(slot_function="mass_memory", equipment_id="mass_mem_1tb_de"),
                    SelectedOption(slot_function="adcs", equipment_id="adcs_agile_wheels_medium"),
                ],
                selected_payload_ids=["pl_opt_stellara_60cm"],
                launcher_id="ln_espa_heavy_rideshare",
            ),
        ),
        # 5. High throughput laser datalink — TeraLink Photonics (25 Gbps)
        # Geo-return: France [35-60%], Allemagne [30-55%], Suisse [2-12%]
        (
            "EXAM-2026-DATARATE",
            SystemConfiguration(
                orbit=OrbitDefinition(altitude_km=500.0, inclination_deg=97.4),
                platform_id="plat_astra_flex150",
                selected_options=[
                    SelectedOption(slot_function="ttc", equipment_id="ttc_sband_gallia_fr"),
                    SelectedOption(slot_function="mass_memory", equipment_id="mass_mem_1tb_ch"),
                    SelectedOption(slot_function="adcs", equipment_id="adcs_sodern_auriga_fr"),
                ],
                selected_payload_ids=["pl_opt_comm_isl_25g"],
                launcher_id="ln_rideshare_sso",
            ),
        ),
        # 6a. Low-cost CubeSat RF/IoT — Meridian RF Payloads
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
        # 6b. Low-cost CubeSat RF/IoT — Nordic NanoComm Systems (plus léger, permet d'ajouter une caméra 6cm !)
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
                selected_payload_ids=["pl_rf_nordic_ais_sdr", "pl_opt_cubesat_6cm"],
                launcher_id="ln_cubesat_deployer",
            ),
        ),
        # 7. Light low-cost optical EO (budget 2.80 M€, GSD <= 3.5 m, swath >= 12 km, SNR >= 50)
        (
            "EXAM-2026-EO-LIGHT",
            SystemConfiguration(
                orbit=OrbitDefinition(altitude_km=500.0, inclination_deg=97.4),
                platform_id="plat_aeromicro_12u",
                selected_options=[
                    SelectedOption(slot_function="ttc", equipment_id="ttc_uhf_cubesat"),
                    SelectedOption(slot_function="mass_memory", equipment_id="mass_mem_64gb"),
                    SelectedOption(slot_function="adcs", equipment_id="adcs_cubesat_precision"),
                ],
                selected_payload_ids=["pl_opt_pan_compact"],
                launcher_id="ln_cubesat_deployer",
            ),
        ),
        # 8. High-performance sub-metric optical EO (budget 35 M€, GSD <= 0.40 m, aperture >= 0.70 m, pointing <= 0.004 deg, lifetime >= 7 yr)
        (
            "EXAM-2026-EO-HIGHPERF",
            SystemConfiguration(
                orbit=OrbitDefinition(altitude_km=500.0, inclination_deg=97.4),
                platform_id="plat_astra_flex300",
                selected_options=[
                    SelectedOption(slot_function="propulsion", equipment_id="prop_green_5n"),
                    SelectedOption(slot_function="ttc", equipment_id="ttc_sband_dual_redundant"),
                    SelectedOption(slot_function="payload_downlink", equipment_id="downlink_xband_tx"),
                    SelectedOption(slot_function="mass_memory", equipment_id="mass_mem_1tb"),
                    SelectedOption(slot_function="adcs", equipment_id="adcs_agile_wheels_medium"),
                ],
                selected_payload_ids=["pl_opt_helios_70cm"],
                launcher_id="ln_espa_heavy_rideshare",
            ),
        ),
        # 9. Classical GEO telecommunications (budget 55 M€, GEO 35,786 km, rate >= 600 Mbps, margin >= 3.5 dB, lifetime >= 12 yr)
        # Geo-return: France [45-75%], Suisse [20-40%], Allemagne [3-15%]
        (
            "EXAM-2026-GEO-COMMS",
            SystemConfiguration(
                orbit=OrbitDefinition(altitude_km=35786.0, inclination_deg=0.0),
                platform_id="plat_smallgeo_500",
                selected_options=[
                    SelectedOption(slot_function="propulsion", equipment_id="prop_electric_hall_1kw"),
                    SelectedOption(slot_function="ttc", equipment_id="ttc_sband_transceiver"),
                    SelectedOption(slot_function="mass_memory", equipment_id="mass_mem_1tb_de"),
                    SelectedOption(slot_function="adcs", equipment_id="adcs_agile_wheels_medium"),
                ],
                selected_payload_ids=["pl_rf_smallgeo_ku_relay"],
                launcher_id="ln_gto_rideshare",
            ),
        ),
    ]

    for mid, cfg in solutions:
        ms = missions[mid]
        b = evaluator.evaluate(cfg, ms)
        failed = [c for c in (b.compliance_checks + b.rule_checks) if c.status == CheckStatus.FAIL]
        assert not failed, f"Mission {mid} failed checks: {[(c.rule_id, c.message) for c in failed]}"
        if ms.geo_return_constraints:
            geo_checks = [c for c in b.compliance_checks if c.rule_id.startswith("RULE_GEORETURN_")]
            assert len(geo_checks) == len(ms.geo_return_constraints)
            assert all(c.status == CheckStatus.PASS for c in geo_checks)


def test_student_and_teacher_gui_offscreen():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtWidgets import QApplication
    from ssb.student_app.main_window import StudentMainWindow
    from ssb.teacher_app.main_window import TeacherMainWindow

    app = QApplication.instance() or QApplication([])
    win = StudentMainWindow()
    assert win.current_budgets is not None
    assert win.cmb_preset_missions.count() >= 6
    assert win.browser_payloads.list_suppliers.count() >= 19
    assert win.browser_platforms.list_suppliers.count() == 6

    # Verify each payload sub-category filter in the UI displays >= 4 suppliers (+ "Tous les fournisseurs")
    for idx in range(1, win.browser_payloads.cmb_type.count()):
        win.browser_payloads.cmb_type.setCurrentIndex(idx)
        assert win.browser_payloads.list_suppliers.count() >= 5, (
            f"Subcategory {win.browser_payloads.cmb_type.currentText()} should have at least 4 suppliers"
        )
    win.browser_payloads.cmb_type.setCurrentIndex(0)

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
