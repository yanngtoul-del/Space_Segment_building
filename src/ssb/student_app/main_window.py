"""Main interactive PySide6 graphical user interface for students."""

import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QLabel,
    QPushButton,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QTextEdit,
    QFileDialog,
    QMessageBox,
    QGroupBox,
    QFormLayout,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

from ssb.catalog.database import CatalogDatabase
from ssb.core.orbit import OrbitDefinition, OrbitType
from ssb.core.mission import (
    MissionSpecification,
    MissionRequirement,
    RequirementType,
    RequirementOperator,
    GroundStationTarget,
)
from ssb.core.project import StudentProject, SystemConfiguration, SelectedOption
from ssb.system.evaluator import SystemEvaluator, CheckStatus, SystemBudgets
from ssb.orbit.propagator import OrbitPropagator
from ssb.report.generator import ReportGenerator


class StudentMainWindow(QMainWindow):
    """Main desktop interface for students taking the satellite design exam."""

    def __init__(self, catalog_dir: Path | str = "data/catalogs") -> None:
        super().__init__()
        self.setWindowTitle("Space Segment Builder — Examen Système Spatial")
        self.resize(1100, 750)

        # Load database
        self.catalog = CatalogDatabase()
        self.catalog.load_from_directory(catalog_dir)
        self.evaluator = SystemEvaluator(self.catalog)

        # Default mission and project state
        self.mission = self._create_default_exam_mission()
        self.project = StudentProject(
            project_id="EXAM-2026-001",
            student_name="Étudiant",
            student_id="ETU-001",
            mission=self.mission,
        )

        self._setup_ui()
        self.refresh_evaluation()

    def _create_default_exam_mission(self) -> MissionSpecification:
        return MissionSpecification(
            id="EXAM-SSO-HR",
            title="Mission Sentinel-Vision Tactical",
            context="Concevoir un satellite d'observation de la Terre basse orbite haute résolution pour le suivi des infrastructures critiques.",
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

    def _setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # Top banner with student info & status
        banner = QHBoxLayout()
        self.lbl_mission_title = QLabel(f"<b>Mission : {self.mission.title}</b> (Plafond : {self.mission.max_budget_meur:.1f} M€)")
        banner.addWidget(self.lbl_mission_title)
        banner.addStretch()

        self.btn_export_report = QPushButton("Générer Rapport Word (.docx)")
        self.btn_export_report.setStyleSheet("background-color: #1a5276; color: white; font-weight: bold; padding: 6px 12px;")
        self.btn_export_report.clicked.connect(self.export_docx_report)
        banner.addWidget(self.btn_export_report)
        main_layout.addLayout(banner)

        # Tabs for student workflow
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # 1. Mission Tab
        tab_mission = QWidget()
        l_miss = QVBoxLayout(tab_mission)
        l_miss.addWidget(QLabel(f"<b>Contexte :</b> {self.mission.context}"))
        l_miss.addWidget(QLabel("<b>Exigences Mission :</b>"))
        self.t_mission_reqs = QTableWidget(len(self.mission.requirements), 4)
        self.t_mission_reqs.setHorizontalHeaderLabels(["ID", "Intitulé", "Seuil", "Unité"])
        self.t_mission_reqs.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for row, req in enumerate(self.mission.requirements):
            self.t_mission_reqs.setItem(row, 0, QTableWidgetItem(req.id))
            self.t_mission_reqs.setItem(row, 1, QTableWidgetItem(req.title))
            self.t_mission_reqs.setItem(row, 2, QTableWidgetItem(f"{req.operator.value} {req.threshold}"))
            self.t_mission_reqs.setItem(row, 3, QTableWidgetItem(req.unit))
        l_miss.addWidget(self.t_mission_reqs)
        self.tabs.addTab(tab_mission, "1. Sujet & Exigences")

        # 2. Orbit Tab
        tab_orbit = QWidget()
        l_orb = QFormLayout(tab_orbit)
        self.combo_orbit_type = QComboBox()
        self.combo_orbit_type.addItems(["SSO (Héliosynchrone)", "Circulaire libre"])
        l_orb.addRow("Type d'Orbite :", self.combo_orbit_type)

        self.spin_altitude = QDoubleSpinBox()
        self.spin_altitude.setRange(200.0, 2000.0)
        self.spin_altitude.setValue(500.0)
        self.spin_altitude.setSuffix(" km")
        self.spin_altitude.valueChanged.connect(self._on_orbit_changed)
        l_orb.addRow("Altitude :", self.spin_altitude)

        self.lbl_inclination = QLabel("97.4 ° (calculée SSO J2)")
        l_orb.addRow("Inclinaison requise :", self.lbl_inclination)
        self.tabs.addTab(tab_orbit, "2. Orbite")

        # 3. Payload Tab
        tab_payload = QWidget()
        l_pl = QVBoxLayout(tab_payload)
        l_pl.addWidget(QLabel("<b>Sélectionnez la/les charge(s) utile(s) au catalogue :</b>"))
        self.combo_payloads = QComboBox()
        for pid, pl in self.catalog.payloads.items():
            self.combo_payloads.addItem(f"{pl.name} ({pl.supplier_name}) — {pl.mass_kg} kg, {pl.operational_power_w} W, {pl.price_meur:.2f} M€", pid)
        self.combo_payloads.currentIndexChanged.connect(self.refresh_evaluation)
        l_pl.addWidget(self.combo_payloads)
        l_pl.addStretch()
        self.tabs.addTab(tab_payload, "3. Charges Utiles")

        # 4. Platform Tab
        tab_plat = QWidget()
        l_p = QVBoxLayout(tab_plat)
        l_p.addWidget(QLabel("<b>Sélectionnez la plateforme :</b>"))
        self.combo_platforms = QComboBox()
        for plat_id, plat in self.catalog.platforms.items():
            self.combo_platforms.addItem(f"{plat.name} ({plat.supplier_name}) — Capacité PL: {plat.max_payload_mass_kg} kg, Puissance: {plat.payload_avg_power_w} W, {plat.base_price_meur:.2f} M€", plat_id)
        self.combo_platforms.currentIndexChanged.connect(self.refresh_evaluation)
        l_p.addWidget(self.combo_platforms)
        l_p.addStretch()
        self.tabs.addTab(tab_plat, "4. Plateforme & Options")

        # 5. Launcher Tab
        tab_ln = QWidget()
        l_ln = QVBoxLayout(tab_ln)
        l_ln.addWidget(QLabel("<b>Sélectionnez le lanceur :</b>"))
        self.combo_launchers = QComboBox()
        for ln_id, ln in self.catalog.launchers.items():
            self.combo_launchers.addItem(f"{ln.name} ({ln.launcher_type.upper()}) — Base: {ln.price_base_meur:.2f} M€", ln_id)
        self.combo_launchers.currentIndexChanged.connect(self.refresh_evaluation)
        l_ln.addWidget(self.combo_launchers)
        l_ln.addStretch()
        self.tabs.addTab(tab_ln, "5. Lanceur")

        # 6. Evaluation & Budgets Tab
        tab_eval = QWidget()
        l_ev = QVBoxLayout(tab_eval)
        l_ev.addWidget(QLabel("<b>Tableau de Bord & Budgets Système :</b>"))
        self.t_eval = QTableWidget(6, 4)
        self.t_eval.setHorizontalHeaderLabels(["Exigence / Budget", "Statut", "Valeur Calculée", "Commentaire"])
        self.t_eval.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        l_ev.addWidget(self.t_eval)
        self.tabs.addTab(tab_eval, "6. Analyses & Conformité")

        # 7. Student Written Sections
        tab_txt = QWidget()
        l_txt = QVBoxLayout(tab_txt)
        l_txt.addWidget(QLabel("<b>Description du CONOPS (Modes, acquisition, stations sol, survie) :</b>"))
        self.txt_conops = QTextEdit()
        l_txt.addWidget(self.txt_conops)
        l_txt.addWidget(QLabel("<b>Justification des Choix & Arbitrages :</b>"))
        self.txt_justif = QTextEdit()
        l_txt.addWidget(self.txt_justif)
        self.tabs.addTab(tab_txt, "7. Rédaction Rapport")

    def _on_orbit_changed(self) -> None:
        alt = self.spin_altitude.value()
        try:
            inc = OrbitDefinition.compute_sso_inclination(alt)
            self.lbl_inclination.setText(f"{inc:.2f} ° (calculée SSO J2)")
        except Exception:
            self.lbl_inclination.setText("Incalculable")
        self.refresh_evaluation()

    def refresh_evaluation(self) -> None:
        alt = self.spin_altitude.value()
        inc = OrbitDefinition.compute_sso_inclination(alt)
        orbit = OrbitDefinition(altitude_km=alt, inclination_deg=inc)

        plat_id = self.combo_platforms.currentData()
        payload_id = self.combo_payloads.currentData()
        launcher_id = self.combo_launchers.currentData()

        if not plat_id or not payload_id:
            return

        # Simple default configuration selection for the student view
        config = SystemConfiguration(
            orbit=orbit,
            platform_id=plat_id,
            selected_payload_ids=[payload_id],
            launcher_id=launcher_id,
        )

        try:
            self.current_budgets = self.evaluator.evaluate(config, self.mission)
            self.project.configuration = config
        except Exception as e:
            QMessageBox.critical(self, "Erreur d'évaluation", str(e))
            return

        all_checks = self.current_budgets.compliance_checks + self.current_budgets.rule_checks
        self.t_eval.setRowCount(len(all_checks))
        for row, chk in enumerate(all_checks):
            self.t_eval.setItem(row, 0, QTableWidgetItem(chk.rule_id))

            item_status = QTableWidgetItem(chk.status.value.upper())
            if chk.status == CheckStatus.PASS:
                item_status.setBackground(QColor(212, 239, 223))  # Soft green
                item_status.setForeground(QColor(20, 90, 50))
            elif chk.status == CheckStatus.WARNING:
                item_status.setBackground(QColor(252, 243, 207))  # Soft yellow
                item_status.setForeground(QColor(125, 102, 8))
            else:
                item_status.setBackground(QColor(242, 215, 213))  # Soft red
                item_status.setForeground(QColor(146, 43, 33))
            item_status.setFont(QFont("Segoe UI", 9, QFont.Bold))
            self.t_eval.setItem(row, 1, item_status)

            val_str = f"{chk.current_value} {chk.unit}" if chk.current_value is not None else "-"
            self.t_eval.setItem(row, 2, QTableWidgetItem(val_str))
            self.t_eval.setItem(row, 3, QTableWidgetItem(chk.message))

    def export_docx_report(self) -> None:
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer le rapport d'examen", "Rapport_Systeme_Spatial.docx", "Word Documents (*.docx)"
        )
        if not file_path:
            return

        self.project.conops_text = self.txt_conops.toPlainText()
        self.project.justification_text = self.txt_justif.toPlainText()
        self.project.update_integrity()

        # Simulate 2 orbits for the report ground track plot
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
