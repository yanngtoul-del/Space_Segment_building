"""Main interactive PySide6 graphical user interface for teachers and examiners."""

import json
import sys
from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFileDialog,
    QMessageBox,
    QLineEdit,
    QDoubleSpinBox,
    QFormLayout,
)

from ssb.catalog.database import CatalogDatabase
from ssb.catalog.datasheet import PAYLOAD_TYPE_LABELS_FR, FUNCTION_LABELS_FR
from ssb.core.paths import catalogs_dir
from ssb.core.mission import (
    MissionSpecification,
    MissionRequirement,
    RequirementType,
    RequirementOperator,
    GroundStationTarget,
)
from ssb.core.project import StudentProject
from ssb.system.evaluator import SystemEvaluator, CheckStatus
from ssb.ui_common.catalog_browser import CatalogBrowser


class TeacherMainWindow(QMainWindow):
    """Teacher interface to create mission topics, browse catalogs, and verify student project submissions."""

    def __init__(self, catalog_dir: Path | str | None = None) -> None:
        super().__init__()
        self.setWindowTitle("Space Segment Builder — Module Enseignant (Sujets, Catalogues & Évaluation)")
        self.resize(1340, 820)

        self.catalog = CatalogDatabase()
        self.catalog.load_from_directory(catalog_dir or catalogs_dir())
        self.evaluator = SystemEvaluator(self.catalog)

        self._setup_ui()

    def _setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        header = QLabel("<h2>Espace Enseignant — Contrôle des Projets, Catalogues & Édition des Sujets</h2>")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Tab 1: Project Inspection & Grading
        tab_inspect = QWidget()
        l_ins = QVBoxLayout(tab_inspect)

        btn_row = QHBoxLayout()
        self.btn_load_project = QPushButton("Ouvrir un Projet Étudiant (.json)")
        self.btn_load_project.setStyleSheet(
            "background-color: #27ae60; color: white; font-weight: bold; padding: 6px 14px;"
        )
        self.btn_load_project.clicked.connect(self.load_student_project)
        btn_row.addWidget(self.btn_load_project)
        btn_row.addStretch()
        l_ins.addLayout(btn_row)

        self.lbl_student_status = QLabel("<i>Aucun projet chargé.</i>")
        l_ins.addWidget(self.lbl_student_status)

        self.t_student_results = QTableWidget(0, 4)
        self.t_student_results.setHorizontalHeaderLabels(
            ["Règle / Exigence", "Statut Rejeu", "Valeur Calculée", "Observation"]
        )
        self.t_student_results.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        l_ins.addWidget(self.t_student_results)

        self.tabs.addTab(tab_inspect, "1. Rejeu & Contrôle Étudiant")

        # Tab 2: Mission Topic Creator
        tab_create = QWidget()
        l_cr = QVBoxLayout(tab_create)

        form = QFormLayout()
        self.edit_m_id = QLineEdit("EXAM-2026-CUSTOM")
        self.edit_m_title = QLineEdit("Mission Nouvelle Définition")
        self.edit_m_context = QLineEdit("Surveillance côtière et détection maritime par optique et AIS...")
        self.spin_m_budget = QDoubleSpinBox()
        self.spin_m_budget.setRange(1.0, 500.0)
        self.spin_m_budget.setValue(20.0)
        self.spin_m_budget.setSuffix(" M€")

        form.addRow("ID Sujet :", self.edit_m_id)
        form.addRow("Titre de la Mission :", self.edit_m_title)
        form.addRow("Contexte opérationnel :", self.edit_m_context)
        form.addRow("Budget Plafond (M€) :", self.spin_m_budget)
        l_cr.addLayout(form)

        btn_save_subject = QPushButton("Enregistrer le Sujet (.mission.json)")
        btn_save_subject.setStyleSheet(
            "background-color: #2980b9; color: white; font-weight: bold; padding: 6px 12px;"
        )
        btn_save_subject.clicked.connect(self.save_mission_subject)
        l_cr.addWidget(btn_save_subject)
        l_cr.addStretch()

        self.tabs.addTab(tab_create, "2. Créateur de Sujet")

        # Tab 3: Complete Reference Catalog Browser (Payloads, Platforms, Equipment, Launchers)
        cat_tabs = QTabWidget()
        for cat, title, opts in [
            ("payload", f"Charges utiles ({len(self.catalog.payloads)})", list(PAYLOAD_TYPE_LABELS_FR.items())),
            ("platform", f"Plateformes ({len(self.catalog.platforms)})", None),
            ("equipment", f"Équipements ({len(self.catalog.equipments)})", list(FUNCTION_LABELS_FR.items())),
            ("launcher", f"Lanceurs ({len(self.catalog.launchers)})", None),
        ]:
            br = CatalogBrowser(self.catalog, cat, type_filter_options=opts)
            br.btn_action.setVisible(False)
            cat_tabs.addTab(br, title)
        self.tabs.addTab(cat_tabs, "3. Exploration des Catalogues & Datasheets")

    def load_student_project(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Sélectionner un projet étudiant", "", "Fichiers Projet (*.json)"
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            proj = StudentProject.model_validate(data)

            is_valid_hash = proj.verify_integrity()
            hash_tag = (
                "<b style='color:green;'>VALIDÉE (Intact)</b>"
                if is_valid_hash
                else "<b style='color:red;'>CORROMPUE (Fichier modifié manuellement)</b>"
            )

            self.lbl_student_status.setText(
                f"<b>Étudiant :</b> {proj.student_name} (ID: {proj.student_id}) | "
                f"<b>Projet :</b> {proj.project_id} | <b>Signature :</b> {hash_tag}"
            )

            budgets = self.evaluator.evaluate(proj.configuration, proj.mission)
            all_checks = budgets.compliance_checks + budgets.rule_checks

            self.t_student_results.setRowCount(len(all_checks))
            pass_count = sum(1 for c in all_checks if c.status == CheckStatus.PASS)

            for row, chk in enumerate(all_checks):
                self.t_student_results.setItem(row, 0, QTableWidgetItem(chk.rule_id))

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
                self.t_student_results.setItem(row, 1, item_status)

                val_str = f"{chk.current_value} {chk.unit}" if chk.current_value is not None else "-"
                self.t_student_results.setItem(row, 2, QTableWidgetItem(val_str))
                self.t_student_results.setItem(row, 3, QTableWidgetItem(chk.message))

            QMessageBox.information(
                self,
                "Rejeu Terminé",
                f"Projet rejoué avec succès !\nConformité : {pass_count}/{len(all_checks)} vérifications validées.\n"
                f"Empreinte intégrité : {'OK' if is_valid_hash else 'NON VALIDE'}",
            )

        except Exception as e:
            QMessageBox.critical(self, "Erreur de lecture", f"Impossible d'ouvrir le projet :\n{e}")

    def save_mission_subject(self) -> None:
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer le sujet d'examen", f"{self.edit_m_id.text()}.mission.json", "JSON Files (*.json)"
        )
        if not file_path:
            return

        mission = MissionSpecification(
            id=self.edit_m_id.text(),
            title=self.edit_m_title.text(),
            context=self.edit_m_context.text(),
            mission_type="optical_eo",
            max_budget_meur=self.spin_m_budget.value(),
            requirements=[
                MissionRequirement(
                    id="REQ-GSD-01",
                    title="GSD au nadir",
                    description="GSD <= 1.0 m",
                    req_type=RequirementType.PAYLOAD_PERF,
                    parameter="gsd_nadir_m",
                    operator=RequirementOperator.LE,
                    threshold=1.0,
                    unit="m",
                )
            ],
            ground_stations=[
                GroundStationTarget(
                    id="sta_toulouse",
                    name="Toulouse Ground Station",
                    latitude_deg=43.60,
                    longitude_deg=1.44,
                    min_elevation_deg=5.0,
                )
            ],
        )

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(mission.model_dump_json(indent=2))

        QMessageBox.information(self, "Sujet Enregistré", f"Sujet d'examen enregistré :\n{file_path}")


def main() -> None:
    app = QApplication(sys.argv)
    window = TeacherMainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
