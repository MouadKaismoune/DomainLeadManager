"""Application theme: light/dark palettes and a shared Qt stylesheet."""

from string import Template

from PySide6.QtCore import QSettings
from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import QApplication

SETTINGS_ORG = "DomainLeadManager"
SETTINGS_APP = "DomainLeadManager"
THEME_SETTING = "ui/theme"

# Core palette for the default (light) mode. Kept short and consistent.
BACKGROUND = "#F5F7FA"
SURFACE = "#FFFFFF"
SIDEBAR = "#0F172A"
SIDEBAR_SURFACE = "#1E293B"
PRIMARY = "#315F85"
PRIMARY_HOVER = "#274F6E"
PRIMARY_PRESSED = "#1F3F58"
TEXT = "#0F172A"
TEXT_SECONDARY = "#64748B"
BORDER = "#E2E8F0"
ACCENT = "#60A5FA"

LIGHT = {
    "bg": "#F5F7FA",
    "surface": "#FFFFFF",
    "surface_alt": "#FAFBFD",
    "sidebar": "#0F172A",
    "sidebar_border": "#1E293B",
    "primary": "#315F85",
    "primary_hover": "#274F6E",
    "primary_pressed": "#1F3F58",
    "primary_text": "#FFFFFF",
    "text": "#0F172A",
    "text_secondary": "#64748B",
    "border": "#E2E8F0",
    "border_strong": "#CBD5E1",
    "accent": "#60A5FA",
    "tab_active": "#315F85",
    "input_bg": "#FFFFFF",
    "input_border": "#E2E8F0",
    "focus": "#315F85",
    "input_disabled_bg": "#F8FAFC",
    "input_disabled_text": "#94A3B8",
    "selection_bg": "#DBEAFE",
    "selection_text": "#0F172A",
    "combo_selection_bg": "#E8F1F8",
    "combo_selection_text": "#0F172A",
    "table_text": "#334155",
    "table_header": "#F8FAFC",
    "table_header_text": "#64748B",
    "row_hover": "#F1F5F9",
    "row_selected": "#E8F1F8",
    "row_selected_text": "#0F172A",
    "button_bg": "#FFFFFF",
    "button_hover": "#F8FAFC",
    "button_pressed": "#F1F5F9",
    "button_text": "#334155",
    "ghost_hover": "#F1F5F9",
    "danger": "#B91C1C",
    "danger_hover_bg": "#FEF2F2",
    "danger_hover_border": "#FECACA",
    "danger_solid": "#DC2626",
    "danger_solid_hover": "#B91C1C",
    "danger_solid_pressed": "#991B1B",
    "button_disabled_bg": "#F8FAFC",
    "button_disabled_text": "#94A3B8",
    "disabled_primary_bg": "#CBD5E1",
    "disabled_primary_text": "#F8FAFC",
    "status_active_bg": "#ECFDF5",
    "status_active_text": "#047857",
    "status_sold_bg": "#FFF7ED",
    "status_sold_text": "#C2410C",
    "status_neutral_bg": "#F1F5F9",
    "status_neutral_text": "#475569",
    "group_title": "#334155",
    "priority_high_bg": "#FEE2E2",
    "priority_high_text": "#B91C1C",
    "priority_normal_bg": "#DBEAFE",
    "priority_normal_text": "#1D4ED8",
    "priority_low_bg": "#E2E8F0",
    "priority_low_text": "#475569",
    "priority_none_bg": "#F1F5F9",
    "priority_none_text": "#64748B",
    "scrollbar": "#CBD5E1",
    "scrollbar_hover": "#94A3B8",
    "tooltip_bg": "#0F172A",
    "tooltip_text": "#F8FAFC",
}

