"""Global Space Segment Architecture & Selection Overview Widget and Dialog."""

from typing import Any
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QDialog,
    QPushButton,
    QGroupBox,
    QAbstractScrollArea,
)

from ssb.catalog.database import CatalogDatabase
from ssb.catalog.datasheet import build_datasheet
from ssb.core.catalog_meta import country_with_flag
from ssb.core.project import Launcher
from ssb.system.evaluator import launcher_capacity_for_orbit
from ssb.core.platform import PlatformBase
from ssb.core.payload import BasePayload
from ssb.core.project import StudentProject
from ssb.system.evaluator import SystemBudgets
from ssb.ui_common.catalog_browser import DatasheetView


CATEGORY_ICONS = {
    "platform": "🛰️ Plateforme",
    "payload": "📷 Charge Utile",
    "propulsion": "⚡ Propulsion",
    "ttc": "📡 TM/TC (TT&C)",
    "payload_downlink": "📶 Liaison descendante CU",
    "mass_memory": "💾 Mémoire de masse",
    "adcs": "🧭 ADCS & Guidage",
    "launcher": "🚀 Service de Lancement",
}


class GlobalArchitectureWidget(QWidget):
    """Unified comprehensive view of everything selected in the space segment:

    Platform, Payloads, Configured Platform Options / Equipments, and Launcher.
    """

    def __init__(
        self,
        catalog: CatalogDatabase,
        project: StudentProject | None = None,
        budgets: SystemBudgets | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.catalog = catalog
        self.project = project
        self.budgets = budgets

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        # 1. KPI Cards Row
        self.kpi_box = QGroupBox("Synthèse rapide du segment spatial")
        kpi_layout = QHBoxLayout(self.kpi_box)
        kpi_layout.setContentsMargins(6, 6, 6, 6)

        self.kpi_plat = QLabel()
        self.kpi_pl = QLabel()
        self.kpi_opts = QLabel()
        self.kpi_ln = QLabel()

        for lbl in (self.kpi_plat, self.kpi_pl, self.kpi_opts, self.kpi_ln):
            lbl.setStyleSheet(
                "background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; border-radius: 4px; padding: 6px; font-size: 11px;"
            )
            lbl.setWordWrap(True)
            kpi_layout.addWidget(lbl, stretch=1)

        layout.addWidget(self.kpi_box)

        # 2. Main Architecture Table
        hdr_layout = QHBoxLayout()
        hdr_lbl = QLabel("<b>Composition Détaillée du Segment Spatial Sélectionné</b>")
        hdr_lbl.setStyleSheet("font-size: 12px; color: #1e293b;")
        hdr_layout.addWidget(hdr_lbl)
        hdr_layout.addStretch()

        help_lbl = QLabel("💡 <i>Double-cliquez sur une ligne pour ouvrir la datasheet complète de l'élément.</i>")
        help_lbl.setStyleSheet("font-size: 11px; color: #64748b;")
        hdr_layout.addWidget(help_lbl)
        layout.addLayout(hdr_layout)

        self.table = QTableWidget(0, 7)
        self.table.setStyleSheet("""
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
                padding: 6px;
                border: 1px solid #1e3a5f;
            }
            QTableWidget::item {
                color: #0f172a;
                padding: 4px;
            }
        """)
        self.table.setHorizontalHeaderLabels(
            [
                "Poste / Sous-système",
                "Élément sélectionné",
                "Fournisseur & Pays",
                "Qté / Détails",
                "Masse",
                "Puissance",
                "Coût",
            ]
        )
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.table.cellDoubleClicked.connect(self._on_cell_double_clicked)
        layout.addWidget(self.table, stretch=1)

        if self.project:
            self.refresh(self.project, self.budgets)

    def refresh(self, project: StudentProject, budgets: SystemBudgets | None) -> None:
        self.project = project
        self.budgets = budgets
        self.table.setRowCount(0)

        cfg = project.configuration
        plat = self.catalog.platforms.get(cfg.platform_id or "")
        pls = [self.catalog.payloads[pid] for pid in cfg.selected_payload_ids if pid in self.catalog.payloads]
        ln = self.catalog.launchers.get(cfg.launcher_id or "")

        # Update KPI Cards
        plat_txt = (
            f"🛰️ <b>Plateforme :</b> {plat.name}<br>"
            f"<span style='color:#64748b;'>{plat.supplier_name} ({country_with_flag(self._country(plat.supplier_id))})</span><br>"
            f"Base : {plat.base_price_meur:.2f} M€ | Sèche : {plat.dry_mass_kg:.0f} kg"
            if plat
            else "🛰️ <b>Plateforme :</b> <span style='color:#dc2626;'>Non sélectionnée</span>"
        )
        self.kpi_plat.setText(plat_txt)

        tot_pl_m = sum(p.mass_kg for p in pls)
        tot_pl_cost = sum(p.price_meur for p in pls)
        pl_txt = (
            f"📷 <b>Charges Utiles :</b> {len(pls)} embarquée(s)<br>"
            f"Masse CU : {tot_pl_m:.1f} kg (cap. {plat.max_payload_mass_kg:.0f} kg)<br>"
            f"Coût CU : {tot_pl_cost:.2f} M€"
            if plat and pls
            else f"📷 <b>Charges Utiles :</b> {len(pls)} sélectionnée(s)"
        )
        self.kpi_pl.setText(pl_txt)

        resolved_opts = budgets.configured_platform.resolved_options if budgets else []
        opt_cost = sum(o.final_price_meur for o in resolved_opts)
        opt_txt = (
            f"⚙️ <b>Sous-systèmes / Options :</b> {len(resolved_opts)} actif(s)<br>"
            f"Coût options : +{opt_cost:.2f} M€<br>"
            f"Masse ajouts : {sum(o.final_mass_kg for o in resolved_opts):.1f} kg"
        )
        self.kpi_opts.setText(opt_txt)

        m_launch = budgets.mass.launch_mass_with_margin_kg if budgets else 0.0
        ln_cap = launcher_capacity_for_orbit(ln, cfg.orbit) if ln else 0.0
        ln_cost = budgets.cost.launcher_meur if budgets else (ln.price_base_meur if ln else 0.0)
        ln_txt = (
            f"🚀 <b>Lanceur :</b> {ln.name}<br>"
            f"Capacité {cfg.orbit.orbit_type.value.upper()} : {ln_cap:.0f} kg (Sat : {m_launch:.0f} kg)<br>"
            f"Coût estimé : {ln_cost:.2f} M€"
            if ln
            else "🚀 <b>Lanceur :</b> <span style='color:#dc2626;'>Non sélectionné</span>"
        )
        self.kpi_ln.setText(ln_txt)

        # Build table rows
        rows: list[dict[str, Any]] = []

        # 1. Platform Row
        if plat:
            plat_sup = self.catalog.suppliers.get(plat.supplier_id)
            c_flag = country_with_flag(plat_sup.country if plat_sup else "")
            rows.append(
                {
                    "item": plat,
                    "cat": "🛰️ Plateforme",
                    "name": f"{plat.name} ({plat.category})",
                    "supplier": f"{plat.supplier_name} [{c_flag}]",
                    "details": f"Emport CU: {plat.max_payload_mass_kg:.0f} kg / {plat.payload_volume_liters:.0f} L | Bus: {plat.payload_avg_power_w:.0f} W",
                    "mass": f"{plat.dry_mass_kg:.1f} kg",
                    "power": f"— (Bus {plat.payload_avg_power_w:.0f} W)",
                    "cost": f"{plat.base_price_meur:.2f} M€",
                    "bg": QColor(240, 249, 255),
                    "fg": QColor("#0369a1"),
                    "bold": True,
                }
            )

        # 2. Payloads Rows
        for p in pls:
            p_sup = self.catalog.suppliers.get(p.supplier_id)
            c_flag = country_with_flag(p_sup.country if p_sup else "")
            rows.append(
                {
                    "item": p,
                    "cat": "📷 Charge Utile",
                    "name": f"{p.name}",
                    "supplier": f"{p.supplier_name} [{c_flag}]",
                    "details": f"Type: {p.payload_type.value} | Vol: {p.volume_liters:.1f} L",
                    "mass": f"{p.mass_kg:.1f} kg",
                    "power": f"{p.operational_power_w * 0.25:.1f} W (crête {p.operational_power_w:.0f} W)",
                    "cost": f"{p.price_meur:.2f} M€",
                    "bg": QColor(254, 243, 199),
                    "fg": QColor("#78350f"),
                    "bold": False,
                }
            )

        # 3. Configured Platform Options / Equipments
        for opt in resolved_opts:
            eq = opt.equipment
            eq_sup = self.catalog.suppliers.get(eq.supplier_id)
            c_flag = country_with_flag(eq_sup.country if eq_sup else "")
            cat_label = CATEGORY_ICONS.get(eq.function.value, f"⚙️ {eq.function.value.upper()}")
            cost_str = "0,00 M€ (Inclus)" if opt.is_included else f"+{opt.final_price_meur:.2f} M€"
            status_tag = "Inclus de base" if opt.is_included else "Option ajoutée"
            rows.append(
                {
                    "item": eq,
                    "cat": cat_label,
                    "name": eq.name,
                    "supplier": f"{eq.supplier_name} [{c_flag}]",
                    "details": f"Slot: {eq.function.value.upper()} | {status_tag}",
                    "mass": f"{opt.final_mass_kg:.1f} kg",
                    "power": f"{eq.power_w:.1f} W",
                    "cost": cost_str,
                    "bg": QColor(241, 245, 249),
                    "fg": QColor("#0f172a"),
                    "bold": False,
                }
            )

        # 4. Launcher Row
        if ln:
            ln_sup = self.catalog.suppliers.get(ln.supplier_id)
            c_flag = country_with_flag(ln_sup.country if ln_sup else "")
            rows.append(
                {
                    "item": ln,
                    "cat": "🚀 Service de Lancement",
                    "name": f"{ln.name} ({ln.launcher_type})",
                    "supplier": f"{ln.supplier_name} [{c_flag}]",
                    "details": f"Orbite {cfg.orbit.orbit_type.value.upper()} @ {cfg.orbit.altitude_km:.0f} km | Capacité: {ln_cap:.0f} kg",
                    "mass": f"Masse au lancement: {m_launch:.1f} kg",
                    "power": "—",
                    "cost": f"{ln_cost:.2f} M€",
                    "bg": QColor(237, 233, 254),
                    "fg": QColor("#5b21b6"),
                    "bold": True,
                }
            )

        # 5. Subtotal Satellite Row
        if budgets:
            b = budgets
            rows.append(
                {
                    "item": None,
                    "cat": "🛰️ SOUS-TOTAL SATELLITE",
                    "name": "Ensemble plateforme + options + charges utiles + ergols",
                    "supplier": "Assiette retour géo ESA",
                    "details": f"Masse sèche: {b.mass.system_dry_mass_kg:.1f} kg + Ergols: {b.mass.propellant_mass_kg:.1f} kg",
                    "mass": f"{b.mass.system_wet_mass_kg:.1f} kg humide",
                    "power": f"Consom. moy: {b.power.total_avg_consumption_w:.1f} W",
                    "cost": f"{b.cost.satellite_cost_meur:.2f} M€",
                    "bg": QColor(224, 242, 254),
                    "fg": QColor("#0369a1"),
                    "bold": True,
                }
            )

            # 6. Grand Total Space Segment
            cost_status = f"(Marge: {b.cost.cost_margin_meur:+.2f} M€)"
            rows.append(
                {
                    "item": None,
                    "cat": "🌟 TOTAL SEGMENT SPATIAL",
                    "name": "Satellite complet avec lanceur & marge de lancement 20%",
                    "supplier": f"Plafond mission: {b.cost.mission_budget_limit_meur:.2f} M€",
                    "details": f"Marge de masse: +{b.mass.margin_pct:.0f}% | Marge puissance: {b.power.power_margin_pct:.0f}%",
                    "mass": f"{b.mass.launch_mass_with_margin_kg:.1f} kg lancement",
                    "power": f"Marge P: {b.power.power_margin_w:+.1f} W",
                    "cost": f"{b.cost.space_segment_total_meur:.2f} M€ {cost_status}",
                    "bg": QColor(220, 252, 231) if b.cost.cost_margin_meur >= 0 else QColor(254, 226, 226),
                    "fg": QColor("#14532d") if b.cost.cost_margin_meur >= 0 else QColor("#991b1b"),
                    "bold": True,
                }
            )

        self.table.setRowCount(len(rows))
        for row_idx, r in enumerate(rows):
            col_vals = [
                r["cat"],
                r["name"],
                r["supplier"],
                r["details"],
                r["mass"],
                r["power"],
                r["cost"],
            ]
            fg_color = r.get("fg", QColor("#0f172a"))
            for col_idx, val in enumerate(col_vals):
                item = QTableWidgetItem(val)
                if r["bold"]:
                    item.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
                item.setBackground(r["bg"])
                item.setForeground(fg_color)
                if r["item"]:
                    item.setData(Qt.ItemDataRole.UserRole, r["item"])
                self.table.setItem(row_idx, col_idx, item)

    def _country(self, supplier_id: str) -> str:
        sup = self.catalog.suppliers.get(supplier_id)
        return sup.country if sup else ""

    def _on_cell_double_clicked(self, row: int, _col: int) -> None:
        item_widget = self.table.item(row, 1)
        if not item_widget:
            return
        item_obj = item_widget.data(Qt.ItemDataRole.UserRole)
        if not item_obj:
            return

        orbit = self.project.configuration.orbit if self.project else None
        ds = build_datasheet(item_obj, self.catalog, orbit)
        DatasheetView.open_modal(ds, self)


class GlobalArchitectureDialog(QDialog):
    """Modal dialog displaying the complete space segment architecture overview."""

    def __init__(
        self,
        catalog: CatalogDatabase,
        project: StudentProject,
        budgets: SystemBudgets | None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Architecture Complète du Segment Spatial Sélectionné")
        self.resize(1100, 680)

        layout = QVBoxLayout(self)

        header_lbl = QLabel(
            f"<h2>Vue d'ensemble du Segment Spatial — {project.mission.title}</h2>"
            f"<p style='color:#475569;'>Visualisation globale de la plateforme, des charges utiles, des options configurées et du lanceur retenu.</p>"
        )
        layout.addWidget(header_lbl)

        self.widget = GlobalArchitectureWidget(catalog, project, budgets, self)
        layout.addWidget(self.widget, stretch=1)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_close = QPushButton("Fermer")
        btn_close.setStyleSheet("padding: 6px 18px; font-weight: bold;")
        btn_close.clicked.connect(self.accept)
        btn_row.addWidget(btn_close)
        layout.addLayout(btn_row)
