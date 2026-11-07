"""Procedural dimensioned schematic widget (3-view + isometric envelope) for datasheets."""

from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QFont, QPolygonF
from PySide6.QtWidgets import QWidget


class DimensionedSchematicWidget(QWidget):
    """Draws a clean technical blueprint with L × W × H dimensions and scale."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMinimumSize(280, 175)
        self._dims_mm: tuple[float, float, float] = (300.0, 200.0, 200.0)
        self._title: str = ""
        self._volume_str: str = ""
        self._mass_str: str = ""

    def set_item_geometry(
        self,
        dims_mm: tuple[float, float, float],
        title: str = "",
        volume_str: str = "",
        mass_str: str = "",
    ) -> None:
        if dims_mm and any(dims_mm):
            self._dims_mm = dims_mm
        else:
            self._dims_mm = (300.0, 200.0, 200.0)
        self._title = title
        self._volume_str = volume_str
        self._mass_str = mass_str
        self.update()

    def paintEvent(self, _event) -> None:  # noqa: N802
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        # Blueprint background
        p.fillRect(0, 0, w, h, QColor("#0c1f36"))
        grid_pen = QPen(QColor("#17375e"), 1)
        p.setPen(grid_pen)
        for x in range(0, w, 18):
            p.drawLine(x, 0, x, h)
        for y in range(0, h, 18):
            p.drawLine(0, y, w, y)

        p.setPen(QPen(QColor("#2c5a8f"), 1.5))
        p.drawRect(1, 1, w - 2, h - 2)

        lx, ly, lz = [max(10.0, float(v)) for v in self._dims_mm]
        mmax = max(lx, ly, lz)

        # Left half: Front (L × H) and Side (l × H) orthographic views
        avail_w = w * 0.56 - 24
        avail_h = h - 54
        scale = min(avail_w / (lx + ly + 0.25 * mmax), avail_h / lz)
        fw, fh = max(24.0, lx * scale), max(24.0, lz * scale)
        sw = max(20.0, ly * scale)

        x0 = 18.0
        y0 = 28.0 + (avail_h - fh) / 2.0

        box_pen = QPen(QColor("#58c4ff"), 1.8)
        fill_brush = QBrush(QColor(30, 90, 150, 95))
        p.setPen(box_pen)
        p.setBrush(fill_brush)

        front_rect = QRectF(x0, y0, fw, fh)
        side_rect = QRectF(x0 + fw + 18.0, y0, sw, fh)
        p.drawRect(front_rect)
        p.drawRect(side_rect)

        # Center crosshairs on front view
        dash_pen = QPen(QColor("#3b82c4"), 1, Qt.PenStyle.DashLine)
        p.setPen(dash_pen)
        p.drawLine(QPointF(front_rect.left(), front_rect.center().y()), QPointF(front_rect.right(), front_rect.center().y()))
        p.drawLine(QPointF(front_rect.center().x(), front_rect.top()), QPointF(front_rect.center().x(), front_rect.bottom()))

        # Isometric 3D box on the right
        iso_cx = w * 0.78
        iso_cy = h * 0.50
        s3 = min(w * 0.34, h * 0.58) / (mmax * 1.45)
        dx, dy, dz = max(14.0, lx * s3), max(12.0, ly * s3), max(14.0, lz * s3)
        c30, s30 = 0.866, 0.5

        def iso(ix: float, iy: float, iz: float) -> QPointF:
            px = iso_cx + (ix - iy) * c30 * 0.55
            py = iso_cy + (ix + iy) * s30 * 0.55 - iz * 0.75
            return QPointF(px, py)

        p000 = iso(-dx / 2, -dy / 2, -dz / 2)
        p100 = iso(dx / 2, -dy / 2, -dz / 2)
        p110 = iso(dx / 2, dy / 2, -dz / 2)
        p010 = iso(-dx / 2, dy / 2, -dz / 2)
        p001 = iso(-dx / 2, -dy / 2, dz / 2)
        p101 = iso(dx / 2, -dy / 2, dz / 2)
        p111 = iso(dx / 2, dy / 2, dz / 2)
        p011 = iso(-dx / 2, dy / 2, dz / 2)

        p.setPen(box_pen)
        p.setBrush(QBrush(QColor(56, 189, 248, 70)))
        p.drawPolygon(QPolygonF([p001, p101, p111, p011]))
        p.setBrush(QBrush(QColor(14, 116, 180, 90)))
        p.drawPolygon(QPolygonF([p100, p110, p111, p101]))
        p.setBrush(QBrush(QColor(12, 74, 130, 105)))
        p.drawPolygon(QPolygonF([p010, p110, p111, p011]))

        # Dimension labels
        font = QFont("Segoe UI", 8)
        p.setFont(font)
        p.setPen(QColor("#fbbf24"))
        p.drawText(QRectF(front_rect.left(), front_rect.bottom() + 2, front_rect.width(), 16), Qt.AlignmentFlag.AlignCenter, f"L={lx:.0f} mm")
        p.drawText(QRectF(side_rect.left(), side_rect.bottom() + 2, side_rect.width(), 16), Qt.AlignmentFlag.AlignCenter, f"l={ly:.0f} mm")
        p.drawText(QRectF(front_rect.left(), front_rect.top() - 15, front_rect.width() + side_rect.width() + 18, 14), Qt.AlignmentFlag.AlignLeft, f"H={lz:.0f} mm")

        # Header & footer
        font_b = QFont("Segoe UI", 8, QFont.Weight.Bold)
        p.setFont(font_b)
        p.setPen(QColor("#e2e8f0"))
        p.drawText(8, 14, "SCHÉMA DIMENSIONNEL (3 VUES + ENVELOPPE 3D)")
        p.setFont(font)
        p.setPen(QColor("#93c5fd"))
        footer = f"Dimensions : {lx:.0f} × {ly:.0f} × {lz:.0f} mm"
        if self._volume_str:
            footer += f"   |   {self._volume_str}"
        if self._mass_str:
            footer += f"   |   {self._mass_str}"
        p.drawText(8, h - 6, footer)
        p.end()
