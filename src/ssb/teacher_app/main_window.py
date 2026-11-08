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
    QSplitter,
    QTabWidget,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFileDialog,
    QMessageBox,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QDoubleSpinBox,
    QSpinBox,
    QFormLayout,
    QGroupBox,
)

from ssb.catalog.database import CatalogDatabase
from ssb.catalog.datasheet import PAYLOAD_TYPE_LABELS_FR, FUNCTION_LABELS_FR
from ssb.ui_common.global_architecture_view import GlobalArchitectureWidget
from ssb.core.paths import catalogs_dir, missions_dir
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
from ssb.ui_common.mission_sheet_view import MissionSheetView, MISSION_TYPE_BADGES_FR


class TeacherMainWindow(QMainWindow):
    """Teacher interface to create/inspect mission specification sheets, browse catalogs, and verify student projects."""

    def __init__(self, catalog_dir: Path | str | None = None) -> None:
        super().__init__()
        self.setWindowTitle("Space Segment Builder — Module Enseignant (Fiches Mission, Catalogues & Évaluation)")
        self.resize(1360, 840)

        self.catalog = CatalogDatabase()
        self.catalog.load_from_directory(catalog_dir or catalogs_dir())
        self.evaluator = SystemEvaluator(self.catalog)

        self._setup_ui()

    def _setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        header = QLabel("<h2>Espace Enseignant — Contrôle des Projets, Fiches de Spécification Mission & Catalogues</h2>")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # ---- Tab 1: Project Inspection & Grading
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

        self.global_arch_widget = GlobalArchitectureWidget(self.catalog)
        l_ins.addWidget(self.global_arch_widget)

        self.t_student_results = QTableWidget(0, 4)
        self.t_student_results.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                color: #0f172a;
                gridline-color: #cbd5e1;
                font-size: 12px;
                selection-background-color: #2563eb;
                selection-color: #ffffff;
            }
            QHeaderView::section {
                background-color: #0f2744;
                color: #ffffff;
                font-weight: bold;
                padding: 5px;
                border: 1px solid #1e3a5f;
            }
            QTableWidget::item {
                color: #0f172a;
                padding: 4px;
            }
        """)
        self.t_student_results.setHorizontalHeaderLabels(
            ["Règle / Exigence", "Statut Rejeu", "Valeur Calculée", "Observation"]
        )
        self.t_student_results.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        l_ins.addWidget(self.t_student_results)

        self.tabs.addTab(tab_inspect, "1. Rejeu & Contrôle Étudiant")

        # ---- Tab 2: Mission Specification Sheet Editor & Preview
        tab_create = QWidget()
        split_m = QSplitter(Qt.Orientation.Horizontal)
        l_cr_outer = QVBoxLayout(tab_create)

        top_m_bar = QHBoxLayout()
        top_m_bar.addWidget(QLabel("<b>Charger une fiche existante :</b>"))
        self.cmb_existing_missions = QComboBox()
        self.cmb_existing_missions.addItem("— Nouvelle fiche vierge —", "")
        mdir = missions_dir()
        if mdir.exists():
            for mf in sorted(mdir.glob("*.mission.json")):
                try:
                    ms = MissionSpecification.model_validate_json(mf.read_text(encoding="utf-8"))
                    self.cmb_existing_missions.addItem(f"[{ms.id}] {ms.title} ({ms.max_budget_meur:.1f} M€)", str(mf))
                except Exception:
                    pass
        self.cmb_existing_missions.currentIndexChanged.connect(self._on_load_existing_mission)
        top_m_bar.addWidget(self.cmb_existing_missions, stretch=1)

        btn_save_subject = QPushButton("Enregistrer la Fiche Mission (.mission.json)")
        btn_save_subject.setStyleSheet(
            "background-color: #2980b9; color: white; font-weight: bold; padding: 6px 14px;"
        )
        btn_save_subject.clicked.connect(self.save_mission_subject)
        top_m_bar.addWidget(btn_save_subject)
        l_cr_outer.addLayout(top_m_bar)

        form_box = QGroupBox("Édition de la Fiche de Spécification Mission")
        form = QFormLayout(form_box)
        self.edit_m_id = QLineEdit("EXAM-2026-CUSTOM")
        self.edit_m_title = QLineEdit("Mission Nouvelle Définition")
        self.edit_m_agency = QLineEdit("Agence Spatiale Européenne / CNES")
        self.cmb_m_type = QComboBox()
        for code, lbl in MISSION_TYPE_BADGES_FR.items():
            self.cmb_m_type.addItem(f"{lbl} ({code})", code)
        self.edit_m_domain = QLineEdit("Observation de la Terre — Imagerie optique & maritime")

        self.spin_m_budget = QDoubleSpinBox()
        self.spin_m_budget.setRange(0.5, 500.0)
        self.spin_m_budget.setValue(20.0)
        self.spin_m_budget.setSuffix(" M€")

        self.spin_m_life = QDoubleSpinBox()
        self.spin_m_life.setRange(0.5, 20.0)
        self.spin_m_life.setValue(5.0)
        self.spin_m_life.setSuffix(" ans")

        self.spin_m_trl = QSpinBox()
        self.spin_m_trl.setRange(1, 9)
        self.spin_m_trl.setValue(8)

        self.edit_m_context = QLineEdit(
            "Surveillance côtière et détection maritime par imagerie optique haute résolution..."
        )
        self.txt_m_objective = QTextEdit(
            "Fournir des images optiques de résolution <= 1,0 m au nadir et établir une liaison descendante "
            "permettant de rapatrier les scènes quotidiennes dans une enveloppe budgétaire totale plafonnée."
        )
        self.txt_m_objective.setMaximumHeight(75)
        self.txt_m_need = QTextEdit(
            "Besoin exprimé par les autorités maritimes et environnementales pour le suivi quotidien."
        )
        self.txt_m_need.setMaximumHeight(60)
        self.edit_m_orbit_desc = QLineEdit("Orbite héliosynchrone (SSO) entre 450 km et 600 km d'altitude.")
        self.edit_m_conops = QLineEdit(
            "Acquisition sur zones côtières éclairées, stockage mémoire de masse et vidage sur station sol."
        )

        for w in (
            self.edit_m_id,
            self.edit_m_title,
            self.edit_m_agency,
            self.edit_m_domain,
            self.edit_m_context,
            self.edit_m_orbit_desc,
            self.edit_m_conops,
        ):
            w.textChanged.connect(self._update_mission_preview)
        self.txt_m_objective.textChanged.connect(self._update_mission_preview)
        self.txt_m_need.textChanged.connect(self._update_mission_preview)
        self.cmb_m_type.currentIndexChanged.connect(self._update_mission_preview)
        self.spin_m_budget.valueChanged.connect(self._update_mission_preview)
        self.spin_m_life.valueChanged.connect(self._update_mission_preview)
        self.spin_m_trl.valueChanged.connect(self._update_mission_preview)

        form.addRow("ID Mission :", self.edit_m_id)
        form.addRow("Titre de la Mission :", self.edit_m_title)
        form.addRow("Agence / Client :", self.edit_m_agency)
        form.addRow("Type de Mission :", self.cmb_m_type)
        form.addRow("Domaine affiché :", self.edit_m_domain)
        form.addRow("Budget Total Plafond (M€) :", self.spin_m_budget)
        form.addRow("Durée de vie / TRL min :", self.spin_m_life)
        form.addRow("Contexte opérationnel :", self.edit_m_context)
        form.addRow("Objectif principal décrit :", self.txt_m_objective)
        form.addRow("Besoin scientifique/opér. :", self.txt_m_need)
        form.addRow("Contraintes orbitales :", self.edit_m_orbit_desc)
        form.addRow("CONOPS attendu :", self.edit_m_conops)
        split_m.addWidget(form_box)

        self.mission_preview = MissionSheetView()
        split_m.addWidget(self.mission_preview)
        split_m.setStretchFactor(0, 2)
        split_m.setStretchFactor(1, 3)
        l_cr_outer.addWidget(split_m, stretch=1)

        self._loaded_reqs: list[MissionRequirement] = [
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
        ]
        self._loaded_stations: list[GroundStationTarget] = [
            GroundStationTarget(
                id="sta_toulouse",
                name="Toulouse Ground Station",
                latitude_deg=43.60,
                longitude_deg=1.44,
                min_elevation_deg=5.0,
            )
        ]
        self._loaded_secondary: list[str] = []
        self._loaded_deliverables: list[str] = []
        self._update_mission_preview()

        self.tabs.addTab(tab_create, "2. Fiches de Spécification Mission")

        # ---- Tab 3: Complete Reference Catalog Browser
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

    def _build_current_mission_spec(self) -> MissionSpecification:
        return MissionSpecification(
            id=self.edit_m_id.text().strip() or "EXAM-CUSTOM",
            title=self.edit_m_title.text().strip() or "Mission",
            client_agency=self.edit_m_agency.text().strip(),
            domain_label=self.edit_m_domain.text().strip(),
            context=self.edit_m_context.text().strip(),
            primary_objective=self.txt_m_objective.toPlainText().strip(),
            secondary_objectives=self._loaded_secondary,
            scientific_or_operational_need=self.txt_m_need.toPlainText().strip(),
            orbit_constraints_description=self.edit_m_orbit_desc.text().strip(),
            conops_guidance=self.edit_m_conops.text().strip(),
            deliverables_expected=self._loaded_deliverables,
            mission_type=self.cmb_m_type.currentData() or "optical_eo",
            max_budget_meur=self.spin_m_budget.value(),
            target_lifetime_years=self.spin_m_life.value(),
            min_trl=self.spin_m_trl.value(),
            requirements=self._loaded_reqs,
            ground_stations=self._loaded_stations,
        )

    def _update_mission_preview(self) -> None:
        self.mission_preview.set_mission(self._build_current_mission_spec())

    def _on_load_existing_mission(self) -> None:
        fp = self.cmb_existing_missions.currentData()
        if not fp:
            return
        ms = MissionSpecification.model_validate_json(Path(fp).read_text(encoding="utf-8"))
        self.edit_m_id.setText(ms.id)
        self.edit_m_title.setText(ms.title)
        self.edit_m_agency.setText(ms.client_agency)
        self.edit_m_domain.setText(ms.domain_label)
        idx = self.cmb_m_type.findData(ms.mission_type)
        if idx >= 0:
            self.cmb_m_type.setCurrentIndex(idx)
        self.spin_m_budget.setValue(ms.max_budget_meur)
        self.spin_m_life.setValue(ms.target_lifetime_years)
        self.spin_m_trl.setValue(ms.min_trl)
        self.edit_m_context.setText(ms.context)
        self.txt_m_objective.setPlainText(ms.primary_objective or ms.context)
        self.txt_m_need.setPlainText(ms.scientific_or_operational_need)
        self.edit_m_orbit_desc.setText(ms.orbit_constraints_description)
        self.edit_m_conops.setText(ms.conops_guidance)
        self._loaded_reqs = list(ms.requirements)
        self._loaded_stations = list(ms.ground_stations)
        self._loaded_secondary = list(ms.secondary_objectives)
        self._loaded_deliverables = list(ms.deliverables_expected)
        self._update_mission_preview()

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
            self.global_arch_widget.refresh(proj, budgets)
            all_checks = budgets.compliance_checks + budgets.rule_checks

            self.t_student_results.setRowCount(len(all_checks))
            pass_count = sum(1 for c in all_checks if c.status == CheckStatus.PASS)

            for row, chk in enumerate(all_checks):
                it0 = QTableWidgetItem(chk.rule_id)
                it0.setForeground(QColor("#0f172a"))
                self.t_student_results.setItem(row, 0, it0)

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
                it2 = QTableWidgetItem(val_str)
                it2.setForeground(QColor("#0f172a"))
                self.t_student_results.setItem(row, 2, it2)
                it3 = QTableWidgetItem(chk.message)
                it3.setForeground(QColor("#0f172a"))
                self.t_student_results.setItem(row, 3, it3)

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
            self,
            "Enregistrer la fiche de spécification mission",
            f"{self.edit_m_id.text()}.mission.json",
            "JSON Files (*.json)",
        )
        if not file_path:
            return

        mission = self._build_current_mission_spec()
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(mission.model_dump_json(indent=2))

        QMessageBox.information(self, "Fiche Mission Enregistrée", f"Fiche de spécification mission enregistrée :\n{file_path}")


def main() -> None:
    app = QApplication(sys.argv)
    window = TeacherMainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
