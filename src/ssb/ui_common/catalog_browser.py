"""Reusable Supplier → Catalog → Complete Datasheet browser widgets (PySide6)."""

from typing import Any, Callable
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QColor, QBrush, QFont
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QScrollArea,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from ssb.catalog.database import CatalogDatabase
from ssb.catalog.datasheet import build_datasheet, DatasheetData
from ssb.core.orbit import OrbitDefinition
from ssb.core.paths import images_dir
from ssb.ui_common.schematic import DimensionedSchematicWidget


class DatasheetView(QScrollArea):
    """Scrollable full datasheet view with illustration image, 3-view schematic, description and spec tables."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)

        self._container = QWidget()
        self._layout = QVBoxLayout(self._container)
        self._layout.setContentsMargins(10, 10, 10, 10)
        self._layout.setSpacing(10)
        self.setWidget(self._container)

        # Header banner
        header_frame = QFrame()
        header_frame.setStyleSheet(
            "QFrame { background: #0f2744; border: 1px solid #1e4976; border-radius: 6px; padding: 6px; }"
            "QLabel { color: #f8fafc; }"
        )
        hl = QHBoxLayout(header_frame)
        left_h = QVBoxLayout()
        self.lbl_title = QLabel("Sélectionnez un élément du catalogue")
        self.lbl_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        self.lbl_sub = QLabel("")
        self.lbl_sub.setStyleSheet("font-size: 12px; color: #93c5fd;")
        left_h.addWidget(self.lbl_title)
        left_h.addWidget(self.lbl_sub)
        hl.addLayout(left_h, stretch=1)

        right_h = QVBoxLayout()
        self.lbl_price = QLabel("")
        self.lbl_price.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lbl_price.setStyleSheet(
            "font-size: 15px; font-weight: bold; color: #fbbf24; background: #1e3a5f; padding: 4px 8px; border-radius: 4px;"
        )
        self.lbl_compat = QLabel("")
        self.lbl_compat.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lbl_compat.setWordWrap(True)
        right_h.addWidget(self.lbl_price)
        right_h.addWidget(self.lbl_compat)
        hl.addLayout(right_h)
        self._layout.addWidget(header_frame)

        # Visual row: illustration image + dimensioned 3-view schematic
        vis_row = QHBoxLayout()
        self.lbl_image = QLabel()
        self.lbl_image.setFixedSize(260, 185)
        self.lbl_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_image.setStyleSheet(
            "background: #0b192c; border: 1px solid #2c5a8f; border-radius: 4px; color: #94a3b8;"
        )
        self.schematic = DimensionedSchematicWidget()
        self.schematic.setFixedHeight(185)
        vis_row.addWidget(self.lbl_image)
        vis_row.addWidget(self.schematic, stretch=1)
        self._layout.addLayout(vis_row)

        # Descriptive text box
        desc_frame = QFrame()
        desc_frame.setStyleSheet(
            "QFrame { background: #f8fafc; color: #0f172a; border: 1px solid #cbd5e1; border-radius: 5px; padding: 6px; }"
            "QLabel { color: #0f172a; }"
        )
        dl = QVBoxLayout(desc_frame)
        lbl_d_hdr = QLabel("Description détaillée & positionnement")
        lbl_d_hdr.setStyleSheet("font-weight: bold; color: #1e3a8a; font-size: 12px;")
        self.lbl_desc = QLabel("")
        self.lbl_desc.setWordWrap(True)
        self.lbl_desc.setTextFormat(Qt.TextFormat.RichText)
        self.lbl_desc.setStyleSheet("font-size: 12px;")
        dl.addWidget(lbl_d_hdr)
        dl.addWidget(self.lbl_desc)
        self._layout.addWidget(desc_frame)

        # Dynamic tables container
        self._tables_box = QWidget()
        self._tables_layout = QVBoxLayout(self._tables_box)
        self._tables_layout.setContentsMargins(0, 0, 0, 0)
        self._tables_layout.setSpacing(8)
        self._layout.addWidget(self._tables_box)
        self._layout.addStretch(1)

    def set_datasheet(
        self,
        ds: DatasheetData,
        compat_status: tuple[bool, str] | None = None,
    ) -> None:
        self.lbl_title.setText(f"{ds.name}   [{ds.item_id}]")
        self.lbl_sub.setText(f"Fournisseur : {ds.supplier_name}   •   {ds.category_label}")
        self.lbl_price.setText(f"Prix : {ds.price_label}")

        if compat_status is not None:
            ok, msg = compat_status
            color = "#4ade80" if ok else "#f87171"
            self.lbl_compat.setStyleSheet(f"font-size: 11px; font-weight: bold; color: {color};")
            self.lbl_compat.setText(msg)
        else:
            self.lbl_compat.setText("")

        # Load illustration image
        img_path = images_dir() / ds.image if ds.image else None
        if img_path and img_path.exists():
            pix = QPixmap(str(img_path))
            self.lbl_image.setPixmap(
                pix.scaled(
                    self.lbl_image.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        else:
            self.lbl_image.setPixmap(QPixmap())
            self.lbl_image.setText("Illustration")

        self.schematic.set_item_geometry(ds.dimensions_mm, ds.name, ds.volume_label, ds.mass_label)

        # Build rich description + key features + interfaces
        parts = [f"<p style='margin-bottom:6px;'><b>Résumé :</b> {ds.short_description}</p>"]
        if ds.long_description and ds.long_description != ds.short_description:
            parts.append(f"<p style='margin-bottom:6px;'>{ds.long_description}</p>")
        if ds.key_features:
            bullets = "".join(f"<li>{f}</li>" for f in ds.key_features)
            parts.append(f"<b>Points clés :</b><ul style='margin-top:2px;margin-bottom:4px;'>{bullets}</ul>")
        if ds.interfaces:
            parts.append(f"<p style='margin-top:2px;'><b>Interfaces :</b> {'  •  '.join(ds.interfaces)}</p>")
        self.lbl_desc.setText("".join(parts))

        # Rebuild section tables
        while self._tables_layout.count():
            child = self._tables_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for sec in ds.sections:
            if not sec.rows:
                continue
            sec_lbl = QLabel(sec.title)
            sec_lbl.setStyleSheet(
                "font-weight: bold; font-size: 12px; color: #0f2744; margin-top: 4px;"
            )
            self._tables_layout.addWidget(sec_lbl)

            tbl = QTableWidget(len(sec.rows), 2)
            tbl.setStyleSheet("""
                QTableWidget {
                    background-color: #ffffff;
                    color: #0f172a;
                    gridline-color: #cbd5e1;
                    font-size: 12px;
                    alternate-background-color: #f8fafc;
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
                }
            """)
            tbl.setHorizontalHeaderLabels(["Paramètre", "Valeur"])
            tbl.verticalHeader().setVisible(False)
            tbl.setWordWrap(True)
            tbl.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            tbl.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
            tbl.setAlternatingRowColors(True)
            tbl.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
            tbl.setColumnWidth(0, 290)
            tbl.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            for r, (k, v) in enumerate(sec.rows):
                k_item = QTableWidgetItem(k)
                k_item.setForeground(QColor("#0f172a"))
                f = QFont()
                f.setBold(True)
                k_item.setFont(f)
                v_item = QTableWidgetItem(v)
                v_item.setForeground(QColor("#0f172a"))
                tbl.setItem(r, 0, k_item)
                tbl.setItem(r, 1, v_item)
                tbl.setRowHeight(r, 24)
            h_total = 28 + 24 * len(sec.rows) + 6
            tbl.setFixedHeight(min(360, max(76, h_total)))
            self._tables_layout.addWidget(tbl)


class CatalogBrowser(QWidget):
    """Three-column browser: Suppliers -> Supplier's catalog items -> Complete Datasheet + action button."""

    item_activated = Signal(object)

    def __init__(
        self,
        catalog: CatalogDatabase,
        category: str,
        action_button_text: str = "Sélectionner cet élément",
        type_filter_options: list[tuple[str, str]] | None = None,
        compatibility_fn: Callable[[Any], tuple[bool, str]] | None = None,
        orbit_provider: Callable[[], OrbitDefinition] | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.catalog = catalog
        self.category = category
        self.compatibility_fn = compatibility_fn
        self.orbit_provider = orbit_provider
        self._current_item: Any = None

        root = QVBoxLayout(self)
        root.setContentsMargins(4, 4, 4, 4)

        # Top filter bar
        fbar = QHBoxLayout()
        fbar.addWidget(QLabel("Recherche :"))
        self.ed_search = QLineEdit()
        self.ed_search.setPlaceholderText("Filtrer par nom, description, bande, technologie...")
        self.ed_search.textChanged.connect(self._refresh_items)
        fbar.addWidget(self.ed_search, stretch=1)

        self.cmb_type: QComboBox | None = None
        if type_filter_options:
            fbar.addWidget(QLabel("Sous-catégorie :"))
            self.cmb_type = QComboBox()
            self.cmb_type.addItem("Toutes les sous-catégories", "")
            for code, lbl in type_filter_options:
                self.cmb_type.addItem(lbl, code)
            self.cmb_type.currentIndexChanged.connect(self._refresh_suppliers)
            fbar.addWidget(self.cmb_type)

        self.btn_action = QPushButton(action_button_text)
        self.btn_action.setStyleSheet(
            "QPushButton { background: #1d4ed8; color: white; font-weight: bold; padding: 6px 14px; border-radius: 4px; }"
            "QPushButton:hover { background: #2563eb; }"
            "QPushButton:disabled { background: #94a3b8; }"
        )
        self.btn_action.setEnabled(False)
        self.btn_action.clicked.connect(self._on_action_clicked)
        fbar.addWidget(self.btn_action)
        root.addLayout(fbar)

        # 3-pane splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Pane 1: Suppliers
        sup_box = QWidget()
        sup_l = QVBoxLayout(sup_box)
        sup_l.setContentsMargins(0, 0, 0, 0)
        lbl_s = QLabel("1. Fournisseurs")
        lbl_s.setStyleSheet("font-weight: bold; color: #0f2744;")
        sup_l.addWidget(lbl_s)
        list_style = """
            QListWidget {
                background-color: #ffffff;
                color: #0f172a;
                border: 1px solid #cbd5e1;
                border-radius: 4px;
                font-size: 12px;
            }
            QListWidget::item {
                color: #0f172a;
                padding: 4px;
            }
            QListWidget::item:selected {
                background-color: #2563eb;
                color: #ffffff;
            }
            QListWidget::item:hover {
                background-color: #f1f5f9;
                color: #0f172a;
            }
        """
        self.list_suppliers = QListWidget()
        self.list_suppliers.setStyleSheet(list_style)
        self.list_suppliers.currentItemChanged.connect(self._on_supplier_changed)
        sup_l.addWidget(self.list_suppliers, stretch=1)
        self.lbl_supplier_info = QLabel("Sélectionnez un fournisseur pour afficher son profil et son catalogue.")
        self.lbl_supplier_info.setWordWrap(True)
        self.lbl_supplier_info.setStyleSheet(
            "background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 4px; padding: 6px; font-size: 11px; color: #1e293b;"
        )
        sup_l.addWidget(self.lbl_supplier_info)
        splitter.addWidget(sup_box)

        # Pane 2: Items of selected supplier
        item_box = QWidget()
        item_l = QVBoxLayout(item_box)
        item_l.setContentsMargins(0, 0, 0, 0)
        self.lbl_items_header = QLabel("2. Catalogue du fournisseur")
        self.lbl_items_header.setStyleSheet("font-weight: bold; color: #0f2744;")
        item_l.addWidget(self.lbl_items_header)
        self.list_items = QListWidget()
        self.list_items.setStyleSheet(list_style)
        self.list_items.currentItemChanged.connect(self._on_item_changed)
        self.list_items.itemDoubleClicked.connect(lambda _: self._on_action_clicked())
        item_l.addWidget(self.list_items, stretch=1)
        splitter.addWidget(item_box)

        # Pane 3: Complete Datasheet
        self.datasheet_view = DatasheetView()
        splitter.addWidget(self.datasheet_view)

        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)
        splitter.setStretchFactor(2, 6)
        root.addWidget(splitter, stretch=1)

        self._refresh_suppliers()

    def _pool(self) -> list[Any]:
        mapping = {
            "platform": list(self.catalog.platforms.values()),
            "payload": list(self.catalog.payloads.values()),
            "equipment": list(self.catalog.equipments.values()),
            "launcher": list(self.catalog.launchers.values()),
        }
        items = mapping[self.category]
        if self.cmb_type and self.cmb_type.currentData():
            code = self.cmb_type.currentData()
            if self.category == "payload":
                items = [x for x in items if x.payload_type.value == code]
            elif self.category == "equipment":
                items = [x for x in items if x.function.value == code]
            elif self.category == "platform":
                items = [x for x in items if code in x.category]
            elif self.category == "launcher":
                items = [x for x in items if x.launcher_type == code]
        return items

    def _refresh_suppliers(self) -> None:
        prev_sup = self.list_suppliers.currentItem().data(Qt.ItemDataRole.UserRole) if self.list_suppliers.currentItem() else None
        self.list_suppliers.blockSignals(True)
        self.list_suppliers.clear()

        pool = self._pool()
        all_item = QListWidgetItem(f"Tous les fournisseurs ({len(pool)} réf.)")
        all_item.setData(Qt.ItemDataRole.UserRole, "__ALL__")
        f = QFont()
        f.setBold(True)
        all_item.setFont(f)
        self.list_suppliers.addItem(all_item)

        for sup in self.catalog.suppliers_for(self.category):
            cnt = sum(1 for x in pool if x.supplier_id == sup.id)
            if cnt == 0:
                continue
            badge = "Historique" if sup.kind == "historique" else "NewSpace"
            it = QListWidgetItem(f"{sup.name} ({cnt})\n   [{badge} — {sup.country}]")
            it.setData(Qt.ItemDataRole.UserRole, sup.id)
            self.list_suppliers.addItem(it)

        self.list_suppliers.blockSignals(False)
        target_row = 0
        if prev_sup:
            for i in range(self.list_suppliers.count()):
                if self.list_suppliers.item(i).data(Qt.ItemDataRole.UserRole) == prev_sup:
                    target_row = i
                    break
        self.list_suppliers.setCurrentRow(target_row)
        self._on_supplier_changed(self.list_suppliers.currentItem(), None)

    def _on_supplier_changed(self, current: QListWidgetItem | None, _prev: QListWidgetItem | None) -> None:
        if not current:
            return
        sup_id = current.data(Qt.ItemDataRole.UserRole)
        if sup_id == "__ALL__":
            self.lbl_supplier_info.setText(
                "<b>Vue globale :</b> tous les fournisseurs du catalogue sont affichés. "
                "Cliquez sur un fournisseur particulier pour lire son profil industriel et filtrer ses produits."
            )
            self.lbl_items_header.setText("2. Tous les produits du catalogue")
        else:
            sup = self.catalog.suppliers[sup_id]
            kind = "Acteur historique / institutionnel" if sup.kind == "historique" else "Acteur NewSpace"
            self.lbl_supplier_info.setText(
                f"<b>{sup.name}</b> ({sup.country})<br>"
                f"<i>{kind} — fondé en {sup.founded or 'N/A'}</i><br>{sup.description}"
            )
            self.lbl_items_header.setText(f"2. Catalogue de {sup.name}")
        self._refresh_items()

    def _refresh_items(self) -> None:
        prev_id = self._current_item.id if self._current_item else None
        sup_item = self.list_suppliers.currentItem()
        sup_id = sup_item.data(Qt.ItemDataRole.UserRole) if sup_item else "__ALL__"
        q = self.ed_search.text().strip().lower()

        items = self._pool()
        if sup_id != "__ALL__":
            items = [x for x in items if x.supplier_id == sup_id]
        if q:
            items = [
                x
                for x in items
                if q in x.name.lower()
                or q in x.description.lower()
                or q in x.long_description.lower()
                or q in x.supplier_name.lower()
                or q in x.id.lower()
            ]

        self.list_items.blockSignals(True)
        self.list_items.clear()
        restore_row = 0
        for idx, x in enumerate(items):
            summary = self._item_summary_line(x)
            compat_tag = ""
            compat_ok = True
            if self.compatibility_fn is not None:
                compat_ok, compat_reason = self.compatibility_fn(x)
                compat_tag = f"\n   {'✔ ' if compat_ok else '⚠ '}{compat_reason}"
            li = QListWidgetItem(f"{x.name}  —  {summary}{compat_tag}")
            li.setData(Qt.ItemDataRole.UserRole, x)
            if not compat_ok:
                li.setForeground(QBrush(QColor("#b91c1c")))
            self.list_items.addItem(li)
            if x.id == prev_id:
                restore_row = idx
        self.list_items.blockSignals(False)

        if self.list_items.count() > 0:
            self.list_items.setCurrentRow(restore_row)
            self._on_item_changed(self.list_items.currentItem(), None)
        else:
            self._current_item = None
            self.btn_action.setEnabled(False)

    def _item_summary_line(self, x: Any) -> str:
        if self.category == "platform":
            return f"{x.base_price_meur:.2f} M€ | CU max {x.max_payload_mass_kg:.0f} kg / {x.payload_volume_liters:.0f} L | {x.payload_avg_power_w:.0f} W"
        if self.category == "payload":
            return f"{x.price_meur:.2f} M€ | {x.mass_kg:.1f} kg | {x.volume_liters:.0f} L | {x.operational_power_w:.0f} W"
        if self.category == "equipment":
            return f"{x.price_meur:.2f} M€ | {x.mass_kg:.1f} kg | {x.volume_liters:.1f} L | {x.power_w:.0f} W"
        if self.category == "launcher":
            return f"{x.price_base_meur:.2f} M€ | max {x.max_total_mass_kg:.0f} kg ({x.launcher_type})"
        return ""

    def _on_item_changed(self, current: QListWidgetItem | None, _prev: QListWidgetItem | None) -> None:
        if not current:
            return
        item = current.data(Qt.ItemDataRole.UserRole)
        self._current_item = item
        self.btn_action.setEnabled(True)
        orbit = self.orbit_provider() if self.orbit_provider else None
        ds = build_datasheet(item, orbit)
        compat = self.compatibility_fn(item) if self.compatibility_fn else None
        self.datasheet_view.set_datasheet(ds, compat)

    def _on_action_clicked(self) -> None:
        if self._current_item is not None:
            self.item_activated.emit(self._current_item)

    def refresh(self) -> None:
        """Re-evaluate compatibility badges and current datasheet (e.g. when orbit or payloads change)."""
        self._refresh_items()

    def select_item_by_id(self, item_id: str) -> None:
        self.list_suppliers.setCurrentRow(0)
        for i in range(self.list_items.count()):
            it = self.list_items.item(i)
            obj = it.data(Qt.ItemDataRole.UserRole)
            if obj and obj.id == item_id:
                self.list_items.setCurrentRow(i)
                return