DARK = {
    "bg": "#0F172A",
    "surface": "#111827",
    "surface_alt": "#0F172A",
    "sidebar": "#0B1220",
    "sidebar_border": "#1E293B",
    "primary": "#2563EB",
    "primary_hover": "#1D4ED8",
    "primary_pressed": "#1E40AF",
    "primary_text": "#FFFFFF",
    "text": "#E2E8F0",
    "text_secondary": "#94A3B8",
    "border": "#1E293B",
    "border_strong": "#334155",
    "accent": "#60A5FA",
    "tab_active": "#60A5FA",
    "input_bg": "#0F172A",
    "input_border": "#334155",
    "focus": "#60A5FA",
    "input_disabled_bg": "#0B1220",
    "input_disabled_text": "#64748B",
    "selection_bg": "#1E3A8A",
    "selection_text": "#E2E8F0",
    "combo_selection_bg": "#1E3A5F",
    "combo_selection_text": "#F8FAFC",
    "table_text": "#CBD5E1",
    "table_header": "#0F172A",
    "table_header_text": "#94A3B8",
    "row_hover": "#1E293B",
    "row_selected": "#1E3A5F",
    "row_selected_text": "#F8FAFC",
    "button_bg": "#111827",
    "button_hover": "#1E293B",
    "button_pressed": "#0F172A",
    "button_text": "#E2E8F0",
    "ghost_hover": "#1E293B",
    "danger": "#F87171",
    "danger_hover_bg": "#3F1D24",
    "danger_hover_border": "#7F1D1D",
    "danger_solid": "#DC2626",
    "danger_solid_hover": "#B91C1C",
    "danger_solid_pressed": "#991B1B",
    "button_disabled_bg": "#0B1220",
    "button_disabled_text": "#64748B",
    "disabled_primary_bg": "#334155",
    "disabled_primary_text": "#94A3B8",
    "status_active_bg": "#064E3B",
    "status_active_text": "#6EE7B7",
    "status_sold_bg": "#7C2D12",
    "status_sold_text": "#FDBA74",
    "status_neutral_bg": "#1E293B",
    "status_neutral_text": "#CBD5E1",
    "group_title": "#CBD5E1",
    "priority_high_bg": "#7F1D1D",
    "priority_high_text": "#FCA5A5",
    "priority_normal_bg": "#1E3A8A",
    "priority_normal_text": "#BFDBFE",
    "priority_low_bg": "#1E293B",
    "priority_low_text": "#CBD5E1",
    "priority_none_bg": "#1E293B",
    "priority_none_text": "#94A3B8",
    "scrollbar": "#334155",
    "scrollbar_hover": "#475569",
    "tooltip_bg": "#1E293B",
    "tooltip_text": "#F8FAFC",
}

PALETTES = {"light": LIGHT, "dark": DARK}

