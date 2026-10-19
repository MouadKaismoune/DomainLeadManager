"""Small, crisp line icons drawn with QPainter (no external icon set)."""

from PySide6.QtCore import QRectF, QSize, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPainterPath, QPen, QPixmap
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget

DEFAULT_COLOR = "#64748B"
PRIMARY_COLOR = "#FFFFFF"
DANGER_COLOR = "#DC2626"


def line_icon(kind: str, color: str = DEFAULT_COLOR, size: int = 20) -> QIcon:
    """Draw a monochrome 24x24 line icon and return it as a QIcon."""
    scale = 4
    pixmap = QPixmap(size * scale, size * scale)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.scale(size * scale / 24.0, size * scale / 24.0)
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.setPen(
        QPen(
            QColor(color),
            1.8,
            Qt.PenStyle.SolidLine,
            Qt.PenCapStyle.RoundCap,
            Qt.PenJoinStyle.RoundJoin,
        )
    )

    if kind == "plus":
        painter.drawLine(12, 4, 12, 20)
        painter.drawLine(4, 12, 20, 12)
    elif kind == "edit":
        path = QPainterPath()
        path.moveTo(5, 19)
        path.lineTo(6, 14.5)
        path.lineTo(15.5, 5)
        path.lineTo(19, 8.5)
        path.lineTo(9.5, 18)
        path.closeSubpath()
        painter.drawPath(path)
        painter.drawLine(14.5, 6, 18, 9.5)
    elif kind == "trash":
        painter.drawLine(4, 7, 20, 7)
        painter.drawLine(9, 7, 9, 4.5)
        painter.drawLine(9, 4.5, 15, 4.5)
        painter.drawLine(15, 4.5, 15, 7)
        body = QPainterPath()
        body.moveTo(6.5, 7)
        body.lineTo(7.4, 19)
        body.quadTo(7.5, 20, 8.6, 20)
        body.lineTo(15.4, 20)
        body.quadTo(16.5, 20, 16.6, 19)
        body.lineTo(17.5, 7)
        painter.drawPath(body)
        painter.drawLine(10, 10.5, 10, 16.5)
        painter.drawLine(14, 10.5, 14, 16.5)
    elif kind == "check":
        painter.drawLine(4.5, 12.5, 9.5, 17.5)
        painter.drawLine(9.5, 17.5, 19.5, 6.5)
    elif kind == "close":
        painter.drawLine(6, 6, 18, 18)
        painter.drawLine(18, 6, 6, 18)
    elif kind == "search":
        painter.drawEllipse(QRectF(4, 4, 11, 11))
        painter.drawLine(15.5, 15.5, 20, 20)
    elif kind == "globe":
        painter.drawEllipse(QRectF(3.5, 3.5, 17, 17))
        painter.drawEllipse(QRectF(8.5, 3.5, 7, 17))
        painter.drawLine(3.5, 12, 20.5, 12)
    elif kind == "sun":
        painter.drawEllipse(QRectF(8, 8, 8, 8))
        for x1, y1, x2, y2 in (
            (12, 1.5, 12, 4.5),
            (12, 19.5, 12, 22.5),
            (1.5, 12, 4.5, 12),
            (19.5, 12, 22.5, 12),
            (4.6, 4.6, 6.7, 6.7),
            (17.3, 17.3, 19.4, 19.4),
            (17.3, 6.7, 19.4, 4.6),
            (4.6, 19.4, 6.7, 17.3),
        ):
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))
    elif kind == "moon":
        outer = QPainterPath()
        outer.addEllipse(QRectF(4, 3, 17, 17))
        inner = QPainterPath()
        inner.addEllipse(QRectF(9.5, 0.5, 16, 16))
        painter.drawPath(outer.subtracted(inner))
    elif kind == "inbox":
        painter.drawRoundedRect(QRectF(4, 4, 16, 16), 3, 3)
        path = QPainterPath()
        path.moveTo(4, 13)
        path.lineTo(8, 13)
        path.lineTo(10, 16)
        path.lineTo(14, 16)
        path.lineTo(16, 13)
        path.lineTo(20, 13)
        painter.drawPath(path)
    else:  # chevron-down
        painter.drawLine(6, 9, 12, 15)
        painter.drawLine(12, 15, 18, 9)

    painter.end()
    return QIcon(pixmap)


def icon_button(
    parent: QWidget,
    icon: str,
    tooltip: str,
    role: str = "ghost",
    color: str | None = None,
    size: int = 32,
) -> QPushButton:
    """Create a compact icon-only button with a tooltip and accessible name."""
    if color is None:
        if role == "primary":
            color = PRIMARY_COLOR
        elif role == "danger":
            color = DANGER_COLOR
        else:
            color = DEFAULT_COLOR
    button = QPushButton(parent)
    button.setIcon(line_icon(icon, color, 20))
    button.setIconSize(QSize(18, 18))
    button.setToolTip(tooltip)
    button.setAccessibleName(tooltip)
    button.setCursor(Qt.CursorShape.PointingHandCursor)
    button.setFixedSize(size, size)
    button.setProperty("role", role)
    return button


def centered_table_button(
    parent: QWidget,
    icon: str,
    tooltip: str,
    color: str = DEFAULT_COLOR,
) -> QWidget:
    """Return a cell widget that centers a compact action button."""
    container = QWidget(parent)
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    button = icon_button(container, icon, tooltip, size=30, color=color)
    layout.addWidget(button)
    return container
