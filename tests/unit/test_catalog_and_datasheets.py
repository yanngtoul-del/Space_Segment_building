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
    assert len(db.equipments) >= 35
    assert len(db.launchers) >= 8

    plat_suppliers = db.suppliers_for("platform")
    assert len(plat_suppliers) >= 10
    major_suppliers = 0
    for sup in plat_suppliers:
        items = db.items_by_supplier(sup.id, "platform")
        assert len(items) >= 1, f"Supplier {sup.id} should have at least 1 platform"
        if len(items) >= 3:
            major_suppliers += 1
    assert major_suppliers >= 5
    assert len(db.platforms) >= 26

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
    assert len(mfiles) >= 10, f"Expected 10 missions, got {len(mfiles)}"

    missions: dict[str, MissionSpecification] = {}
    for mf in mfiles:
        ms = MissionSpecification.model_validate_json(mf.read_text(encoding="utf-8"))
        assert ms.max_budget_meur > 0
        assert len(ms.context) >= 50
        assert len(ms.primary_objective) >= 80
        assert len(ms.domain_label) >= 10
        assert len(ms.requirements) >= 4
        assert ms.image, f"Mission {ms.id} has no image defined"
        img_file = images_dir() / ms.image
        assert img_file.exists(), f"Mission image {ms.image} not found on disk for {ms.id}"
        # Verify every mission has explicit calibration and lifetime requirements matching header
        req_params = {r.parameter: r for r in ms.requirements}
        assert "radiometric_accuracy_pct" in req_params, f"Mission {ms.id} missing radiometric_accuracy_pct requirement"
        assert "design_lifetime_years" in req_params, f"Mission {ms.id} missing design_lifetime_years requirement"
        assert float(req_params["design_lifetime_years"].threshold) == ms.target_lifetime_years, (
            f"Mission {ms.id} lifetime mismatch: header {ms.target_lifetime_years} vs req {req_params['design_lifetime_years'].threshold}"
        )
        missions[ms.id] = ms

    # Reference valid student baseline solutions across all 10 missions,
    # satisfying mandatory thresholds, ground TVAC calibration, and ESA geographic return quotas:
    solutions = [
        # 1. Optical EO (budget 15.20 M€, GSD <= 0.88 m [Goal 0.70 m], swath >= 17 km, SNR >= 58, TVAC <= 2.0%)
        # Geo-return: France [35-60%], Italie [25-45%], Allemagne [8-25%]
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
                selected_calibration_ids=["calib_optical_tvac"],
                launcher_id="ln_rideshare_sso",
            ),
        ),
        # 2. SAR surveillance — Aegis Radar institutional SAR + CATR-TVAC qualification
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
                selected_calibration_ids=["calib_sar_catr_tvac"],
                launcher_id="ln_rideshare_sso",
            ),
        ),
        # 3. Atmosphere GHG — Coupled chain: Telescope [WideView-18] -> Slit [Athermal GHG] -> Spectrometer [TropoSonde-CH4] + Cryo-TVAC
        # Geo-return: France [30-60%], Allemagne [10-35%], Espagne [5-20%]
        (
            "EXAM-2026-ATMO-GHG",
            SystemConfiguration(
                orbit=OrbitDefinition(altitude_km=500.0, inclination_deg=97.4),
                platform_id="plat_sstl_mini150",
                selected_options=[
                    SelectedOption(slot_function="optical_interface", equipment_id="opt_slit_athermal_ghg"),
                    SelectedOption(slot_function="propulsion", equipment_id="prop_electric_hemp_de"),
                    SelectedOption(slot_function="ttc", equipment_id="ttc_xband_tmtc"),
                    SelectedOption(slot_function="mass_memory", equipment_id="mass_mem_1tb"),
                    SelectedOption(slot_function="adcs", equipment_id="adcs_high_accuracy_pack"),
                ],
                selected_payload_ids=["pl_opt_wide_swath_18cm", "pl_spec_atmo_tropo_ghg"],
                selected_calibration_ids=["calib_cryo_spectral_tvac"],
                launcher_id="ln_rideshare_sso",
            ),
        ),
        # 4a. Cosmology deep field — Single primary telescope STELLA-60 + Cryo-TVAC
        # Geo-return: Italie [40-65%], France [25-50%], Allemagne [4-20%]
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
                selected_calibration_ids=["calib_cryo_spectral_tvac"],
                launcher_id="ln_espa_heavy_rideshare",
            ),
        ),
        # 4b. Cosmology deep field — Dual payload coupled architecture (STELLA-60 + Slit + Lumina VNIR/SWIR spectrometer) + Cryo-TVAC
        (
            "EXAM-2026-COSMO",
            SystemConfiguration(
                orbit=OrbitDefinition(altitude_km=500.0, inclination_deg=97.4),
                platform_id="plat_astra_flex300",
                selected_options=[
                    SelectedOption(slot_function="optical_interface", equipment_id="opt_slit_wide_mapper"),
                    SelectedOption(slot_function="propulsion", equipment_id="prop_electric_hemp_de"),
                    SelectedOption(slot_function="ttc", equipment_id="ttc_sband_dual_redundant"),
                    SelectedOption(slot_function="payload_downlink", equipment_id="downlink_xband_tx"),
                    SelectedOption(slot_function="mass_memory", equipment_id="mass_mem_1tb_de"),
                    SelectedOption(slot_function="adcs", equipment_id="adcs_agile_wheels_medium"),
                ],
                selected_payload_ids=["pl_opt_stellara_60cm", "pl_spec_lumina_vnir_swir"],
                selected_calibration_ids=["calib_cryo_spectral_tvac"],
                launcher_id="ln_espa_heavy_rideshare",
            ),
        ),
        # 5. High throughput laser datalink — TeraLink Photonics (25 Gbps) + PAT-TVAC ESTEC
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
                selected_calibration_ids=["calib_laser_pat_tvac"],
                launcher_id="ln_rideshare_sso",
            ),
        ),
        # 6a. Low-cost CubeSat RF/IoT — Meridian RF Payloads + RF-TVAC
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
                selected_calibration_ids=["calib_rf_transponder_tvac"],
                launcher_id="ln_cubesat_deployer",
            ),
        ),
        # 6b. Low-cost CubeSat RF/IoT — Nordic NanoComm Systems (20 Mbps + Secondary Optical 6cm camera !) + RF-TVAC
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
                selected_calibration_ids=["calib_rf_transponder_tvac"],
                launcher_id="ln_cubesat_deployer",
            ),
        ),
        # 7. Light low-cost optical EO (budget 2.35 M€, GSD <= 2.80 m, swath >= 18 km, SNR >= 80, lifetime >= 3.0 yr)
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
                selected_calibration_ids=["calib_optical_tvac"],
                launcher_id="ln_cubesat_deployer",
            ),
        ),
        # 8. High-performance sub-metric optical EO (budget 33.5 M€, GSD <= 0.40 m, aperture >= 0.70 m, swath >= 13.8 km, TVAC <= 2.0%)
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
                selected_calibration_ids=["calib_optical_tvac"],
                launcher_id="ln_espa_heavy_rideshare",
            ),
        ),
        # 9. Classical GEO telecommunications (budget 46.0 M€, GEO 35,786 km, rate >= 700 Mbps, margin >= 8.0 dB, lifetime >= 15 yr, RF-TVAC)
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
                selected_calibration_ids=["calib_rf_transponder_tvac"],
                launcher_id="ln_gto_rideshare",
            ),
        ),
        # 10. Quantum Key Distribution QKD (budget 14.5 M€, SKR >= 20 kbps, QBER <= 2.0%, PAT-TVAC)
        (
            "EXAM-2026-QKD",
            SystemConfiguration(
                orbit=OrbitDefinition(altitude_km=500.0, inclination_deg=97.4),
                platform_id="plat_astra_flex150",
                selected_options=[
                    SelectedOption(slot_function="ttc", equipment_id="ttc_sband_gallia_fr"),
                    SelectedOption(slot_function="mass_memory", equipment_id="mass_mem_1tb_de"),
                    SelectedOption(slot_function="adcs", equipment_id="adcs_sodern_auriga_fr"),
                ],
                selected_payload_ids=["pl_qkd_edelweiss_entangled"],
                selected_calibration_ids=["calib_laser_pat_tvac"],
                launcher_id="ln_rideshare_sso",
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
            # N member state checks + 1 non-ESA ceiling check (RULE_GEORETURN_NON_ESA_CAP)
            assert len(geo_checks) == len(ms.geo_return_constraints) + 1
            assert all(c.status == CheckStatus.PASS for c in geo_checks)


def test_mission_architectural_dilemmas_and_non_conformities():
    """Verify that missions embed deliberate engineering dilemmas where attempting to satisfy
    aggressive Goals or alternative trade-offs triggers specific non-conformities (requiring student waivers)."""
    db = CatalogDatabase()
    db.load_from_directory(catalogs_dir())
    evaluator = SystemEvaluator(db)

    # Dilemma 1 (EXAM-2026-EO-OPT): Lowering altitude to 410 km with STELLA-35 achieves Goal GSD <= 0.70 m (0.70 m),
    # but violates REQ-OPT-SWATH (14.1 km < 17.0 km). Conversely, using EagleEye-45 at 500 km violates Budget & Geo-return.
    ms_eo = MissionSpecification.model_validate_json(
        (missions_dir() / "exam_optical_earth_observation.mission.json").read_text(encoding="utf-8")
    )
    cfg_eo_low_alt = SystemConfiguration(
        orbit=OrbitDefinition(altitude_km=405.0, inclination_deg=97.0),
        platform_id="plat_astra_flex150",
        selected_options=[
            SelectedOption(slot_function="propulsion", equipment_id="prop_electric_hemp_de"),
            SelectedOption(slot_function="ttc", equipment_id="ttc_sband_gallia_fr"),
            SelectedOption(slot_function="mass_memory", equipment_id="mass_mem_1tb_de"),
            SelectedOption(slot_function="adcs", equipment_id="adcs_sodern_auriga_fr"),
        ],
        selected_payload_ids=["pl_opt_stellara_35cm"],
        selected_calibration_ids=["calib_optical_tvac"],
        launcher_id="ln_rideshare_sso",
    )
    b_eo_low = evaluator.evaluate(cfg_eo_low_alt, ms_eo)
    eo_checks = {c.rule_id: c for c in b_eo_low.compliance_checks}
    assert eo_checks["REQ-OPT-GSD"].current_value <= 0.70  # Reaches the 0.70 m Goal!
    assert eo_checks["REQ-OPT-SWATH"].status == CheckStatus.FAIL  # Fails Swath >= 17 km (Waiver required)

    # Dilemma 2 (EXAM-2026-ATMO-GHG): Coupling STELLA-20 (f=1.80 m) instead of WideView-18 (f=0.90 m)
    # reaches the spatial resolution Goal <= 3.50 m (GSD = 3.33 m), but fails Swath >= 9.5 km (5.0 km) and SNR >= 70 (25.5).
    ms_ghg = MissionSpecification.model_validate_json(
        (missions_dir() / "exam_atmosphere_greenhouse_gas.mission.json").read_text(encoding="utf-8")
    )
    cfg_ghg_high_gsd = SystemConfiguration(
        orbit=OrbitDefinition(altitude_km=500.0, inclination_deg=97.4),
        platform_id="plat_sstl_mini150",
        selected_options=[
            SelectedOption(slot_function="optical_interface", equipment_id="opt_slit_athermal_ghg"),
            SelectedOption(slot_function="propulsion", equipment_id="prop_electric_hemp_de"),
            SelectedOption(slot_function="ttc", equipment_id="ttc_xband_tmtc"),
            SelectedOption(slot_function="mass_memory", equipment_id="mass_mem_1tb"),
            SelectedOption(slot_function="adcs", equipment_id="adcs_high_accuracy_pack"),
        ],
        selected_payload_ids=["pl_opt_stellara_20cm", "pl_spec_atmo_tropo_ghg"],
        selected_calibration_ids=["calib_cryo_spectral_tvac"],
        launcher_id="ln_rideshare_sso",
    )
    b_ghg_hi = evaluator.evaluate(cfg_ghg_high_gsd, ms_ghg)
    ghg_checks = {c.rule_id: c for c in b_ghg_hi.compliance_checks}
    assert ghg_checks["REQ-ATMO-GSD"].current_value <= 3.50  # Reaches the 3.50 m Goal!
    assert ghg_checks["REQ-ATMO-SWATH"].status == CheckStatus.FAIL  # Fails Swath >= 9.5 km
    assert ghg_checks["REQ-ATMO-SNR"].status == CheckStatus.FAIL  # Fails SNR >= 70

    # Dilemma 3 (EXAM-2026-SAR): Choosing CompactSAR-X achieves the Stripmap Azimuth Goal <= 1.30 m (1.25 m),
    # but fails NESZ <= -21.0 dB (-2.1 dB).
    ms_sar = MissionSpecification.model_validate_json(
        (missions_dir() / "exam_sar_surveillance.mission.json").read_text(encoding="utf-8")
    )
    cfg_sar_compact = SystemConfiguration(
        orbit=OrbitDefinition(altitude_km=500.0, inclination_deg=97.4),
        platform_id="plat_astra_flex300",
        selected_options=[
            SelectedOption(slot_function="ttc", equipment_id="ttc_sband_aurora_it"),
            SelectedOption(slot_function="payload_downlink", equipment_id="downlink_xband_milan_it"),
        ],
        selected_payload_ids=["pl_sar_xband_compact"],
        selected_calibration_ids=["calib_sar_catr_tvac"],
        launcher_id="ln_rideshare_sso",
    )
    b_sar_comp = evaluator.evaluate(cfg_sar_compact, ms_sar)
    sar_checks = {c.rule_id: c for c in b_sar_comp.compliance_checks}
    assert sar_checks["REQ-SAR-AZ-01"].current_value <= 1.30  # Reaches Azimuth Goal <= 1.30 m!
    assert sar_checks["REQ-SAR-NESZ-01"].status == CheckStatus.FAIL  # Fails NESZ <= -21 dB


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
    assert win.browser_platforms.list_suppliers.count() >= 11

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
        assert win.mission_sheet_view.lbl_image.pixmap() is not None
        assert not win.mission_sheet_view.lbl_image.pixmap().isNull()

    win.browser_payloads.list_suppliers.setCurrentRow(1)
    assert win.browser_payloads.list_items.count() >= 1

    second_pl = win.catalog.payloads["pl_opt_comm_terminal_10g"]
    win._add_payload_from_browser(second_pl)
    assert len(win.project.configuration.selected_payload_ids) == 2

    # Verify the selection highlight boxes across all tabs
    assert win.box_selected_platform is not None
    assert win.box_active_equipments is not None
    assert win.box_selected_launcher is not None
    assert win.global_arch_widget is not None
    assert win.global_arch_widget.table.rowCount() >= 3
    assert win.t_active_equipments.rowCount() >= 1

    # Verify Tab 5: double-clicking an equipment in the catalog adds/equips it onto the platform
    win.tabs.setCurrentIndex(4)
    eq = win.catalog.equipments["prop_electric_hemp_de"]
    win.browser_equipments.item_activated.emit(eq)
    app.processEvents()
    active_ids = [opt.equipment_id for opt in win.project.configuration.selected_options]
    assert "prop_electric_hemp_de" in active_ids
    assert win.t_active_equipments.rowCount() >= 2

    # Verify Tab 3: basket box buttons remain fixed and within the visible box bounds
    basket_box = win.list_selected_payloads.parentWidget()
    btn_col_box = basket_box.layout().itemAt(1).widget()
    assert btn_col_box.width() == 240
    assert btn_col_box.x() + btn_col_box.width() <= basket_box.width()

    # Verify Global Architecture modal dialog creation
    from ssb.ui_common.global_architecture_view import GlobalArchitectureDialog
    dlg = GlobalArchitectureDialog(win.catalog, win.project, win.current_budgets, win)
    assert dlg.widget.table.rowCount() >= 3
    dlg.close()

    twin = TeacherMainWindow()
    assert twin.tabs.count() == 3
    assert twin.cmb_existing_missions.count() >= 11
    assert twin.global_arch_widget is not None
    twin.cmb_existing_missions.setCurrentIndex(1)
    rebuilt_ms = twin._build_current_mission_spec()
    assert rebuilt_ms.image != ""
    assert len(rebuilt_ms.geo_return_constraints) >= 2
    win.close()
    twin.close()
    assert app is not None


def test_geo_return_non_esa_spending_flexibility():
    """Verify that ESA missions allow up to 15% non-European procurement (COTS / US / CA / JP),
    and reject configurations exceeding this 15% ceiling."""
    db = CatalogDatabase()
    db.load_from_directory(catalogs_dir())
    evaluator = SystemEvaluator(db)

    ms = MissionSpecification.model_validate_json(
        (missions_dir() / "exam_optical_earth_observation.mission.json").read_text(encoding="utf-8")
    )
    assert ms.max_non_esa_spend_pct == 15.0

    # Baseline configuration (100% European): France ~47%, Italie ~40.5%, Allemagne ~12.5%
    orbit = OrbitDefinition(altitude_km=500.0, inclination_deg=97.4)
    cfg_eu = SystemConfiguration(
        orbit=orbit,
        platform_id="plat_astra_flex150",  # France (3.80 M€)
        selected_options=[
            SelectedOption(slot_function="propulsion", equipment_id="prop_electric_hemp_de"),  # Allemagne (0.75 M€)
            SelectedOption(slot_function="ttc", equipment_id="ttc_sband_gallia_fr"),  # France (0.42 M€)
            SelectedOption(slot_function="mass_memory", equipment_id="mass_mem_1tb_de"),  # Allemagne (0.55 M€)
            SelectedOption(slot_function="adcs", equipment_id="adcs_sodern_auriga_fr"),  # France (0.65 M€)
        ],
        selected_payload_ids=["pl_opt_stellara_35cm"],  # Italie (4.20 M€)
        launcher_id="ln_rideshare_sso",
    )
    b_eu = evaluator.evaluate(cfg_eu, ms)
    non_esa_check_eu = next(c for c in b_eu.compliance_checks if c.rule_id == "RULE_GEORETURN_NON_ESA_CAP")
    assert non_esa_check_eu.status == CheckStatus.PASS
    assert non_esa_check_eu.current_value == 0.0

    # Non-European procurement test (e.g. US platform apex_pro500 ~5.2 M€ out of ~11.7 M€ = 44% > 15%)
    cfg_non_esa_exceeded = SystemConfiguration(
        orbit=orbit,
        platform_id="plat_apex_pro500",  # États-Unis (5.20 M€)
        selected_options=[
            SelectedOption(slot_function="propulsion", equipment_id="prop_electric_hemp_de"),
            SelectedOption(slot_function="ttc", equipment_id="ttc_sband_gallia_fr"),
            SelectedOption(slot_function="mass_memory", equipment_id="mass_mem_1tb_de"),
            SelectedOption(slot_function="adcs", equipment_id="adcs_sodern_auriga_fr"),
        ],
        selected_payload_ids=["pl_opt_stellara_35cm"],
        launcher_id="ln_rideshare_sso",
    )
    b_excess = evaluator.evaluate(cfg_non_esa_exceeded, ms)
    non_esa_check_excess = next(c for c in b_excess.compliance_checks if c.rule_id == "RULE_GEORETURN_NON_ESA_CAP")
    assert non_esa_check_excess.status == CheckStatus.FAIL
    assert non_esa_check_excess.current_value > 15.0


def test_spectrometer_telescope_slit_chain_coupling():
    """Verify pedagogical optical telescope + spectrometer slit interface chain validation:
    - Complete chain (Telescope + Slit option + Spectrometer): PASS with computed GSD and SNR.
    - Missing telescope: FAIL (RULE_SPECTRO_MISSING_TELESCOPE).
    - Missing slit interface: FAIL (RULE_SPECTRO_MISSING_SLIT).
    """
    db = CatalogDatabase()
    db.load_from_directory(catalogs_dir())
    evaluator = SystemEvaluator(db)

    ms = MissionSpecification.model_validate_json(
        (missions_dir() / "exam_atmosphere_greenhouse_gas.mission.json").read_text(encoding="utf-8")
    )
    orbit = OrbitDefinition(altitude_km=500.0, inclination_deg=97.4)

    # 1. Complete chain: WideView-18 (D=0.18 m, f=0.90 m) + Slit + TropoSonde-CH4
    cfg_complete = SystemConfiguration(
        orbit=orbit,
        platform_id="plat_sstl_mini150",
        selected_options=[
            SelectedOption(slot_function="optical_interface", equipment_id="opt_slit_athermal_ghg"),
            SelectedOption(slot_function="propulsion", equipment_id="prop_electric_hemp_de"),
            SelectedOption(slot_function="ttc", equipment_id="ttc_xband_tmtc"),
            SelectedOption(slot_function="mass_memory", equipment_id="mass_mem_1tb"),
            SelectedOption(slot_function="adcs", equipment_id="adcs_high_accuracy_pack"),
        ],
        selected_payload_ids=["pl_opt_wide_swath_18cm", "pl_spec_atmo_tropo_ghg"],
        launcher_id="ln_rideshare_sso",
    )
    b_comp = evaluator.evaluate(cfg_complete, ms)
    rule_chain_ok = next((c for c in b_comp.compliance_checks if c.rule_id == "RULE_SPECTRO_CHAIN_OK"), None)
    assert rule_chain_ok is not None
    assert rule_chain_ok.status == CheckStatus.PASS
    spec_perf = b_comp.payload_performances.get("pl_spec_atmo_tropo_ghg", {})
    assert spec_perf.get("gsd_spatial_nadir_m", 0.0) == 6.67
    assert spec_perf.get("mean_snr_estimate", 0.0) > 50.0

    # 2. Missing telescope (only spectrometer + slit)
    cfg_no_tel = SystemConfiguration(
        orbit=orbit,
        platform_id="plat_sstl_mini150",
        selected_options=[
            SelectedOption(slot_function="optical_interface", equipment_id="opt_slit_athermal_ghg"),
            SelectedOption(slot_function="ttc", equipment_id="ttc_xband_tmtc"),
            SelectedOption(slot_function="mass_memory", equipment_id="mass_mem_1tb"),
        ],
        selected_payload_ids=["pl_spec_atmo_tropo_ghg"],
        launcher_id="ln_rideshare_sso",
    )
    b_no_tel = evaluator.evaluate(cfg_no_tel, ms)
    rule_no_tel = next((c for c in b_no_tel.compliance_checks if c.rule_id == "RULE_SPECTRO_MISSING_TELESCOPE"), None)
    assert rule_no_tel is not None
    assert rule_no_tel.status == CheckStatus.FAIL
    spec_perf_no_tel = b_no_tel.payload_performances.get("pl_spec_atmo_tropo_ghg", {})
    assert spec_perf_no_tel.get("gsd_spatial_nadir_m", 0.0) == 0.0

    # 3. Missing slit interface (telescope + spectrometer, but no optical_interface slot option selected)
    cfg_no_slit = SystemConfiguration(
        orbit=orbit,
        platform_id="plat_sstl_mini150",
        selected_options=[
            SelectedOption(slot_function="ttc", equipment_id="ttc_xband_tmtc"),
            SelectedOption(slot_function="mass_memory", equipment_id="mass_mem_1tb"),
        ],
        selected_payload_ids=["pl_opt_wide_swath_18cm", "pl_spec_atmo_tropo_ghg"],
        launcher_id="ln_rideshare_sso",
    )
    b_no_slit = evaluator.evaluate(cfg_no_slit, ms)
    rule_no_slit = next((c for c in b_no_slit.compliance_checks if c.rule_id == "RULE_SPECTRO_MISSING_SLIT"), None)
    assert rule_no_slit is not None
    assert rule_no_slit.status == CheckStatus.FAIL
    spec_perf_no_slit = b_no_slit.payload_performances.get("pl_spec_atmo_tropo_ghg", {})
    assert spec_perf_no_slit.get("gsd_spatial_nadir_m", 0.0) == 0.0


def test_calibration_catalog_and_datasheets():
    db = CatalogDatabase()
    db.load_from_directory()
    assert len(db.calibrations) >= 6

    # Verify supplier association
    calib_suppliers = db.suppliers_for("calibration")
    sup_ids = {s.id for s in calib_suppliers}
    assert "cso_intespace_fr" in sup_ids
    assert "iabg_test_centre_de" in sup_ids
    assert "csl_liege_be" in sup_ids
    assert "estec_test_centre_nl" in sup_ids

    # Verify TVAC vs Ambient calibration entries
    tvac_opt = db.calibrations["calib_optical_tvac"]
    assert tvac_opt.is_tvac is True
    assert tvac_opt.is_thermal_vacuum is True
    assert tvac_opt.cost_meur == 0.48
    assert tvac_opt.duration_weeks == 4.0
    assert "optical_imager" in tvac_opt.compatible_payload_types

    amb = db.calibrations["calib_cleanroom_std"]
    assert amb.is_tvac is False
    assert amb.cost_meur == 0.12

    # Verify datasheet building
    from ssb.catalog.datasheet import build_datasheet
    ds_tvac = build_datasheet(tvac_opt)
    assert "Vide Thermique" in ds_tvac.category_label
    assert ds_tvac.item_id == "calib_optical_tvac"
    assert len(ds_tvac.sections) >= 3

    ds_amb = build_datasheet(amb)
    assert "ISO 5" in ds_amb.category_label


def test_calibration_system_evaluation_and_rules():
    from pathlib import Path
    db = CatalogDatabase()
    db.load_from_directory()
    evaluator = SystemEvaluator(db)
    ms = MissionSpecification.model_validate_json(
        (missions_dir() / "exam_optical_earth_observation.mission.json").read_text(encoding="utf-8")
    )
    orbit = OrbitDefinition(altitude_km=500.0, inclination_deg=97.4)

    # 1. Config with NO calibration selected -> triggers RULE_CALIB_NONE
    cfg_no_calib = SystemConfiguration(
        orbit=orbit,
        platform_id="plat_apex_pro500",
        selected_payload_ids=["pl_opt_submeter_highres"],
        selected_calibration_ids=[],
        launcher_id="ln_rideshare_sso",
    )
    b0 = evaluator.evaluate(cfg_no_calib, ms)
    assert b0.cost.calibration_total_meur == 0.0
    r_none = next((c for c in b0.rule_checks if c.rule_id == "RULE_CALIB_NONE"), None)
    assert r_none is not None
    assert r_none.status == CheckStatus.WARNING

    # 2. Config with Ambient cleanroom calibration only -> RULE_CALIB_SELECTED PASS, RULE_CALIB_TVAC_QUALIFIED WARNING
    cfg_amb = SystemConfiguration(
        orbit=orbit,
        platform_id="plat_apex_pro500",
        selected_payload_ids=["pl_opt_submeter_highres"],
        selected_calibration_ids=["calib_cleanroom_std"],
        launcher_id="ln_rideshare_sso",
    )
    b_amb = evaluator.evaluate(cfg_amb, ms)
    assert b_amb.cost.calibration_total_meur == 0.12
    r_sel = next((c for c in b_amb.rule_checks if c.rule_id == "RULE_CALIB_SELECTED"), None)
    assert r_sel is not None and r_sel.status == CheckStatus.PASS
    r_tvac_warn = next((c for c in b_amb.rule_checks if c.rule_id == "RULE_CALIB_TVAC_QUALIFIED"), None)
    assert r_tvac_warn is not None and r_tvac_warn.status == CheckStatus.WARNING

    # 3. Config with TVAC calibration -> RULE_CALIB_TVAC_QUALIFIED PASS + geo return contribution
    cfg_tvac = SystemConfiguration(
        orbit=orbit,
        platform_id="plat_apex_pro500",
        selected_payload_ids=["pl_opt_submeter_highres"],
        selected_calibration_ids=["calib_optical_tvac"],
        launcher_id="ln_rideshare_sso",
    )
    b_tvac = evaluator.evaluate(cfg_tvac, ms)
    assert b_tvac.cost.calibration_total_meur == 0.48
    r_tvac_pass = next((c for c in b_tvac.rule_checks if c.rule_id == "RULE_CALIB_TVAC_QUALIFIED"), None)
    assert r_tvac_pass is not None and r_tvac_pass.status == CheckStatus.PASS
    # Intespace Toulouse is in France -> cost included in France geo return
    assert "France" in b_tvac.cost.cost_by_country_meur
    assert b_tvac.cost.cost_by_country_meur["France"] >= 0.48


def test_calibration_gui_integration_offscreen():
    import os
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtWidgets import QApplication
    from ssb.student_app.main_window import StudentMainWindow

    app = QApplication.instance() or QApplication([])
    win = StudentMainWindow()

    # 9 Tabs total
    assert win.tabs.count() == 9
    assert "Calibration & Essais Sol (TVAC)" in win.tabs.tabText(5)
    assert "Lanceurs" in win.tabs.tabText(6)
    assert "Analyses" in win.tabs.tabText(7)
    assert "Rapport" in win.tabs.tabText(8)

    # Verify Tab 6: Calibration selection
    win.tabs.setCurrentIndex(5)
    cal = win.catalog.calibrations["calib_optical_tvac"]
    win.browser_calibrations.item_activated.emit(cal)
    app.processEvents()

    assert "calib_optical_tvac" in win.project.configuration.selected_calibration_ids
    assert win.t_active_calibrations.rowCount() == 1
    assert win.current_budgets.cost.calibration_total_meur == 0.48

    # Verify Global Architecture Table reflects the calibration row
    arch_calib_rows = [
        row for row in range(win.global_arch_widget.table.rowCount())
        if "Calibration" in win.global_arch_widget.table.item(row, 0).text()
    ]
    assert len(arch_calib_rows) == 1

    # Verify clearing calibrations
    win._clear_calibrations()
    app.processEvents()
    assert len(win.project.configuration.selected_calibration_ids) == 0
    assert win.t_active_calibrations.rowCount() == 0
    assert win.current_budgets.cost.calibration_total_meur == 0.0
    win.close()
