"""Main interactive PySide6 graphical user interface for students."""

import sys
from pathlib import Path
from typing import Any
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QTabWidget,
    QLabel,
    QPushButton,
    QComboBox,
    QDoubleSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QTextEdit,
    QFileDialog,
    QMessageBox,
    QGroupBox,
    QFormLayout,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
)
from PySide6.QtCore import Qt

from ssb.catalog.database import CatalogDatabase
from ssb.catalog.datasheet import PAYLOAD_TYPE_LABELS_FR, FUNCTION_LABELS_FR
from ssb.core.paths import catalogs_dir, missions_dir
from ssb.core.orbit import OrbitDefinition, OrbitType
from ssb.core.mission import (
    MissionSpecification,
    MissionRequirement,
    RequirementType,
    RequirementOperator,
    GroundStationTarget,
)
from ssb.core.platform import PlatformBase
from ssb.core.payload import BasePayload
from ssb.core.project import StudentProject, SystemConfiguration, Launcher
from ssb.system.evaluator import SystemEvaluator, CheckStatus, SystemBudgets, launcher_capacity_for_orbit
from ssb.orbit.propagator import OrbitPropagator
from ssb.report.generator import ReportGenerator
from ssb.ui_common.catalog_browser import CatalogBrowser
from ssb.ui_common.platform_slots_widget import PlatformSlotsWidget
from ssb.ui_common.mission_sheet_view import MissionSheetView


