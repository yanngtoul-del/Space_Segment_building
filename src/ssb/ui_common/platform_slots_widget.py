"""Interactive platform slot & option configurator widget implementing rules D15–D21."""

from typing import Callable
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QBrush, QFont
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QSpinBox,
    QDialog,
    QPushButton,
)
from ssb.catalog.database import CatalogDatabase
from ssb.catalog.datasheet import build_datasheet, FUNCTION_LABELS_FR
from ssb.core.platform import PlatformBase, SlotRule, Equipment
from ssb.core.project import SelectedOption
from ssb.ui_common.catalog_browser import DatasheetView


class PlatformSlotsWidget(QWidget):
    """Displays all subsystem slots of the selected platform, allowed & greyed-out options, surcharges, and quantities."""

    options_changed = Signal()

    def __init__(self, catalog: CatalogDatabase, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.catalog = catalog
        self._platform: PlatformBase | None = None
        self._spinners: list[tuple[str, str, QSpinBox, SlotRule]] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        self.lbl_header = QLabel("<b>Configuration des sous-systèmes & options de la plateforme</b>")
        layout.addWidget(self.lbl_header)

        self.lbl_rules = QLabel(
            "Règles : un équipement <b>inclus de base</b> coûte 0 M€ supplémentaire (le retirer ne donne aucun crédit). "
            "Une option payante ajoute son prix (éventuellement spécifique à la plateforme) + les frais d'intégration du slot. "
            "Double-cliquez sur une ligne pour ouvrir la datasheet complète de l'équipement."
        )
        self.lbl_rules.setWordWrap(True)
        self.lbl_rules.setStyleSheet("font-size: 11px; color: #334155;")
        layout.addWidget(self.lbl_rules)

        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(
            [
                "Sous-système (Slot)",
                "Qté slot",
                "Équipement",
                "Fournisseur",
                "Statut sur cette plateforme",
                "Masse (+interf.)",
                "Puissance",
                "Surcoût / unité",
            ]
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)
        self.table.cellDoubleClicked.connect(self._on_row_double_clicked)
        layout.addWidget(self.table, stretch=1)

    def set_platform(
        self,
        platform: PlatformBase,
        selected_options: list[SelectedOption] | None = None,
    ) -> None:
        self._platform = platform
        self._spinners.clear()
        self.lbl_header.setText(
            f"<b>Options & sous-systèmes pour {platform.name}</b> "
            f"(prix de base : {platform.base_price_meur:.2f} M€, masse sèche : {platform.dry_mass_kg:.1f} kg)"
        )

        # Map existing selections if provided, otherwise default to included equipment
        sel_map: dict[tuple[str, str], int] = {}
        if selected_options:
            for opt in selected_options:
                sel_map[(opt.slot_function, opt.equipment_id)] = opt.quantity
        else:
            for slot in platform.slots:
                for inc_id in slot.included_equipment_ids:
                    sel_map[(slot.function.value, inc_id)] = 1

        slots_by_fn = {s.function.value: s for s in platform.slots}

        # Build rows: first all allowed equipments per slot, then unavailable equipments (greyed out with reason D20)
        rows_data: list[tuple[SlotRule | None, Equipment, bool, str]] = []
        for slot in platform.slots:
            for eq_id in slot.allowed_equipment_ids:
                eq = self.catalog.equipments[eq_id]
                is_inc = eq_id in slot.included_equipment_ids
                status_txt = "Inclus de base (0 M€)" if is_inc else "Option compatible"
                rows_data.append((slot, eq, True, status_txt))

        # Add greyed-out incompatible equipments from catalog so student sees why they can't pick them (D20)
        for eq in self.catalog.equipments.values():
            fn = eq.function.value
            slot = slots_by_fn.get(fn)
            if slot and eq.id in slot.allowed_equipment_ids:
                continue
            reason = self._incompatibility_reason(platform, eq)
            rows_data.append((slot, eq, False, f"Indisponible — {reason}"))

        self.table.setRowCount(len(rows_data))
        for r, (slot, eq, allowed, status_txt) in enumerate(rows_data):
            fn_lbl = FUNCTION_LABELS_FR.get(eq.function.value, eq.function.value)
            if slot is not None:
                fn_lbl += f" (min {slot.min_qty} / max {slot.max_qty})"

            it_fn = QTableWidgetItem(fn_lbl)
            it_name = QTableWidgetItem(eq.name)
            it_name.setData(Qt.ItemDataRole.UserRole, eq.id)
            it_sup = QTableWidgetItem(eq.supplier_name)
            it_stat = QTableWidgetItem(status_txt)

            if allowed and slot is not None:
                ov = slot.equipment_overrides.get(eq.id, {})
                base_p = ov.get("price_meur", eq.price_meur)
                base_m = ov.get("mass_kg", eq.mass_kg)
                is_inc = eq.id in slot.included_equipment_ids
                if is_inc:
                    surch_str = "0,00 M€ (inclus)"
                    eff_m = base_m
                else:
                    integ = slot.integration_cost_fixed_meur + base_p * (slot.integration_cost_pct / 100.0)
                    tot_p = base_p + integ
                    surch_str = f"+{tot_p:.2f} M€ (éq. {base_p:.2f} + intég. {integ:.2f})"
                    eff_m = base_m + slot.interface_mass_kg
                mass_str = f"{eff_m:.1f} kg"
                if eq.function.value == "propulsion" and "propellant_mass_kg" in eq.specs:
                    mass_str += f" (+{eq.specs['propellant_mass_kg']:.1f} kg ergol)"
                pwr_str = f"{eq.power_w:.0f} W (pic {eq.peak_power_w:.0f} W)"

                sp = QSpinBox()
                sp.setRange(0, slot.max_qty)
                sp.setValue(sel_map.get((slot.function.value, eq.id), 0))
                sp.valueChanged.connect(self._on_spin_changed)
                self.table.setCellWidget(r, 1, sp)
                self._spinners.append((slot.function.value, eq.id, sp, slot))

                if is_inc:
                    it_stat.setForeground(QBrush(QColor("#15803d")))
                    f = QFont()
                    f.setBold(True)
                    it_stat.setFont(f)
            else:
                mass_str = f"{eq.mass_kg:.1f} kg"
                pwr_str = f"{eq.power_w:.0f} W"
                surch_str = f"({eq.price_meur:.2f} M€ cat.)"
                it_qty = QTableWidgetItem("—")
                it_qty.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(r, 1, it_qty)

            it_mass = QTableWidgetItem(mass_str)
            it_pwr = QTableWidgetItem(pwr_str)
            it_cost = QTableWidgetItem(surch_str)

            for c_idx, cell in [
                (0, it_fn),
                (2, it_name),
                (3, it_sup),
                (4, it_stat),
                (5, it_mass),
                (6, it_pwr),
                (7, it_cost),
            ]:
                if not allowed:
                    cell.setForeground(QBrush(QColor("#94a3b8")))
                    cell.setBackground(QBrush(QColor("#f1f5f9")))
                self.table.setItem(r, c_idx, cell)

    def _incompatibility_reason(self, plat: PlatformBase, eq: Equipment) -> str:
        if eq.mass_kg > plat.dry_mass_kg * 0.6:
            return f"Masse ({eq.mass_kg:.1f} kg) disproportionnée pour {plat.name}"
        if eq.power_w > plat.orbit_avg_power_w * 0.8:
            return f"Puissance ({eq.power_w:.0f} W) supérieure à la capacité du bus ({plat.orbit_avg_power_w:.0f} W)"
        if plat.bus_voltage_v < 28.0 and eq.power_w > 20.0:
            return f"Requiert un bus ≥ 28 V (bus {plat.name} : {plat.bus_voltage_v:.0f} V)"
        return f"Interface non qualifiée sur la plateforme {plat.name}"

    def _on_spin_changed(self, _val: int) -> None:
        self.options_changed.emit()

    def selected_options(self) -> list[SelectedOption]:
        out: list[SelectedOption] = []
        for fn, eq_id, sp, _slot in self._spinners:
            if sp.value() > 0:
                out.append(SelectedOption(slot_function=fn, equipment_id=eq_id, quantity=sp.value()))
        return out

    def _on_row_double_clicked(self, row: int, _col: int) -> None:
        it = self.table.item(row, 2)
        if not it:
            return
        eq_id = it.data(Qt.ItemDataRole.UserRole)
        if eq_id and eq_id in self.catalog.equipments:
            eq = self.catalog.equipments[eq_id]
            dlg = QDialog(self)
            dlg.setWindowTitle(f"Datasheet Équipement — {eq.name}")
            dlg.resize(820, 620)
            vl = QVBoxLayout(dlg)
            view = DatasheetView()
            view.set_datasheet(build_datasheet(eq))
            vl.addWidget(view, stretch=1)
            btn = QPushButton("Fermer")
            btn.clicked.connect(dlg.accept)
            vl.addWidget(btn)
            dlg.exec()