STYLESHEET_TEMPLATE = Template(
    """
QWidget {
    font-family: "Inter", "Segoe UI", "SF Pro Text", "Helvetica Neue", "Noto Sans", "DejaVu Sans", "Arial";
    font-size: 13px;
}

QMainWindow, QDialog {
    background: $bg;
}

#appRoot, #appBody, #workspace {
    background: $bg;
}

/* ------------------------------------------------------------- App shell */

#appHeader, #appFooter, #sidebar {
    background: $sidebar;
}

#appHeader {
    border-bottom: 1px solid $sidebar_border;
}

#appFooter {
    border-top: 1px solid $sidebar_border;
}

#appTitle {
    color: #F8FAFC;
    font-size: 15px;
    font-weight: 700;
}

#appSubtitle {
    color: #94A3B8;
    font-size: 11px;
}

#versionPill {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 10px;
    color: #CBD5E1;
    font-size: 11px;
    font-weight: 600;
    padding: 2px 8px;
}

#themeToggleHeader {
    background: transparent;
    border: 1px solid #334155;
    border-radius: 8px;
    color: #E2E8F0;
    padding: 0 12px;
    font-weight: 600;
}

#themeToggleHeader:hover {
    background: #1E293B;
    border-color: #475569;
}

#themeToggleHeader:pressed {
    background: #0F172A;
}

#themeToggleFooter {
    background: transparent;
    border: 1px solid #334155;
    border-radius: 8px;
    color: #CBD5E1;
    padding: 0 10px;
    font-size: 11px;
    font-weight: 600;
}

#themeToggleFooter:hover {
    background: #1E293B;
    border-color: #475569;
}

#themeToggleFooter:pressed {
    background: #0F172A;
}

#footerText {
    color: #94A3B8;
    font-size: 11px;
}

#footerSeparator {
    color: #475569;
    font-size: 11px;
}

#statusDot {
    color: #34D399;
    font-size: 10px;
}

/* ---------------------------------------------------------------- Sidebar */

#sidebar {
    border-right: 1px solid $sidebar_border;
}

#sidebarTitle {
    color: #F8FAFC;
    font-size: 19px;
    font-weight: 700;
}

#sidebarSubtitle, #sidebarHint {
    color: #94A3B8;
    font-size: 12px;
}

#sidebarHint {
    padding: 6px 2px;
}

#sidebar QPushButton {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 8px;
    color: #E2E8F0;
    font-weight: 600;
    padding: 0 14px;
}

#sidebar QPushButton:hover {
    background: #334155;
    border-color: #475569;
}

#sidebar QPushButton:pressed {
    background: $sidebar;
}

#sidebar QPushButton[role="primary"] {
    background: $primary;
    border-color: $primary;
    color: $primary_text;
}

#sidebar QPushButton[role="primary"]:hover {
    background: $primary_hover;
    border-color: $primary_hover;
}

#sidebar QPushButton[role="ghost"],
#sidebar QPushButton[role="danger"] {
    background: transparent;
    border-color: transparent;
}

#sidebar QPushButton[role="ghost"]:hover {
    background: #1E293B;
}

#sidebar QPushButton[role="danger"]:hover {
    background: #3F1D24;
}

#sidebar QPushButton:disabled {
    background: transparent;
    border-color: transparent;
}

#domainList {
    background: transparent;
    border: none;
    outline: 0;
    padding: 2px;
}

#domainList::item {
    color: #CBD5E1;
    padding: 10px 12px;
    margin: 2px 0;
    border-radius: 8px;
}

#domainList::item:hover {
    background: #1E293B;
    color: #F8FAFC;
}

#domainList::item:selected {
    background: #1E3A5F;
    color: #FFFFFF;
    border-left: 3px solid #60A5FA;
    padding-left: 9px;
    font-weight: 600;
}

/* -------------------------------------------------------------- Workspace */

#workspaceTitle {
    color: $text;
    font-size: 26px;
    font-weight: 700;
}

#workspaceSubtitle {
    color: $text_secondary;
    font-size: 13px;
}

#statusBadge {
    border-radius: 10px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 600;
}

#statusBadge[tone="active"] {
    background: $status_active_bg;
    color: $status_active_text;
}

#statusBadge[tone="sold"] {
    background: $status_sold_bg;
    color: $status_sold_text;
}

#statusBadge[tone="archived"] {
    background: $status_neutral_bg;
    color: $status_neutral_text;
}

#statusBadge[tone="none"] {
    background: $status_neutral_bg;
    color: $status_neutral_text;
}

/* ---------------------------------------------------------------- Buttons */

QPushButton {
    background: $button_bg;
    border: 1px solid $border;
    border-radius: 8px;
    color: $button_text;
    font-weight: 600;
    padding: 7px 14px;
}

QPushButton:hover {
    background: $button_hover;
    border-color: $border_strong;
}

QPushButton:pressed {
    background: $button_pressed;
}

QPushButton[role="primary"] {
    background: $primary;
    border-color: $primary;
    color: $primary_text;
}

QPushButton[role="primary"]:hover {
    background: $primary_hover;
    border-color: $primary_hover;
}

QPushButton[role="primary"]:pressed {
    background: $primary_pressed;
}

QPushButton[role="primary"]:disabled {
    background: $disabled_primary_bg;
    border-color: $disabled_primary_bg;
    color: $disabled_primary_text;
}

QPushButton[role="dangerSolid"] {
    background: $danger_solid;
    border-color: $danger_solid;
    color: #FFFFFF;
}

QPushButton[role="dangerSolid"]:hover {
    background: $danger_solid_hover;
    border-color: $danger_solid_hover;
}

QPushButton[role="dangerSolid"]:pressed {
    background: $danger_solid_pressed;
    border-color: $danger_solid_pressed;
}

QPushButton[role="secondary"] {
    background: $button_bg;
    border-color: $border;
    color: $button_text;
}

QPushButton[role="ghost"],
QPushButton[role="danger"] {
    background: transparent;
    border-color: transparent;
    padding: 0;
}

QPushButton[role="ghost"]:hover {
    background: $ghost_hover;
}

QPushButton[role="danger"] {
    color: $danger;
}

QPushButton[role="danger"]:hover {
    background: $danger_hover_bg;
    border-color: $danger_hover_border;
}

QPushButton:disabled {
    color: $button_disabled_text;
    border-color: $border;
    background: $button_disabled_bg;
}

/* ------------------------------------------------------------------- Tabs */

QTabWidget::pane {
    border: none;
    background: transparent;
}

QTabBar::tab {
    background: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    color: $text_secondary;
    font-weight: 600;
    padding: 9px 16px;
    margin-right: 6px;
}

QTabBar::tab:hover {
    color: $text;
}

QTabBar::tab:selected {
    color: $text;
    border-bottom: 2px solid $tab_active;
}

/* ----------------------------------------------------------------- Inputs */

QLineEdit, QTextEdit, QComboBox {
    background: $input_bg;
    border: 1px solid $input_border;
    border-radius: 8px;
    color: $text;
    padding: 7px 10px;
    selection-background-color: $selection_bg;
    selection-color: $selection_text;
}

QLineEdit:hover, QTextEdit:hover, QComboBox:hover {
    border-color: $border_strong;
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border-color: $focus;
}

QLineEdit:disabled, QTextEdit:disabled, QComboBox:disabled {
    background: $input_disabled_bg;
    color: $input_disabled_text;
}

QComboBox::drop-down {
    border: none;
    width: 26px;
}

QComboBox QAbstractItemView {
    background: $surface;
    border: 1px solid $border;
    border-radius: 8px;
    padding: 4px;
    selection-background-color: $combo_selection_bg;
    selection-color: $combo_selection_text;
}

#searchInput {
    padding-left: 10px;
    min-height: 22px;
}

#hint {
    color: $text_secondary;
    font-size: 12px;
}

/* ----------------------------------------------------------------- Tables */

#tableCard {
    background: $surface;
    border: 1px solid $border;
    border-radius: 12px;
}

QTableWidget {
    background: $surface;
    alternate-background-color: $surface_alt;
    border: none;
    border-radius: 12px;
    color: $table_text;
    gridline-color: transparent;
    outline: 0;
    selection-background-color: $row_selected;
    selection-color: $row_selected_text;
}

QTableWidget::item {
    border: none;
    padding: 0 12px;
}

QTableWidget::item:hover {
    background: $row_hover;
}

QTableWidget::item:selected {
    background: $row_selected;
    color: $row_selected_text;
}

QHeaderView::section {
    background: $table_header;
    border: none;
    border-bottom: 1px solid $border;
    color: $table_header_text;
    font-size: 11px;
    font-weight: 700;
    padding: 0 12px;
}

QHeaderView::section:first {
    border-top-left-radius: 12px;
}

QHeaderView::section:last {
    border-top-right-radius: 12px;
}

QTableCornerButton::section {
    background: $table_header;
    border: none;
}

/* ------------------------------------------------------------- Empty state */

#emptyTitle {
    color: $text;
    font-size: 17px;
    font-weight: 700;
}

#emptySubtitle {
    color: $text_secondary;
    font-size: 13px;
}

/* ----------------------------------------------------------- Priority pill */

#priorityBadge {
    border-radius: 11px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 600;
}

#priorityBadge[tone="high"] {
    background: $priority_high_bg;
    color: $priority_high_text;
}

#priorityBadge[tone="normal"] {
    background: $priority_normal_bg;
    color: $priority_normal_text;
}

#priorityBadge[tone="low"] {
    background: $priority_low_bg;
    color: $priority_low_text;
}

#priorityBadge[tone="none"] {
    background: $priority_none_bg;
    color: $priority_none_text;
}

/* ----------------------------------------------------------------- Groups */

QGroupBox {
    background: $surface;
    border: 1px solid $border;
    border-radius: 10px;
    margin-top: 18px;
    padding: 16px 12px 12px 12px;
    font-weight: 600;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: $group_title;
}

QScrollArea {
    border: none;
    background: transparent;
}

QScrollArea > QWidget > QWidget {
    background: transparent;
}

QDialog QLabel {
    color: $button_text;
}

QLabel#hint {
    color: $text_secondary;
    font-size: 12px;
}

/* -------------------------------------------------------------- Scrollbars */

QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 4px 2px;
}

QScrollBar::handle:vertical {
    background: $scrollbar;
    border-radius: 5px;
    min-height: 32px;
}

QScrollBar::handle:vertical:hover {
    background: $scrollbar_hover;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: transparent;
    height: 0;
}

QScrollBar:horizontal {
    background: transparent;
    height: 10px;
    margin: 2px 4px;
}

QScrollBar::handle:horizontal {
    background: $scrollbar;
    border-radius: 5px;
    min-width: 32px;
}

QScrollBar::handle:horizontal:hover {
    background: $scrollbar_hover;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: transparent;
    width: 0;
}

/* ----------------------------------------------------------------- Tooltip */

QToolTip {
    background: $tooltip_bg;
    border: 1px solid $border;
    border-radius: 6px;
    color: $tooltip_text;
    padding: 6px 8px;
}
"""
)