class StudentMainWindow(QMainWindow):
    """Main desktop interface for students taking the satellite design exam."""

    def __init__(self, catalog_dir: Path | str | None = None) -> None:
        super().__init__()
        self.setWindowTitle("Space Segment Builder — Examen d'Architecture de Segment Spatial")
        self.resize(1380, 860)

        self.catalog = CatalogDatabase()
        self.catalog.load_from_directory(catalog_dir or catalogs_dir())
        self.evaluator = SystemEvaluator(self.catalog)

        self.mission = self._create_default_exam_mission()
        self.project = StudentProject(
            project_id="EXAM-2026-001",
            student_name="Étudiant",
            student_id="ETU-001",
            mission=self.mission,
            configuration=SystemConfiguration(
                orbit=OrbitDefinition(altitude_km=500.0, inclination_deg=97.4),
                platform_id="plat_astra_flex150",
                selected_payload_ids=["pl_opt_submeter_highres"],
                launcher_id="ln_rideshare_sso",
            ),
        )
        self.current_budgets: SystemBudgets | None = None

        self._setup_ui()
        default_plat = self.catalog.platforms[self.project.configuration.platform_id]
        self.slots_widget.set_platform(default_plat)
        self._refresh_selected_payloads_list()
        self.refresh_evaluation()

    def _create_default_exam_mission(self) -> MissionSpecification:
        default_file = missions_dir() / "exam_optical_earth_observation.mission.json"
        if default_file.exists():
            try:
                return MissionSpecification.model_validate_json(default_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        return MissionSpecification(
            id="EXAM-2026-EO-OPT",
            title="Mission Sentinel-Vision — Observation de la Terre Haute Résolution",
            client_agency="Agence Européenne d'Observation Civile & Sécurité (AEOCS)",
            domain_label="Observation de la Terre — Imagerie optique sub-métrique",
            context="Concevoir un satellite d'observation de la Terre basse orbite haute résolution pour le suivi des infrastructures critiques.",
            primary_objective="Fournir des images optiques avec un GSD <= 1,0 m et une fauchée >= 10 km sous un budget total de 18,0 M€.",
            mission_type="optical_eo",
            max_budget_meur=18.0,
            target_lifetime_years=5.0,
            requirements=[
                MissionRequirement(
                    id="REQ-GSD-01",
                    title="Résolution spatiale nadir (GSD)",
                    description="Résolution au sol GSD <= 1.0 m",
                    req_type=RequirementType.PAYLOAD_PERF,
                    parameter="gsd_nadir_m",
                    operator=RequirementOperator.LE,
                    threshold=1.0,
                    unit="m",
                ),
                MissionRequirement(
                    id="REQ-SWATH-01",
                    title="Largeur de fauchée",
                    description="Fauchée cross-track >= 10.0 km",
                    req_type=RequirementType.PAYLOAD_PERF,
                    parameter="swath_width_km",
                    operator=RequirementOperator.GE,
                    threshold=10.0,
                    unit="km",
                ),
            ],
            ground_stations=[
                GroundStationTarget(
                    id="svalbard",
                    name="Svalbard Station",
                    latitude_deg=78.22,
                    longitude_deg=15.40,
                    min_elevation_deg=5.0,
                )
            ],
        )

    def _current_orbit(self) -> OrbitDefinition:
        alt = self.spin_altitude.value()
        if self.combo_orbit_type.currentIndex() == 0:
            try:
                inc = OrbitDefinition.compute_sso_inclination(alt)
            except Exception:
                inc = 97.4
            otype = OrbitType.SSO
        else:
            inc = self.spin_inclination.value()
            otype = OrbitType.CIRCULAR
        return OrbitDefinition(orbit_type=otype, altitude_km=alt, inclination_deg=inc)

    def _setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(8, 8, 8, 8)

        # ---- Top status & action bar
        banner = QHBoxLayout()
        self.lbl_mission_title = QLabel()
        self.lbl_mission_title.setStyleSheet("font-size: 13px;")
        banner.addWidget(self.lbl_mission_title, stretch=1)

        self.lbl_live_summary = QLabel()
        self.lbl_live_summary.setStyleSheet(
            "background: #0f2744; color: #f8fafc; padding: 5px 10px; border-radius: 4px; font-weight: bold;"
        )
        banner.addWidget(self.lbl_live_summary)

        btn_open_proj = QPushButton("Ouvrir Projet (.json)")
        btn_open_proj.clicked.connect(self.open_project_json)
        banner.addWidget(btn_open_proj)

        btn_save_proj = QPushButton("Enregistrer Projet (.json)")
        btn_save_proj.setStyleSheet("background-color: #0f766e; color: white; font-weight: bold; padding: 5px 10px;")
        btn_save_proj.clicked.connect(self.save_project_json)
        banner.addWidget(btn_save_proj)

        self.btn_export_report = QPushButton("Générer Rapport Word (.docx)")
        self.btn_export_report.setStyleSheet("background-color: #1a5276; color: white; font-weight: bold; padding: 5px 12px;")
        self.btn_export_report.clicked.connect(self.export_docx_report)
        banner.addWidget(self.btn_export_report)
        main_layout.addLayout(banner)

        # ---- Main workflow tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs, stretch=1)

        self._build_tab_mission()
        self._build_tab_orbit()
        self._build_tab_payloads()
        self._build_tab_platform()
        self._build_tab_equipment_catalog()
        self._build_tab_launcher()
        self._build_tab_evaluation()
        self._build_tab_report_text()

        self._sync_legacy_combos()

    # ------------------------------------------------------------------ Tab 1: Mission Specification Sheet
    def _build_tab_mission(self) -> None:
        tab = QWidget()
        l = QVBoxLayout(tab)

        top_row = QHBoxLayout()
        top_row.addWidget(QLabel("<b>Fiche de spécification mission :</b>"))
        self.cmb_preset_missions = QComboBox()
        mdir = missions_dir()
        added_files = 0
        if mdir.exists():
            for mf in sorted(mdir.glob("*.mission.json")):
                try:
                    ms = MissionSpecification.model_validate_json(mf.read_text(encoding="utf-8"))
                    dom = ms.domain_label or ms.mission_type
                    self.cmb_preset_missions.addItem(
                        f"[{ms.id}] {ms.title} — {dom} (Budget plafond : {ms.max_budget_meur:.1f} M€)",
                        str(mf),
                    )
                    added_files += 1
                except Exception:
                    pass
        if added_files == 0:
            self.cmb_preset_missions.addItem(
                f"[{self.mission.id}] {self.mission.title} (Budget plafond : {self.mission.max_budget_meur:.1f} M€)",
                "__DEFAULT__",
            )
        self.cmb_preset_missions.currentIndexChanged.connect(self._on_preset_mission_selected)
        top_row.addWidget(self.cmb_preset_missions, stretch=1)

        btn_load_m = QPushButton("Importer une autre fiche mission (.mission.json)...")
        btn_load_m.clicked.connect(self._browse_mission_file)
        top_row.addWidget(btn_load_m)
        l.addLayout(top_row)

        stu_box = QGroupBox("Identification de l'étudiant")
        stu_form = QHBoxLayout(stu_box)
        stu_form.addWidget(QLabel("Nom & Prénom :"))
        self.ed_student_name = QLineEdit(self.project.student_name)
        stu_form.addWidget(self.ed_student_name)
        stu_form.addWidget(QLabel("Numéro étudiant :"))
        self.ed_student_id = QLineEdit(self.project.student_id)
        stu_form.addWidget(self.ed_student_id)
        stu_form.addWidget(QLabel("ID Projet :"))
        self.ed_project_id = QLineEdit(self.project.project_id)
        stu_form.addWidget(self.ed_project_id)
        l.addWidget(stu_box)

        self.mission_sheet_view = MissionSheetView()
        self.t_mission_reqs = self.mission_sheet_view.t_reqs
        l.addWidget(self.mission_sheet_view, stretch=1)

        self._populate_mission_view()
        self.tabs.addTab(tab, "1. Fiche de Spécification Mission")

    def _populate_mission_view(self) -> None:
        self.mission_sheet_view.set_mission(self.mission)

    def _on_preset_mission_selected(self) -> None:
        data = self.cmb_preset_missions.currentData()
        if not data or data == "__DEFAULT__":
            self.mission = self._create_default_exam_mission()
        else:
            self.mission = MissionSpecification.model_validate_json(Path(data).read_text(encoding="utf-8"))
        self.project.mission = self.mission
        self._populate_mission_view()
        self.refresh_evaluation()

    def _browse_mission_file(self) -> None:
        fp, _ = QFileDialog.getOpenFileName(self, "Charger une fiche mission", str(missions_dir()), "Mission JSON (*.json)")
        if fp:
            self.mission = MissionSpecification.model_validate_json(Path(fp).read_text(encoding="utf-8"))
            self.project.mission = self.mission
            self._populate_mission_view()
            self.refresh_evaluation()

    # ------------------------------------------------------------------ Tab 2: Orbit
    def _build_tab_orbit(self) -> None:
        tab = QWidget()
        l = QVBoxLayout(tab)
        grp = QGroupBox("Paramètres orbitaux (propagation séculaire J2)")
        form = QFormLayout(grp)

        self.combo_orbit_type = QComboBox()
        self.combo_orbit_type.addItems(["SSO — Héliosynchrone (inclinaison calculée via J2)", "Orbite circulaire à inclinaison libre"])
        self.combo_orbit_type.currentIndexChanged.connect(self._on_orbit_changed)
        form.addRow("Type d'orbite :", self.combo_orbit_type)

        self.spin_altitude = QDoubleSpinBox()
        self.spin_altitude.setRange(250.0, 1800.0)
        self.spin_altitude.setSingleStep(25.0)
        self.spin_altitude.setValue(500.0)
        self.spin_altitude.setSuffix(" km")
        self.spin_altitude.valueChanged.connect(self._on_orbit_changed)
        form.addRow("Altitude orbitale :", self.spin_altitude)

        self.spin_inclination = QDoubleSpinBox()
        self.spin_inclination.setRange(0.0, 180.0)
        self.spin_inclination.setValue(97.4)
        self.spin_inclination.setSuffix(" °")
        self.spin_inclination.setEnabled(False)
        self.spin_inclination.valueChanged.connect(self._on_orbit_changed)
        form.addRow("Inclinaison :", self.spin_inclination)

        self.lbl_inclination = QLabel("97.40 ° (SSO J2)")
        form.addRow("Synthèse orbitale :", self.lbl_inclination)
        l.addWidget(grp)

        self.lbl_orbit_details = QLabel()
        self.lbl_orbit_details.setWordWrap(True)
        self.lbl_orbit_details.setStyleSheet(
            "background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 5px; padding: 10px; font-size: 12px;"
        )
        l.addWidget(self.lbl_orbit_details)
        l.addStretch(1)
        self.tabs.addTab(tab, "2. Orbite")

    def _on_orbit_changed(self) -> None:
        alt = self.spin_altitude.value()
        is_sso = self.combo_orbit_type.currentIndex() == 0
        self.spin_inclination.setEnabled(not is_sso)
        if is_sso:
            try:
                inc = OrbitDefinition.compute_sso_inclination(alt)
                self.spin_inclination.blockSignals(True)
                self.spin_inclination.setValue(inc)
                self.spin_inclination.blockSignals(False)
                self.lbl_inclination.setText(f"{inc:.2f} ° (calculée automatiquement pour précession SSO J2)")
            except Exception:
                self.lbl_inclination.setText("Orbite SSO impossible à cette altitude")
        else:
            self.lbl_inclination.setText(f"{self.spin_inclination.value():.2f} ° (inclinaison libre)")

        orb = self._current_orbit()
        self.lbl_orbit_details.setText(
            f"<b>Demi-grand axe :</b> {orb.semi_major_axis_km:.1f} km   |   "
            f"<b>Période orbitale :</b> {orb.period_minutes:.1f} min ({orb.revolutions_per_day:.2f} orb/jour)<br>"
            "<i>Note : l'altitude influe directement sur la résolution au sol (GSD), la fauchée, le bilan de liaison RF/optique, "
            "le NESZ radar et la capacité du lanceur.</i>"
        )
        self.browser_payloads.refresh()
        self.browser_launchers.refresh()
        self.refresh_evaluation()

    # ------------------------------------------------------------------ Tab 3: Payloads
    def _build_tab_payloads(self) -> None:
        tab = QWidget()
        l = QVBoxLayout(tab)

        basket_box = QGroupBox("Charges utiles embarquées sur le satellite (sélection multiple possible)")
        bl = QHBoxLayout(basket_box)
        self.list_selected_payloads = QListWidget()
        self.list_selected_payloads.setMaximumHeight(95)
        self.list_selected_payloads.currentItemChanged.connect(self._on_basket_payload_clicked)
        bl.addWidget(self.list_selected_payloads, stretch=1)

        btn_col = QVBoxLayout()
        btn_remove_pl = QPushButton("Retirer la charge utile sélectionnée")
        btn_remove_pl.clicked.connect(self._remove_selected_payload)
        btn_clear_pl = QPushButton("Tout vider")
        btn_clear_pl.clicked.connect(self._clear_payloads)
        btn_col.addWidget(btn_remove_pl)
        btn_col.addWidget(btn_clear_pl)
        bl.addLayout(btn_col)
        l.addWidget(basket_box)

        type_opts = [(k, v) for k, v in PAYLOAD_TYPE_LABELS_FR.items()]
        self.browser_payloads = CatalogBrowser(
            catalog=self.catalog,
            category="payload",
            action_button_text="＋ Ajouter cette charge utile au satellite",
            type_filter_options=type_opts,
            compatibility_fn=self._check_payload_compat,
            orbit_provider=self._current_orbit,
        )
        self.browser_payloads.item_activated.connect(self._add_payload_from_browser)
        l.addWidget(self.browser_payloads, stretch=1)

        self.tabs.addTab(tab, f"3. Charges Utiles ({len(self.catalog.payloads)} réf.)")

    def _check_payload_compat(self, pl: BasePayload) -> tuple[bool, str]:
        plat_id = self.project.configuration.platform_id
        if not plat_id or plat_id not in self.catalog.platforms:
            return True, "Aucune plateforme choisie"
        plat = self.catalog.platforms[plat_id]
        issues = []
        if pl.mass_kg > plat.max_payload_mass_kg:
            issues.append(f"masse {pl.mass_kg:.0f}>{plat.max_payload_mass_kg:.0f} kg")
        if pl.volume_liters > plat.payload_volume_liters:
            issues.append(f"vol. {pl.volume_liters:.0f}>{plat.payload_volume_liters:.0f} L")
        if pl.operational_power_w * 0.25 > plat.payload_avg_power_w:
            issues.append("puissance moy. élevée")
        if issues:
            return False, f"Sur {plat.name} : " + ", ".join(issues)
        return True, f"Compatible avec {plat.name}"

    def _add_payload_from_browser(self, pl: BasePayload) -> None:
        self.project.configuration.selected_payload_ids.append(pl.id)
        self._refresh_selected_payloads_list()
        self.browser_platforms.refresh()
        self.refresh_evaluation()

    def _remove_selected_payload(self) -> None:
        row = self.list_selected_payloads.currentRow()
        if 0 <= row < len(self.project.configuration.selected_payload_ids):
            self.project.configuration.selected_payload_ids.pop(row)
            self._refresh_selected_payloads_list()
            self.browser_platforms.refresh()
            self.refresh_evaluation()

    def _clear_payloads(self) -> None:
        self.project.configuration.selected_payload_ids.clear()
        self._refresh_selected_payloads_list()
        self.browser_platforms.refresh()
        self.refresh_evaluation()

    def _on_basket_payload_clicked(self, current: QListWidgetItem | None, _prev: QListWidgetItem | None) -> None:
        if current:
            pid = current.data(Qt.ItemDataRole.UserRole)
            if pid:
                self.browser_payloads.select_item_by_id(pid)

    def _refresh_selected_payloads_list(self) -> None:
        self.list_selected_payloads.clear()
        for pid in self.project.configuration.selected_payload_ids:
            pl = self.catalog.payloads.get(pid)
            if not pl:
                continue
            it = QListWidgetItem(
                f"• {pl.name} ({pl.supplier_name}) — {pl.mass_kg:.1f} kg | {pl.volume_liters:.1f} L | "
                f"{pl.operational_power_w:.0f} W | {pl.price_meur:.2f} M€"
            )
            it.setData(Qt.ItemDataRole.UserRole, pid)
            self.list_selected_payloads.addItem(it)

    # ------------------------------------------------------------------ Tab 4: Platform & Options
    def _build_tab_platform(self) -> None:
        tab = QWidget()
        vsplit = QSplitter(Qt.Orientation.Vertical)
        l = QVBoxLayout(tab)
        l.addWidget(vsplit)

        cat_opts = [
            ("cubesat", "CubeSats (6U à 16U)"),
            ("smallsat", "Microsatellites & SmallSats (50 à 500 kg)"),
            ("medium", "Plateformes moyennes (700 à 1500 kg)"),
            ("heavy", "Plateformes lourdes (3000 kg)"),
        ]
        self.browser_platforms = CatalogBrowser(
            catalog=self.catalog,
            category="platform",
            action_button_text="✓ Choisir cette plateforme pour le satellite",
            type_filter_options=cat_opts,
            compatibility_fn=self._check_platform_compat,
            orbit_provider=self._current_orbit,
        )
        self.browser_platforms.item_activated.connect(self._on_platform_chosen)
        vsplit.addWidget(self.browser_platforms)

        self.slots_widget = PlatformSlotsWidget(self.catalog)
        self.slots_widget.options_changed.connect(self._on_slot_options_changed)
        vsplit.addWidget(self.slots_widget)

        vsplit.setStretchFactor(0, 3)
        vsplit.setStretchFactor(1, 2)
        self.tabs.addTab(tab, f"4. Plateforme & Options ({len(self.catalog.platforms)} réf.)")

    def _check_platform_compat(self, plat: PlatformBase) -> tuple[bool, str]:
        pls = [self.catalog.payloads[pid] for pid in self.project.configuration.selected_payload_ids if pid in self.catalog.payloads]
        tot_m = sum(p.mass_kg for p in pls)
        tot_v = sum(p.volume_liters for p in pls)
        tot_p = sum(p.operational_power_w for p in pls) * 0.25
        issues = []
        if tot_m > plat.max_payload_mass_kg:
            issues.append(f"CU {tot_m:.0f}>{plat.max_payload_mass_kg:.0f} kg")
        if tot_v > plat.payload_volume_liters:
            issues.append(f"vol. {tot_v:.0f}>{plat.payload_volume_liters:.0f} L")
        if tot_p > plat.payload_avg_power_w:
            issues.append(f"puiss. {tot_p:.0f}>{plat.payload_avg_power_w:.0f} W")
        if issues:
            return False, "Incompatible avec CU choisies : " + ", ".join(issues)
        return True, f"Apte pour CU actuelle ({tot_m:.0f}/{plat.max_payload_mass_kg:.0f} kg, {tot_v:.0f}/{plat.payload_volume_liters:.0f} L)"

    def _on_platform_chosen(self, plat: PlatformBase) -> None:
        self.project.configuration.platform_id = plat.id
        self.slots_widget.set_platform(plat)
        self.project.configuration.selected_options = self.slots_widget.selected_options()
        self.browser_payloads.refresh()
        self.browser_launchers.refresh()
        self.refresh_evaluation()

    def _on_slot_options_changed(self) -> None:
        self.project.configuration.selected_options = self.slots_widget.selected_options()
        self.browser_launchers.refresh()
        self.refresh_evaluation()

    # ------------------------------------------------------------------ Tab 5: Equipment Catalog
    def _build_tab_equipment_catalog(self) -> None:
        tab = QWidget()
        l = QVBoxLayout(tab)
        info = QLabel(
            "Explorez ici les catalogues de tous les équipementiers (propulsion chimique/électrique, TT&C, émetteurs X/Ka, "
            "mémoires de masse, suites ADCS). Pour activer une option sur votre plateforme, utilisez le tableau en bas de l'onglet 4."
        )
        info.setWordWrap(True)
        l.addWidget(info)

        fn_opts = [(k, v) for k, v in FUNCTION_LABELS_FR.items()]
        self.browser_equipments = CatalogBrowser(
            catalog=self.catalog,
            category="equipment",
            action_button_text="Voir compatibilité sur la plateforme",
            type_filter_options=fn_opts,
            compatibility_fn=self._check_equipment_compat,
            orbit_provider=self._current_orbit,
        )
        self.browser_equipments.btn_action.setVisible(False)
        l.addWidget(self.browser_equipments, stretch=1)
        self.tabs.addTab(tab, f"5. Catalogue Équipements ({len(self.catalog.equipments)} réf.)")

    def _check_equipment_compat(self, eq: Any) -> tuple[bool, str]:
        plat_id = self.project.configuration.platform_id
        if not plat_id or plat_id not in self.catalog.platforms:
            return True, ""
        plat = self.catalog.platforms[plat_id]
        for s in plat.slots:
            if s.function == eq.function and eq.id in s.allowed_equipment_ids:
                if eq.id in s.included_equipment_ids:
                    return True, f"Inclus de base sur {plat.name}"
                return True, f"Option autorisée sur {plat.name} (max {s.max_qty})"
        return False, f"Non qualifié sur {plat.name}"

    # ------------------------------------------------------------------ Tab 6: Launcher
    def _build_tab_launcher(self) -> None:
        tab = QWidget()
        l = QVBoxLayout(tab)
        self.lbl_chosen_launcher = QLabel()
        self.lbl_chosen_launcher.setStyleSheet(
            "background: #eff6ff; border: 1px solid #93c5fd; border-radius: 4px; padding: 6px; font-weight: bold;"
        )
        l.addWidget(self.lbl_chosen_launcher)

        ltype_opts = [("rideshare", "Covoiturage (Rideshare / Dispenser)"), ("dedicated", "Lanceur dédié")]
        self.browser_launchers = CatalogBrowser(
            catalog=self.catalog,
            category="launcher",
            action_button_text="✓ Retenir ce service de lancement",
            type_filter_options=ltype_opts,
            compatibility_fn=self._check_launcher_compat,
            orbit_provider=self._current_orbit,
        )
        self.browser_launchers.item_activated.connect(self._on_launcher_chosen)
        l.addWidget(self.browser_launchers, stretch=1)
        self.tabs.addTab(tab, f"6. Lanceurs ({len(self.catalog.launchers)} réf.)")

    def _check_launcher_compat(self, ln: Launcher) -> tuple[bool, str]:
        m_launch = self.current_budgets.mass.launch_mass_with_margin_kg if self.current_budgets else 0.0
        cap = launcher_capacity_for_orbit(ln, self._current_orbit())
        cost = ln.price_base_meur + ln.price_per_kg_meur * m_launch
        if m_launch > cap:
            return False, f"Masse sat {m_launch:.0f} kg > capacité {cap:.0f} kg ({cost:.2f} M€)"
        return True, f"Capacité OK : {m_launch:.0f}/{cap:.0f} kg — coût estimé {cost:.2f} M€"

    def _on_launcher_chosen(self, ln: Launcher) -> None:
        self.project.configuration.launcher_id = ln.id
        self.refresh_evaluation()

    # ------------------------------------------------------------------ Tab 7: Evaluation & Budgets
    def _build_tab_evaluation(self) -> None:
        tab = QWidget()
        l = QVBoxLayout(tab)

        self.lbl_budgets_cards = QLabel()
        self.lbl_budgets_cards.setWordWrap(True)
        self.lbl_budgets_cards.setStyleSheet(
            "background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 5px; padding: 10px; font-size: 12px;"
        )
        l.addWidget(self.lbl_budgets_cards)

        l.addWidget(QLabel("<b>Vérifications de conformité au cahier des charges & règles d'ingénierie système :</b>"))
        self.t_eval = QTableWidget(0, 5)
        self.t_eval.setHorizontalHeaderLabels(["Code", "Catégorie", "Statut", "Valeur Calculée", "Diagnostic détaillé"])
        self.t_eval.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.t_eval.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.t_eval.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.t_eval.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.t_eval.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        l.addWidget(self.t_eval, stretch=1)
        self.tabs.addTab(tab, "7. Analyses & Conformité")

    # ------------------------------------------------------------------ Tab 8: Student Written Sections
    def _build_tab_report_text(self) -> None:
        tab = QWidget()
        l = QVBoxLayout(tab)
        l.addWidget(QLabel("<b>1. Description du CONOPS (Modes, acquisition, gestion mémoire/liaison, éclipses, survie) :</b>"))
        self.txt_conops = QTextEdit()
        l.addWidget(self.txt_conops)
        l.addWidget(QLabel("<b>2. Justification des choix d'architecture & arbitrages (plateforme, options, charge utile, lanceur) :</b>"))
        self.txt_justif = QTextEdit()
        l.addWidget(self.txt_justif)
        l.addWidget(QLabel("<b>3. Analyse des risques, limitations et marges système :</b>"))
        self.txt_risks = QTextEdit()
        l.addWidget(self.txt_risks)
        self.tabs.addTab(tab, "8. Rédaction Rapport")

    def _sync_legacy_combos(self) -> None:
        self.combo_payloads = QComboBox()
        for pid, pl in self.catalog.payloads.items():
            self.combo_payloads.addItem(pl.name, pid)
        self.combo_platforms = QComboBox()
        for plat_id, plat in self.catalog.platforms.items():
            self.combo_platforms.addItem(plat.name, plat_id)
        self.combo_launchers = QComboBox()
        for ln_id, ln in self.catalog.launchers.items():
            self.combo_launchers.addItem(ln.name, ln_id)

    # ------------------------------------------------------------------ Evaluation
    def refresh_evaluation(self) -> None:
        orbit = self._current_orbit()
        self.project.configuration.orbit = orbit
        self.project.configuration.selected_options = self.slots_widget.selected_options()

        if not self.project.configuration.platform_id:
            return

        try:
            self.current_budgets = self.evaluator.evaluate(self.project.configuration, self.mission)
        except Exception as e:
            QMessageBox.critical(self, "Erreur d'évaluation", str(e))
            return

        b = self.current_budgets
        plat = b.configured_platform.base
        ln = self.catalog.launchers.get(self.project.configuration.launcher_id or "")
        ln_name = ln.name if ln else "Aucun"

        self.lbl_mission_title.setText(
            f"<b>Mission : {self.mission.title}</b> (Plafond : {self.mission.max_budget_meur:.1f} M€)   •   "
            f"<b>Plateforme :</b> {plat.name} ({plat.supplier_name})   •   "
            f"<b>Charges utiles :</b> {len(self.project.configuration.selected_payload_ids)}   •   "
            f"<b>Lanceur :</b> {ln_name}"
        )
        self.lbl_chosen_launcher.setText(
            f"Service de lancement actuellement retenu : {ln_name} — Coût lancement estimé : {b.cost.launcher_meur:.2f} M€ "
            f"(masse au lancement avec marge 20% : {b.mass.launch_mass_with_margin_kg:.1f} kg)"
        )

        all_checks = b.compliance_checks + b.rule_checks
        n_pass = sum(1 for c in all_checks if c.status == CheckStatus.PASS)
        status_tag = "CONFORME" if not b.has_blocking_errors else "NON CONFORME"
        self.lbl_live_summary.setText(
            f"Coût total : {b.cost.space_segment_total_meur:.2f} / {self.mission.max_budget_meur:.1f} M€  |  "
            f"Masse : {b.mass.launch_mass_with_margin_kg:.0f} kg  |  "
            f"Marge P : {b.power.power_margin_pct:.0f}%  |  "
            f"Vérifications : {n_pass}/{len(all_checks)} ({status_tag})"
        )

        self.lbl_budgets_cards.setText(
            f"<b>Bilan de Masse :</b> Plateforme sèche {b.mass.platform_dry_kg:.1f} kg + Options {b.mass.options_mass_kg:.1f} kg + "
            f"Charges utiles {b.mass.payloads_mass_kg:.1f} kg (max {b.mass.platform_capacity_kg:.1f} kg) + "
            f"Ergols {b.mass.propellant_mass_kg:.1f} kg = <b>{b.mass.system_wet_mass_kg:.1f} kg humide</b> "
            f"(<b>{b.mass.launch_mass_with_margin_kg:.1f} kg</b> avec marge {b.mass.margin_pct:.0f}%)<br>"
            f"<b>Bilan de Puissance :</b> Disponible pour CU+options : {b.power.platform_generation_w:.1f} W (bus total {b.power.platform_avg_power_w:.0f} W) | "
            f"Consommation moyenne : {b.power.total_avg_consumption_w:.1f} W (Options {b.power.options_avg_power_w:.1f} W + CU {b.power.payloads_avg_power_w:.1f} W) | "
            f"<b>Marge : {b.power.power_margin_w:.1f} W ({b.power.power_margin_pct:.1f}%)</b> | Crête : {b.power.peak_consumption_w:.0f} W<br>"
            f"<b>Bilan Financier :</b> Plateforme base {b.cost.platform_base_meur:.2f} M€ + Options & intégration {b.cost.options_total_meur:.2f} M€ + "
            f"Charges utiles {b.cost.payloads_total_meur:.2f} M€ + Lanceur {b.cost.launcher_meur:.2f} M€ = "
            f"<b>{b.cost.space_segment_total_meur:.2f} M€</b> (plafond {b.cost.mission_budget_limit_meur:.2f} M€, marge {b.cost.cost_margin_meur:+.2f} M€)"
        )

        self.t_eval.setRowCount(len(all_checks))
        for row, chk in enumerate(all_checks):
            self.t_eval.setItem(row, 0, QTableWidgetItem(chk.rule_id))
            self.t_eval.setItem(row, 1, QTableWidgetItem(chk.category))

            item_status = QTableWidgetItem(chk.status.value.upper())
            if chk.status == CheckStatus.PASS:
                item_status.setBackground(QColor(212, 239, 223))
                item_status.setForeground(QColor(20, 90, 50))
            elif chk.status == CheckStatus.WARNING:
                item_status.setBackground(QColor(252, 243, 207))
                item_status.setForeground(QColor(125, 102, 8))
            else:
                item_status.setBackground(QColor(242, 215, 213))
                item_status.setForeground(QColor(146, 43, 33))
            item_status.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            self.t_eval.setItem(row, 2, item_status)

            val_str = f"{chk.current_value} {chk.unit}" if chk.current_value is not None else "—"
            self.t_eval.setItem(row, 3, QTableWidgetItem(val_str))
            self.t_eval.setItem(row, 4, QTableWidgetItem(chk.message))

    # ------------------------------------------------------------------ Save / Open / Export
    def _sync_project_fields(self) -> None:
        self.project.student_name = self.ed_student_name.text().strip() or "Étudiant"
        self.project.student_id = self.ed_student_id.text().strip() or "ETU-001"
        self.project.project_id = self.ed_project_id.text().strip() or "EXAM-2026-001"
        self.project.conops_text = self.txt_conops.toPlainText()
        self.project.justification_text = self.txt_justif.toPlainText()
        self.project.risk_analysis_text = self.txt_risks.toPlainText()
        self.project.update_integrity()

    def save_project_json(self) -> None:
        self._sync_project_fields()
        fp, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer le projet étudiant", f"{self.project.student_id}_{self.project.project_id}.json", "Projet JSON (*.json)"
        )
        if not fp:
            return
        Path(fp).write_text(self.project.model_dump_json(indent=2), encoding="utf-8")
        QMessageBox.information(self, "Projet enregistré", f"Projet sauvegardé avec signature d'intégrité SHA-256 :\n{fp}")

    def open_project_json(self) -> None:
        fp, _ = QFileDialog.getOpenFileName(self, "Ouvrir un projet étudiant", "", "Projet JSON (*.json)")
        if not fp:
            return
        try:
            proj = StudentProject.model_validate_json(Path(fp).read_text(encoding="utf-8"))
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Fichier projet invalide :\n{e}")
            return
        self.project = proj
        self.mission = proj.mission
        self.ed_student_name.setText(proj.student_name)
        self.ed_student_id.setText(proj.student_id)
        self.ed_project_id.setText(proj.project_id)
        self.txt_conops.setPlainText(proj.conops_text)
        self.txt_justif.setPlainText(proj.justification_text)
        self.txt_risks.setPlainText(proj.risk_analysis_text)
        self._populate_mission_view()

        orb = proj.configuration.orbit
        self.combo_orbit_type.setCurrentIndex(0 if (orb.orbit_type == OrbitType.SSO) else 1)
        self.spin_altitude.setValue(orb.altitude_km)
        self.spin_inclination.setValue(orb.inclination_deg)

        if proj.configuration.platform_id and proj.configuration.platform_id in self.catalog.platforms:
            plat = self.catalog.platforms[proj.configuration.platform_id]
            self.slots_widget.set_platform(plat, proj.configuration.selected_options)
            self.browser_platforms.select_item_by_id(plat.id)

        self._refresh_selected_payloads_list()
        self.refresh_evaluation()

    def export_docx_report(self) -> None:
        if not self.current_budgets:
            return
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer le rapport d'examen", "Rapport_Systeme_Spatial.docx", "Word Documents (*.docx)"
        )
        if not file_path:
            return

        self._sync_project_fields()
        sim = OrbitPropagator.simulate(self.project.configuration.orbit, duration_orbits=2.0)
        out = ReportGenerator.generate(
            project=self.project,
            budgets=self.current_budgets,
            output_docx_path=file_path,
            ground_track=sim.ground_track,
        )
        QMessageBox.information(self, "Rapport Généré", f"Rapport généré avec succès :\n{out}")


def main() -> None:
    app = QApplication(sys.argv)
    window = StudentMainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
