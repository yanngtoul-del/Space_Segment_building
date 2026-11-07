"""Unit tests for the enriched multi-supplier catalogs, datasheets, and offscreen GUI rendering."""

import os
from ssb.catalog.database import CatalogDatabase
from ssb.catalog.datasheet import build_datasheet
from ssb.core.paths import catalogs_dir, images_dir
from ssb.core.orbit import OrbitDefinition


def test_enriched_catalog_counts_and_datasheets():
    db = CatalogDatabase()
    db.load_from_directory(catalogs_dir())

    assert len(db.suppliers) >= 18
    assert len(db.platforms) >= 16
    assert len(db.payloads) >= 33
    assert len(db.equipments) >= 31
    assert len(db.launchers) >= 8

    # Every platform supplier must have multiple platforms in its catalog
    plat_suppliers = db.suppliers_for("platform")
    assert len(plat_suppliers) == 5
    for sup in plat_suppliers:
        items = db.items_by_supplier(sup.id, "platform")
        assert len(items) >= 3, f"Supplier {sup.id} should have at least 3 platforms"

    # Every item across all 4 catalogs must have a valid image, descriptive text, and buildable datasheet
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


def test_student_and_teacher_gui_offscreen():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtWidgets import QApplication
    from ssb.student_app.main_window import StudentMainWindow
    from ssb.teacher_app.main_window import TeacherMainWindow

    app = QApplication.instance() or QApplication([])
    win = StudentMainWindow()
    assert win.current_budgets is not None
    assert win.browser_payloads.list_suppliers.count() > 5
    assert win.browser_platforms.list_suppliers.count() == 6  # "Tous" + 5 platform suppliers

    # Select a specific supplier in the payload browser and verify its catalog populates
    win.browser_payloads.list_suppliers.setCurrentRow(1)
    assert win.browser_payloads.list_items.count() >= 1

    # Add a second payload and verify multi-payload evaluation works
    second_pl = win.catalog.payloads["pl_opt_comm_terminal_10g"]
    win._add_payload_from_browser(second_pl)
    assert len(win.project.configuration.selected_payload_ids) == 2
    assert "pl_opt_comm_terminal_10g" in win.current_budgets.payload_performances

    twin = TeacherMainWindow()
    assert twin.tabs.count() == 3
    win.close()
    twin.close()
    assert app is not None