def build_stylesheet(mode: str = "light") -> str:
    """Return the stylesheet for the requested mode."""
    palette = PALETTES.get(mode, LIGHT)
    return STYLESHEET_TEMPLATE.substitute(palette)


def _build_palette(mode: str) -> QPalette:
    """Build a native palette so popups, placeholders and dialogs match the theme."""
    palette = QPalette()
    if mode == "dark":
        colors = {
            QPalette.ColorRole.Window: "#0F172A",
            QPalette.ColorRole.WindowText: "#E2E8F0",
            QPalette.ColorRole.Base: "#111827",
            QPalette.ColorRole.AlternateBase: "#0F172A",
            QPalette.ColorRole.Text: "#E2E8F0",
            QPalette.ColorRole.Button: "#111827",
            QPalette.ColorRole.ButtonText: "#E2E8F0",
            QPalette.ColorRole.Highlight: "#2563EB",
            QPalette.ColorRole.HighlightedText: "#FFFFFF",
            QPalette.ColorRole.PlaceholderText: "#64748B",
            QPalette.ColorRole.ToolTipBase: "#1E293B",
            QPalette.ColorRole.ToolTipText: "#F8FAFC",
            QPalette.ColorRole.Link: "#60A5FA",
            QPalette.ColorRole.Mid: "#1E293B",
            QPalette.ColorRole.Dark: "#0B1220",
            QPalette.ColorRole.Light: "#334155",
        }
    else:
        colors = {
            QPalette.ColorRole.Window: "#F5F7FA",
            QPalette.ColorRole.WindowText: "#0F172A",
            QPalette.ColorRole.Base: "#FFFFFF",
            QPalette.ColorRole.AlternateBase: "#FAFBFD",
            QPalette.ColorRole.Text: "#0F172A",
            QPalette.ColorRole.Button: "#FFFFFF",
            QPalette.ColorRole.ButtonText: "#334155",
            QPalette.ColorRole.Highlight: "#315F85",
            QPalette.ColorRole.HighlightedText: "#FFFFFF",
            QPalette.ColorRole.PlaceholderText: "#94A3B8",
            QPalette.ColorRole.ToolTipBase: "#0F172A",
            QPalette.ColorRole.ToolTipText: "#F8FAFC",
            QPalette.ColorRole.Link: "#315F85",
            QPalette.ColorRole.Mid: "#E2E8F0",
            QPalette.ColorRole.Dark: "#CBD5E1",
            QPalette.ColorRole.Light: "#FFFFFF",
        }
    for role, color in colors.items():
        palette.setColor(role, QColor(color))
    return palette


def apply_theme(application: QApplication | None = None, mode: str = "light") -> None:
    """Apply the shared font, palette and stylesheet to the whole application."""
    app = application or QApplication.instance()
    if app is None:
        return
    mode = mode if mode in PALETTES else "light"
    font = QFont()
    font.setPointSize(10)
    app.setFont(font)
    app.setStyle("Fusion")
    app.setPalette(_build_palette(mode))
    app.setStyleSheet(build_stylesheet(mode))


def load_theme_mode() -> str:
    """Read the saved theme mode, defaulting to light."""
    settings = QSettings(SETTINGS_ORG, SETTINGS_APP)
    value = str(settings.value(THEME_SETTING, "light"))
    return value if value in PALETTES else "light"


def save_theme_mode(mode: str) -> None:
    """Persist the selected theme mode."""
    if mode not in PALETTES:
        return
    settings = QSettings(SETTINGS_ORG, SETTINGS_APP)
    settings.setValue(THEME_SETTING, mode)
    settings.sync()
