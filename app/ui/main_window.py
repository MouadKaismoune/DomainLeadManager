"""Domain-scoped PySide6 workspace with a modern, themeable interface."""

from pathlib import Path

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QFont, QIcon, QPainter, QPalette, QPen
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.config.settings import APP_TITLE, APP_VERSION
from app.core.exceptions import DuplicateRecordError, ValidationError
from app.services.domain_service import DomainService
from app.services.workspace_service import WorkspaceService
from app.ui.icons import centered_table_button, icon_button, line_icon
from app.ui.table_data import (
    aggregate_contact_rows,
    aggregate_overview_rows,
    display_value,
)
from app.ui.theme import apply_theme, load_theme_mode, save_theme_mode


def repolish(widget: QWidget) -> None:
    """Re-apply stylesheet rules after changing a dynamic property."""
    widget.style().unpolish(widget)
    widget.style().polish(widget)


class ThemedComboBox(QComboBox):
    """Combo box with a theme-aware chevron drawn over the native control."""

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = self.palette().color(QPalette.ColorRole.Window).lightness() < 128
        color = QColor("#94A3B8" if dark else "#64748B")
        painter.setPen(
            QPen(
                color,
                1.6,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
                Qt.PenJoinStyle.RoundJoin,
            )
        )
        x = self.width() - 15
        y = int(self.height() / 2) - 1
        painter.drawLine(x - 4, y - 1, x, y + 3)
        painter.drawLine(x, y + 3, x + 4, y - 1)
        painter.end()


class ResponsiveTable(QTableWidget):
    """A table that keeps proportional column widths while the window resizes."""

    def __init__(
        self,
        rows: int,
        columns: int,
        ratios: dict[int, float],
        fixed_columns: dict[int, int] | None = None,
    ) -> None:
        super().__init__(rows, columns)
        self.ratios = ratios
        self.fixed_columns = fixed_columns or {}
        self._adjusting = False

    def apply_column_widths(self) -> None:
        if self._adjusting:
            return
        width = self.viewport().width()
        if width <= 0 or not self.ratios:
            return
        self._adjusting = True
        try:
            available = max(0, width - sum(self.fixed_columns.values()))
            for column, ratio in self.ratios.items():
                self.setColumnWidth(column, max(80, int(available * ratio)))
            for column, column_width in self.fixed_columns.items():
                self.setColumnWidth(column, column_width)
        finally:
            self._adjusting = False

    def resizeEvent(self, event) -> None:  # noqa: N802 - Qt API name
        super().resizeEvent(event)
        self.apply_column_widths()


def configure_table(table: QTableWidget) -> None:
    """Apply the shared modern table configuration."""
    table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    table.setShowGrid(False)
    table.setAlternatingRowColors(True)
    table.setWordWrap(False)
    table.setMouseTracking(True)
    table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
    table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
    table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
    table.setCornerButtonEnabled(False)

    vertical = table.verticalHeader()
    vertical.setVisible(False)
    vertical.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
    vertical.setDefaultSectionSize(44)

    header = table.horizontalHeader()
    header.setFixedHeight(42)
    header.setHighlightSections(False)
    header.setStretchLastSection(False)
    header.setMinimumSectionSize(44)
    header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

    for column in getattr(table, "fixed_columns", {}):
        header.setSectionResizeMode(column, QHeaderView.ResizeMode.Fixed)

    if isinstance(table, ResponsiveTable):
        table.apply_column_widths()


def configure_dialog_buttons(buttons: QDialogButtonBox, save_tooltip: str = "Save") -> None:
    """Use clear text buttons with icons instead of ambiguous icon-only actions."""
    save = buttons.button(QDialogButtonBox.StandardButton.Save)
    cancel = buttons.button(QDialogButtonBox.StandardButton.Cancel)

    save.setText("Save")
    save.setIcon(line_icon("check", "#FFFFFF", 18))
    save.setIconSize(QSize(16, 16))
    save.setProperty("role", "primary")
    save.setToolTip(save_tooltip)
    save.setAccessibleName(save_tooltip)
    save.setMinimumHeight(36)
    save.setDefault(True)
    save.setAutoDefault(True)
    save.setCursor(Qt.CursorShape.PointingHandCursor)

    cancel.setText("Cancel")
    cancel.setIcon(line_icon("close", "#64748B", 18))
    cancel.setIconSize(QSize(16, 16))
    cancel.setProperty("role", "secondary")
    cancel.setToolTip("Cancel")
    cancel.setAccessibleName("Cancel")
    cancel.setMinimumHeight(36)
    cancel.setCursor(Qt.CursorShape.PointingHandCursor)

    # QDialogButtonBox creates its buttons before the role property is set,
    # so force the stylesheet to re-evaluate the selectors.
    repolish(save)
    repolish(cancel)


def priority_cell(value: object) -> QWidget:
    """Return a centered colored pill for a lead priority."""
    priority = str(value).strip().lower() if value is not None else ""
    text = priority.capitalize() if priority else "—"
    tone = priority if priority in ("low", "normal", "high") else "none"

    label = QLabel(text)
    label.setObjectName("priorityBadge")
    label.setProperty("tone", tone)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setFixedHeight(24)
    label.setMinimumWidth(74)

    container = QWidget()
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(label)
    container.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
    return container


class EmptyState(QWidget):
    """Centered empty state with an optional primary action."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._callback = None

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.addStretch(1)

        content = QWidget(self)
        content.setMaximumWidth(440)
        box = QVBoxLayout(content)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(10)
        box.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.icon = QLabel()
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title = QLabel()
        self.title.setObjectName("emptyTitle")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle = QLabel()
        self.subtitle.setObjectName("emptySubtitle")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setWordWrap(True)
        self.action = QPushButton()
        self.action.setProperty("role", "primary")
        self.action.setCursor(Qt.CursorShape.PointingHandCursor)
        self.action.setMinimumHeight(36)
        self.action.hide()
        self.action.clicked.connect(self._run)

        box.addWidget(self.icon, 0, Qt.AlignmentFlag.AlignHCenter)
        box.addWidget(self.title)
        box.addWidget(self.subtitle)
        box.addSpacing(4)
        box.addWidget(self.action, 0, Qt.AlignmentFlag.AlignHCenter)

        root.addWidget(content, 0, Qt.AlignmentFlag.AlignHCenter)
        root.addStretch(1)

    def set_content(
        self,
        icon: str,
        title: str,
        subtitle: str,
        action_text: str | None = None,
        callback=None,
        tone: str = "#94A3B8",
    ) -> None:
        self.icon.setPixmap(line_icon(icon, tone, 44).pixmap(44, 44))
        self.title.setText(title)
        self.subtitle.setText(subtitle)
        self._callback = callback
        if action_text:
            self.action.setText(action_text)
            self.action.show()
        else:
            self.action.hide()

    def _run(self) -> None:
        if self._callback:
            self._callback()


class DynamicValueRows(QWidget):
    """One or more text fields with an add button beside every field."""

    def __init__(self, placeholder: str) -> None:
        super().__init__()
        self.placeholder = placeholder
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(6)
        self.fields: list[QLineEdit] = []
        self.add_row()

    def add_row(self, value: str = "") -> None:
        row = QHBoxLayout()
        row.setSpacing(6)
        field = QLineEdit(value)
        field.setPlaceholderText(self.placeholder)
        field.setCursorPosition(0)
        add_button = icon_button(self, "plus", "Add another field", size=30)
        add_button.clicked.connect(lambda _checked=False: self.add_row())
        remove_button = icon_button(self, "close", "Remove field", "danger", size=30)
        remove_button.clicked.connect(lambda _checked=False: self.remove_row(field, row))
        row.addWidget(field, 1)
        row.addWidget(add_button)
        row.addWidget(remove_button)
        self.layout.addLayout(row)
        self.fields.append(field)

    def remove_row(self, field: QLineEdit, row: QHBoxLayout) -> None:
        if len(self.fields) == 1:
            field.clear()
            return
        self.fields.remove(field)
        while row.count():
            item = row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.layout.removeItem(row)

    def values(self) -> list[str]:
        return [field.text() for field in self.fields]

    def set_values(self, values: list[str]) -> None:
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.layout():
                while item.layout().count():
                    child = item.layout().takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
            elif item.widget():
                item.widget().deleteLater()
        self.fields = []
        for value in values or [""]:
            self.add_row(value)


class DynamicSocialRows(QWidget):
    """Platform and URL fields with add/remove controls."""

    def __init__(self) -> None:
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(6)
        self.rows: list[tuple[QLineEdit, QLineEdit, QHBoxLayout]] = []
        self.add_row()

    def add_row(self) -> None:
        row = QHBoxLayout()
        row.setSpacing(6)
        platform = QLineEdit()
        platform.setPlaceholderText("Facebook / LinkedIn")
        url = QLineEdit()
        url.setPlaceholderText("Profile URL")
        add_button = icon_button(self, "plus", "Add another account", size=30)
        add_button.clicked.connect(lambda _checked=False: self.add_row())
        remove_button = icon_button(self, "close", "Remove account", "danger", size=30)
        remove_button.clicked.connect(
            lambda _checked=False: self.remove_row(platform, url, row)
        )
        row.addWidget(platform, 2)
        row.addWidget(url, 3)
        row.addWidget(add_button)
        row.addWidget(remove_button)
        self.layout.addLayout(row)
        self.rows.append((platform, url, row))

    def remove_row(self, platform: QLineEdit, url: QLineEdit, row: QHBoxLayout) -> None:
        if len(self.rows) == 1:
            platform.clear()
            url.clear()
            return
        self.rows = [item for item in self.rows if item[0] is not platform]
        while row.count():
            item = row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.layout.removeItem(row)

    def values(self) -> list[dict[str, str]]:
        return [
            {"platform": platform.text(), "url": url.text()}
            for platform, url, _ in self.rows
        ]

    def set_values(self, values: list[dict[str, str]]) -> None:
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.layout():
                while item.layout().count():
                    child = item.layout().takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
            elif item.widget():
                item.widget().deleteLater()
        self.rows = []
        for value in values or [{"platform": "", "url": ""}]:
            self.add_row()
            platform, url, _ = self.rows[-1]
            platform.setText(value.get("platform", ""))
            platform.setCursorPosition(0)
            url.setText(value.get("url", ""))
            url.setCursorPosition(0)


class ContactEditor(QGroupBox):
    def __init__(self, number: int) -> None:
        super().__init__(f"Contact {number}")
        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText("Full name")
        self.title_entry = QLineEdit()
        self.title_entry.setPlaceholderText("Job title")
        self.department_entry = QLineEdit()
        self.department_entry.setPlaceholderText("Department")
        self.email_rows = DynamicValueRows("Email address")
        self.phone_rows = DynamicValueRows("Phone number")
        self.social_rows = DynamicSocialRows()

        form = QFormLayout(self)
        form.setContentsMargins(14, 18, 14, 14)
        form.setHorizontalSpacing(14)
        form.setVerticalSpacing(8)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        form.addRow("Name", self.name_entry)
        form.addRow("Job title", self.title_entry)
        form.addRow("Department", self.department_entry)
        form.addRow("Emails", self.email_rows)
        form.addRow("Phones", self.phone_rows)
        form.addRow("Socials", self.social_rows)

    def values(self) -> dict:
        return {
            "name": self.name_entry.text(),
            "job_title": self.title_entry.text(),
            "department": self.department_entry.text(),
            "emails": self.email_rows.values(),
            "phones": self.phone_rows.values(),
            "socials": self.social_rows.values(),
        }

    def populate(self, contact: dict) -> None:
        self.name_entry.setText(str(contact.get("full_name") or contact.get("name") or ""))
        self.name_entry.setCursorPosition(0)
        self.title_entry.setText(str(contact.get("job_title") or ""))
        self.title_entry.setCursorPosition(0)
        self.department_entry.setText(str(contact.get("department") or ""))
        self.department_entry.setCursorPosition(0)
        self.email_rows.set_values(contact.get("emails", []))
        self.phone_rows.set_values(contact.get("phones", []))
        self.social_rows.set_values(contact.get("socials", []))


class DomainDialog(QDialog):
    def __init__(self, parent: QWidget, value: str = "") -> None:
        super().__init__(parent)
        self.setWindowTitle("Edit domain" if value else "Add domain")
        self.setMinimumWidth(460)
        self.domain_entry = QLineEdit(value)
        self.domain_entry.setPlaceholderText("example.com")

        form = QFormLayout()
        form.setContentsMargins(0, 0, 0, 0)
        form.setSpacing(12)
        form.addRow("Domain", self.domain_entry)
        hint = QLabel("Use the domain name, for example example.com.")
        hint.setObjectName("hint")
        hint.setWordWrap(True)
        form.addRow(hint)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        configure_dialog_buttons(buttons)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 18)
        layout.setSpacing(18)
        layout.addLayout(form)
        layout.addWidget(buttons)
        self.domain_entry.setFocus()

    def value(self) -> str:
        return self.domain_entry.text()


class ProspectDialog(QDialog):
    def __init__(self, parent: QWidget, record: dict | None = None) -> None:
        super().__init__(parent)
        self.record = record
        self.setWindowTitle("Edit contact" if record else "Add contact")
        self.setMinimumSize(740, 620)
        self.resize(860, 740)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.addTab(self._company_tab(), "Company")
        self.tabs.addTab(self._contacts_tab(), "Contacts")
        self.tabs.addTab(self._lead_tab(), "Lead")

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        configure_dialog_buttons(buttons, "Save changes" if record else "Save")
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 18)
        layout.setSpacing(14)
        layout.addWidget(self.tabs, 1)
        layout.addWidget(buttons)

        if record:
            self._populate(record)

    def _populate(self, record: dict) -> None:
        self.company_name_entry.setText(str(record.get("company_name") or ""))
        self.website_entry.setText(str(record.get("website") or ""))
        self.description_entry.setText(str(record.get("description") or ""))
        self.address_entry.setText(str(record.get("address") or ""))
        self.city_entry.setText(str(record.get("city") or ""))
        self.state_entry.setText(str(record.get("state") or ""))
        self.country_entry.setText(str(record.get("country") or ""))
        for entry in (
            self.company_name_entry,
            self.website_entry,
            self.address_entry,
            self.city_entry,
            self.state_entry,
            self.country_entry,
        ):
            entry.setCursorPosition(0)
        self.company_email_rows.set_values(record.get("company_emails", []))
        self.company_phone_rows.set_values(record.get("company_phones", []))
        self.company_social_rows.set_values(record.get("company_socials", []))
        contacts = record.get("contacts", [])
        for index, contact in enumerate(contacts):
            if index >= len(self.contact_editors):
                self._add_contact_editor()
            self.contact_editors[index].populate(contact)
        priority = str(record.get("priority") or "normal").lower()
        priority_index = self.priority_choice.findData(priority)
        if priority_index >= 0:
            self.priority_choice.setCurrentIndex(priority_index)
        self.notes_entry.setText(str(record.get("notes") or ""))

    def _company_tab(self) -> QWidget:
        tab = QWidget()
        outer = QVBoxLayout(tab)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        content = QWidget()
        form = QFormLayout(content)
        form.setContentsMargins(20, 18, 20, 18)
        form.setHorizontalSpacing(16)
        form.setVerticalSpacing(12)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        form.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow
        )

        self.company_name_entry = QLineEdit()
        self.company_name_entry.setPlaceholderText("Company or independent professional")
        self.website_entry = QLineEdit()
        self.website_entry.setPlaceholderText("https://example.com")
        self.description_entry = QTextEdit()
        self.description_entry.setPlaceholderText("Short company description")
        self.description_entry.setFixedHeight(90)
        self.address_entry = QLineEdit()
        self.city_entry = QLineEdit()
        self.state_entry = QLineEdit()
        self.country_entry = QLineEdit()
        self.company_email_rows = DynamicValueRows("General email")
        self.company_phone_rows = DynamicValueRows("Company phone")
        self.company_social_rows = DynamicSocialRows()

        form.addRow("Name *", self.company_name_entry)
        form.addRow("Website", self.website_entry)
        form.addRow("Description", self.description_entry)
        form.addRow("Address", self.address_entry)
        form.addRow("City", self.city_entry)
        form.addRow("State", self.state_entry)
        form.addRow("Country", self.country_entry)
        form.addRow("General emails", self.company_email_rows)
        form.addRow("Company phones", self.company_phone_rows)
        form.addRow("Social accounts", self.company_social_rows)

        scroll.setWidget(content)
        outer.addWidget(scroll)
        return tab

    def _contacts_tab(self) -> QWidget:
        tab = QWidget()
        outer = QVBoxLayout(tab)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(10)

        header = QHBoxLayout()
        hint = QLabel("People you want to reach at this company.")
        hint.setObjectName("hint")
        add_button = QPushButton("Add person")
        add_button.setIcon(line_icon("plus", "#64748B", 18))
        add_button.setIconSize(QSize(16, 16))
        add_button.setProperty("role", "secondary")
        add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        add_button.setMinimumHeight(34)
        add_button.clicked.connect(lambda _checked=False: self._add_contact_editor())
        header.addWidget(hint)
        header.addStretch(1)
        header.addWidget(add_button)
        outer.addLayout(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        content = QWidget()
        self.contacts_layout = QVBoxLayout(content)
        self.contacts_layout.setContentsMargins(0, 0, 0, 0)
        self.contacts_layout.setSpacing(10)
        self.contact_editors: list[ContactEditor] = []
        self._add_contact_editor()
        self.contacts_layout.addStretch(1)
        scroll.setWidget(content)
        outer.addWidget(scroll, 1)
        return tab

    def _add_contact_editor(self) -> None:
        editor = ContactEditor(len(getattr(self, "contact_editors", [])) + 1)
        self.contact_editors.append(editor)
        self.contacts_layout.insertWidget(self.contacts_layout.count() - 1, editor)

    def _lead_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(14)

        hint = QLabel("Priority and notes are specific to this domain opportunity.")
        hint.setObjectName("hint")
        hint.setWordWrap(True)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        form.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow
        )
        self.priority_choice = ThemedComboBox()
        for value in ("low", "normal", "high"):
            self.priority_choice.addItem(value.capitalize(), value)
        self.priority_choice.setCurrentIndex(1)
        self.notes_entry = QTextEdit()
        self.notes_entry.setPlaceholderText("Notes for this domain opportunity")
        self.notes_entry.setFixedHeight(140)
        form.addRow("Priority", self.priority_choice)
        form.addRow("Notes", self.notes_entry)

        layout.addWidget(hint)
        layout.addLayout(form)
        layout.addStretch(1)
        return tab

    def values(self) -> dict:
        values = {
            "company": {
                "name": self.company_name_entry.text(),
                "website": self.website_entry.text(),
                "description": self.description_entry.toPlainText(),
                "address": self.address_entry.text(),
                "city": self.city_entry.text(),
                "state": self.state_entry.text(),
                "country": self.country_entry.text(),
            },
            "company_emails": self.company_email_rows.values(),
            "company_phones": self.company_phone_rows.values(),
            "company_socials": self.company_social_rows.values(),
            "contacts": [editor.values() for editor in self.contact_editors],
            "priority": self.priority_choice.currentData() or "normal",
            "notes": self.notes_entry.toPlainText(),
        }
        if self.record:
            values["lead_id"] = self.record["lead_id"]
        return values


class MainWindow(QMainWindow):
    def __init__(self, title: str) -> None:
        super().__init__()
        self._theme_mode = load_theme_mode()
        apply_theme(QApplication.instance(), self._theme_mode)
        self.setObjectName("mainWindow")
        self.setWindowTitle(title)
        self._icon_path = (
            Path(__file__).resolve().parents[2] / "assets" / "domain-lead-manager.svg"
        )
        self.setWindowIcon(QIcon(str(self._icon_path)))
        self.setMinimumSize(980, 640)
        self.resize(1200, 780)

        self.domain_service = DomainService()
        self.workspace_service = WorkspaceService()
        self.domain_rows: list[dict] = []
        self.workspace_rows: list[dict] = []
        self.all_workspace_rows: list[dict] = []
        self.all_contact_rows: list[dict] = []

        self._build()
        self._sync_theme_controls()
        self.refresh_domains()

    # ---------------------------------------------------------------- layout

    def _build(self) -> None:
        central = QWidget()
        central.setObjectName("appRoot")
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._build_header())

        body = QWidget()
        body.setObjectName("appBody")
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)
        body_layout.addWidget(self._build_sidebar())
        body_layout.addWidget(self._build_workspace(), stretch=1)
        layout.addWidget(body, 1)

        layout.addWidget(self._build_footer())
        self.setCentralWidget(central)

    def _build_header(self) -> QWidget:
        header = QWidget()
        header.setObjectName("appHeader")
        header.setFixedHeight(58)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(18, 0, 18, 0)
        layout.setSpacing(12)

        logo = QLabel()
        logo.setPixmap(QIcon(str(self._icon_path)).pixmap(28, 28))
        logo.setFixedSize(28, 28)
        layout.addWidget(logo)

        titles = QVBoxLayout()
        titles.setSpacing(0)
        app_title = QLabel(APP_TITLE)
        app_title.setObjectName("appTitle")
        app_subtitle = QLabel("Lead workspace")
        app_subtitle.setObjectName("appSubtitle")
        titles.addWidget(app_title)
        titles.addWidget(app_subtitle)
        layout.addLayout(titles)
        layout.addStretch(1)

        version = QLabel(f"v{APP_VERSION}")
        version.setObjectName("versionPill")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version.setFixedHeight(26)
        layout.addWidget(version)

        self.header_theme_button = QPushButton()
        self.header_theme_button.setObjectName("themeToggleHeader")
        self.header_theme_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.header_theme_button.setFixedHeight(34)
        self.header_theme_button.setIconSize(QSize(16, 16))
        self.header_theme_button.clicked.connect(self._toggle_theme)
        layout.addWidget(self.header_theme_button)
        return header

    def _build_footer(self) -> QWidget:
        footer = QWidget()
        footer.setObjectName("appFooter")
        footer.setFixedHeight(44)
        layout = QHBoxLayout(footer)
        layout.setContentsMargins(18, 0, 18, 0)
        layout.setSpacing(8)

        copyright_label = QLabel(f"© 2026 {APP_TITLE}")
        copyright_label.setObjectName("footerText")
        separator = QLabel("•")
        separator.setObjectName("footerSeparator")
        version = QLabel(f"Version {APP_VERSION}")
        version.setObjectName("footerText")
        layout.addWidget(copyright_label)
        layout.addWidget(separator)
        layout.addWidget(version)
        layout.addStretch(1)

        status_dot = QLabel("●")
        status_dot.setObjectName("statusDot")
        status_text = QLabel("Local database")
        status_text.setObjectName("footerText")
        layout.addWidget(status_dot)
        layout.addWidget(status_text)

        self.footer_theme_button = QPushButton()
        self.footer_theme_button.setObjectName("themeToggleFooter")
        self.footer_theme_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.footer_theme_button.setFixedHeight(28)
        self.footer_theme_button.setIconSize(QSize(14, 14))
        self.footer_theme_button.clicked.connect(self._toggle_theme)
        layout.addWidget(self.footer_theme_button)
        return footer

    # ---------------------------------------------------------------- theme

    def _sync_theme_controls(self) -> None:
        is_dark = self._theme_mode == "dark"
        action = "Light mode" if is_dark else "Dark mode"
        short = "Light" if is_dark else "Dark"
        icon = "sun" if is_dark else "moon"
        tooltip = "Switch to light mode" if is_dark else "Switch to dark mode"

        self.header_theme_button.setText(action)
        self.header_theme_button.setIcon(line_icon(icon, "#CBD5E1", 18))
        self.header_theme_button.setToolTip(tooltip)
        self.header_theme_button.setAccessibleName(tooltip)

        self.footer_theme_button.setText(short)
        self.footer_theme_button.setIcon(line_icon(icon, "#94A3B8", 16))
        self.footer_theme_button.setToolTip(tooltip)
        self.footer_theme_button.setAccessibleName(tooltip)

    def _toggle_theme(self) -> None:
        self._theme_mode = "dark" if self._theme_mode == "light" else "light"
        save_theme_mode(self._theme_mode)
        app = QApplication.instance()
        if app is not None:
            apply_theme(app, self._theme_mode)
        self._sync_theme_controls()
        self._refresh_badges()

    def _refresh_badges(self) -> None:
        if getattr(self, "status_badge", None) is not None:
            repolish(self.status_badge)
        table = getattr(self, "workspace_table", None)
        if table is None:
            return
        for row in range(table.rowCount()):
            cell = table.cellWidget(row, 5)
            if cell is None:
                continue
            for label in cell.findChildren(QLabel):
                if label.objectName() == "priorityBadge":
                    repolish(label)

    def _build_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(272)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(18, 22, 18, 18)
        layout.setSpacing(14)

        title_row = QHBoxLayout()
        title_row.setSpacing(9)
        title_icon = QLabel()
        title_icon.setPixmap(line_icon("globe", "#60A5FA", 20).pixmap(20, 20))
        title = QLabel("Domains")
        title.setObjectName("sidebarTitle")
        title_row.addWidget(title_icon)
        title_row.addWidget(title)
        title_row.addStretch(1)
        layout.addLayout(title_row)

        subtitle = QLabel("Manage your domain portfolio")
        subtitle.setObjectName("sidebarSubtitle")
        layout.addWidget(subtitle)

        actions = QHBoxLayout()
        actions.setSpacing(8)
        self.add_button = QPushButton("Add domain")
        self.add_button.setIcon(line_icon("plus", "#FFFFFF", 18))
        self.add_button.setIconSize(QSize(16, 16))
        self.add_button.setProperty("role", "primary")
        self.add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_button.setMinimumHeight(38)
        self.edit_button = icon_button(
            self, "edit", "Edit selected domain", color="#CBD5E1", size=38
        )
        self.delete_button = icon_button(
            self, "trash", "Delete selected domain", "danger", color="#F87171", size=38
        )
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.add_button.clicked.connect(self._add_domain)
        self.edit_button.clicked.connect(self._edit_domain)
        self.delete_button.clicked.connect(self._delete_domain)
        actions.addWidget(self.add_button, 1)
        actions.addWidget(self.edit_button)
        actions.addWidget(self.delete_button)
        layout.addLayout(actions)

        self.domain_list = QListWidget()
        self.domain_list.setObjectName("domainList")
        self.domain_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.domain_list.setTextElideMode(Qt.TextElideMode.ElideRight)
        self.domain_list.setUniformItemSizes(True)
        self.domain_list.setSpacing(0)
        self.domain_list.currentItemChanged.connect(self._domain_selected)
        layout.addWidget(self.domain_list, 1)

        self.domains_hint = QLabel("No domains yet. Add your first domain to get started.")
        self.domains_hint.setObjectName("sidebarHint")
        self.domains_hint.setWordWrap(True)
        self.domains_hint.hide()
        layout.addWidget(self.domains_hint)
        return sidebar

    def _build_workspace(self) -> QWidget:
        workspace = QWidget()
        workspace.setObjectName("workspace")
        layout = QVBoxLayout(workspace)
        layout.setContentsMargins(28, 24, 28, 22)
        layout.setSpacing(18)

        header = QHBoxLayout()
        header.setSpacing(16)
        titles = QVBoxLayout()
        titles.setSpacing(4)

        title_row = QHBoxLayout()
        title_row.setSpacing(10)
        self.workspace_title = QLabel("Select a domain")
        self.workspace_title.setObjectName("workspaceTitle")
        self.workspace_title.setSizePolicy(
            QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred
        )
        self.status_badge = QLabel("Active")
        self.status_badge.setObjectName("statusBadge")
        self.status_badge.hide()
        title_row.addWidget(self.workspace_title, 1)
        title_row.addWidget(self.status_badge, 0, Qt.AlignmentFlag.AlignVCenter)
        titles.addLayout(title_row)

        self.workspace_status = QLabel(
            "Choose a domain from the sidebar to open its workspace."
        )
        self.workspace_status.setObjectName("workspaceSubtitle")
        titles.addWidget(self.workspace_status)
        header.addLayout(titles, 1)

        self.add_contact_button = QPushButton("Add contact")
        self.add_contact_button.setIcon(line_icon("plus", "#FFFFFF", 18))
        self.add_contact_button.setIconSize(QSize(16, 16))
        self.add_contact_button.setProperty("role", "primary")
        self.add_contact_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_contact_button.setMinimumHeight(38)
        self.add_contact_button.setMinimumWidth(142)
        self.add_contact_button.setEnabled(False)
        self.add_contact_button.clicked.connect(self._add_contact)
        header.addWidget(self.add_contact_button, 0, Qt.AlignmentFlag.AlignTop)
        layout.addLayout(header)

        self.workspace_tabs = QTabWidget()
        self.workspace_tabs.setDocumentMode(True)
        self.workspace_tabs.addTab(self._overview_tab(), "Overview")
        self.workspace_tabs.addTab(self._contacts_tab(), "Contacts")
        layout.addWidget(self.workspace_tabs, 1)
        return workspace

    def _table_card(self, stack: QStackedWidget) -> QFrame:
        card = QFrame()
        card.setObjectName("tableCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(0)
        layout.addWidget(stack)
        return card

    def _search_field(self, placeholder: str) -> QLineEdit:
        field = QLineEdit()
        field.setObjectName("searchInput")
        field.setPlaceholderText(placeholder)
        field.setClearButtonEnabled(True)
        field.setMinimumHeight(38)
        field.setTextMargins(28, 0, 8, 0)
        field.addAction(
            line_icon("search", "#64748B", 18),
            QLineEdit.ActionPosition.LeadingPosition,
        )
        return field

    def _overview_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 16, 0, 0)
        layout.setSpacing(12)

        self.overview_search = self._search_field(
            "Search by company, contact, email or address…"
        )
        self.overview_search.textChanged.connect(self._filter_overview)
        layout.addWidget(self.overview_search)

        self.workspace_table = ResponsiveTable(
            0,
            7,
            ratios={0: 0.24, 1: 0.17, 2: 0.20, 3: 0.17, 4: 0.22},
            fixed_columns={5: 96, 6: 72},
        )
        self.workspace_table.setHorizontalHeaderLabels(
            (
                "Company",
                "Website",
                "Company email",
                "Contact",
                "Contact email",
                "Priority",
                "Actions",
            )
        )
        configure_table(self.workspace_table)
        for column in (5, 6):
            header_item = self.workspace_table.horizontalHeaderItem(column)
            if header_item is not None:
                header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.workspace_table.cellDoubleClicked.connect(
            lambda row, _column: self._edit_record(self.workspace_rows[row])
        )

        self.overview_empty = EmptyState()
        self.overview_stack = QStackedWidget()
        self.overview_stack.addWidget(self.workspace_table)
        self.overview_stack.addWidget(self.overview_empty)
        layout.addWidget(self._table_card(self.overview_stack), 1)
        return tab

    def _contacts_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 16, 0, 0)
        layout.setSpacing(12)

        self.contacts_search = self._search_field(
            "Search contacts by name, company, email or phone…"
        )
        self.contacts_search.textChanged.connect(self._filter_contacts)
        layout.addWidget(self.contacts_search)

        self.contacts_table = ResponsiveTable(
            0,
            7,
            ratios={0: 0.145, 1: 0.165, 2: 0.155, 3: 0.115, 4: 0.185, 5: 0.12, 6: 0.115},
        )
        self.contacts_table.setHorizontalHeaderLabels(
            (
                "Name",
                "Company",
                "Job title",
                "Department",
                "Email",
                "Phones",
                "Social accounts",
            )
        )
        configure_table(self.contacts_table)

        self.contacts_empty = EmptyState()
        self.contacts_stack = QStackedWidget()
        self.contacts_stack.addWidget(self.contacts_table)
        self.contacts_stack.addWidget(self.contacts_empty)
        layout.addWidget(self._table_card(self.contacts_stack), 1)
        return tab

    # --------------------------------------------------------------- behaviour

    def _selected_domain(self) -> dict | None:
        item = self.domain_list.currentItem()
        return item.data(Qt.ItemDataRole.UserRole) if item else None

    def _clear_filters(self) -> None:
        for field in (self.overview_search, self.contacts_search):
            field.blockSignals(True)
            field.clear()
            field.blockSignals(False)

    def _domain_selected(
        self,
        current: QListWidgetItem | None,
        _previous: QListWidgetItem | None,
    ) -> None:
        domain = current.data(Qt.ItemDataRole.UserRole) if current else None
        has_domain = domain is not None
        if current is not None and _previous is not None and _previous is not current:
            self._clear_filters()
        self.edit_button.setEnabled(has_domain)
        self.delete_button.setEnabled(has_domain)
        self.add_contact_button.setEnabled(has_domain)
        self.overview_search.setEnabled(has_domain)
        self.contacts_search.setEnabled(has_domain)

        if domain is None:
            self.workspace_title.setText("Select a domain")
            self.workspace_title.setToolTip("")
            self.workspace_status.setText(
                "Choose a domain from the sidebar to open its workspace."
            )
            self.status_badge.hide()
            self.all_workspace_rows = []
            self.all_contact_rows = []
            self._fill_overview([])
            self._fill_contacts([])
            return

        self.workspace_title.setText(domain["domain_name"])
        self.workspace_title.setToolTip(domain["domain_name"])
        self.workspace_status.setText(
            "Manage companies, contacts and outreach details for this domain."
        )
        self._show_status_badge(domain.get("status") or "active")

        raw_rows = self.workspace_service.list_domain_workspace(domain["id"])
        self.all_workspace_rows = aggregate_overview_rows(raw_rows)
        self._filter_overview(self.overview_search.text())
        contact_rows = self.workspace_service.list_domain_contacts(domain["id"])
        self.all_contact_rows = aggregate_contact_rows(contact_rows)
        self._filter_contacts(self.contacts_search.text())

    def _show_status_badge(self, status: str) -> None:
        value = (status or "active").strip().lower()
        self.status_badge.setText(value.capitalize())
        self.status_badge.setProperty(
            "tone", value if value in ("active", "sold", "archived") else "none"
        )
        repolish(self.status_badge)
        self.status_badge.show()

    def _add_domain(self) -> None:
        dialog = DomainDialog(self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        try:
            domain_id = self.domain_service.create_domain(dialog.value())
            self._clear_filters()
            self.refresh_domains(select_id=domain_id)
        except (ValidationError, DuplicateRecordError) as error:
            self._show_error(error)

    def _edit_domain(self) -> None:
        domain = self._selected_domain()
        if domain is None:
            return
        dialog = DomainDialog(self, domain["domain_name"])
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        try:
            self.domain_service.update_domain(domain["id"], dialog.value())
            self.refresh_domains(select_id=domain["id"])
        except (ValidationError, DuplicateRecordError) as error:
            self._show_error(error)

    def _delete_domain(self) -> None:
        domain = self._selected_domain()
        if domain is None:
            return
        box = QMessageBox(self)
        box.setWindowTitle("Delete domain")
        box.setIcon(QMessageBox.Icon.Warning)
        box.setText(f"Delete {domain['domain_name']}?")
        box.setInformativeText(
            "Related leads will also be removed. This action cannot be undone."
        )
        box.setStandardButtons(
            QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Yes
        )
        box.setDefaultButton(QMessageBox.StandardButton.Cancel)
        delete_button = box.button(QMessageBox.StandardButton.Yes)
        delete_button.setText("Delete")
        delete_button.setProperty("role", "dangerSolid")
        repolish(delete_button)
        box.button(QMessageBox.StandardButton.Cancel).setText("Cancel")
        if box.exec() == QMessageBox.StandardButton.Yes:
            self.domain_service.delete_domain(domain["id"])
            self._clear_filters()
            self.refresh_domains()

    def _add_contact(self) -> None:
        domain = self._selected_domain()
        if domain is None:
            return
        dialog = ProspectDialog(self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        try:
            self.workspace_service.add_prospect(domain["id"], dialog.values())
            self._domain_selected(self.domain_list.currentItem(), None)
        except (ValidationError, DuplicateRecordError) as error:
            self._show_error(error)

    def _edit_record(self, record: dict) -> None:
        full_record = self.workspace_service.get_edit_record(record["lead_id"])
        dialog = ProspectDialog(self, full_record)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        try:
            self.workspace_service.update_record(dialog.values())
            self._domain_selected(self.domain_list.currentItem(), None)
        except (ValidationError, DuplicateRecordError) as error:
            self._show_error(error)

    def _show_error(self, error: Exception) -> None:
        QMessageBox.critical(self, "Could not save", str(error))

    def refresh_domains(self, select_id: int | None = None) -> None:
        self.domain_rows = self.domain_service.list_domains()
        self.domain_list.blockSignals(True)
        self.domain_list.clear()
        selected_row = 0
        for index, domain in enumerate(self.domain_rows):
            item = QListWidgetItem(domain["domain_name"])
            item.setData(Qt.ItemDataRole.UserRole, domain)
            item.setSizeHint(QSize(200, 44))
            item.setToolTip(domain["domain_name"])
            self.domain_list.addItem(item)
            if domain["id"] == select_id:
                selected_row = index
        self.domain_list.blockSignals(False)
        self.domains_hint.setVisible(not self.domain_rows)
        if self.domain_rows:
            self.domain_list.setCurrentRow(selected_row)
        else:
            self._domain_selected(None, None)

    def _fill_overview(self, rows: list[dict]) -> None:
        self.workspace_rows = rows
        self.workspace_table.setRowCount(len(rows))
        fields = ("company_name", "website", "company_email", "contact_name", "contact_email")
        for row_index, row in enumerate(rows):
            for column_index, field in enumerate(fields):
                raw = str(row.get(field) or "").strip()
                item = QTableWidgetItem(display_value(raw))
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
                )
                if raw:
                    item.setToolTip(raw)
                if column_index == 0:
                    font = item.font()
                    font.setWeight(QFont.Weight.DemiBold)
                    item.setFont(font)
                self.workspace_table.setItem(row_index, column_index, item)

            self.workspace_table.setCellWidget(
                row_index, 5, priority_cell(row.get("priority"))
            )
            edit_container = centered_table_button(
                self.workspace_table, "edit", "Edit this record", "#64748B"
            )
            edit_button = edit_container.findChild(QPushButton)
            edit_button.clicked.connect(
                lambda _checked=False, item=row: self._edit_record(item)
            )
            self.workspace_table.setCellWidget(row_index, 6, edit_container)

        self._update_overview_empty(rows)

    def _filter_overview(self, text: str) -> None:
        query = text.strip().casefold()
        if not query:
            self._fill_overview(self.all_workspace_rows)
            return
        searchable_fields = (
            "company_name",
            "contact_name",
            "address",
            "company_email",
            "contact_email",
        )
        filtered = [
            row
            for row in self.all_workspace_rows
            if any(
                query in str(row.get(field) or "").casefold()
                for field in searchable_fields
            )
        ]
        self._fill_overview(filtered)

    def _filter_contacts(self, text: str) -> None:
        query = text.strip().casefold()
        if not query:
            self._fill_contacts(self.all_contact_rows)
            return
        searchable_fields = (
            "full_name",
            "company_name",
            "job_title",
            "department",
            "email",
            "phones",
            "socials",
        )
        filtered = [
            row
            for row in self.all_contact_rows
            if any(
                query in str(row.get(field) or "").casefold()
                for field in searchable_fields
            )
        ]
        self._fill_contacts(filtered)

    def _fill_contacts(self, rows: list[dict]) -> None:
        self.contacts_table.setRowCount(len(rows))
        fields = (
            "full_name",
            "company_name",
            "job_title",
            "department",
            "email",
            "phones",
            "socials",
        )
        for row_index, row in enumerate(rows):
            for column_index, field in enumerate(fields):
                raw = str(row.get(field) or "").strip()
                item = QTableWidgetItem(display_value(raw))
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
                )
                if raw:
                    item.setToolTip(raw)
                if column_index == 0:
                    font = item.font()
                    font.setWeight(QFont.Weight.DemiBold)
                    item.setFont(font)
                self.contacts_table.setItem(row_index, column_index, item)
        self._update_contacts_empty(rows)

    def _update_overview_empty(self, rows: list[dict]) -> None:
        has_domain = self._selected_domain() is not None
        query = self.overview_search.text().strip()
        if not has_domain:
            self.overview_empty.set_content(
                "globe",
                "No domain selected",
                "Choose a domain from the sidebar to open its workspace.",
            )
        elif not rows:
            if query:
                self.overview_empty.set_content(
                    "search",
                    "No matches",
                    "Try a different search term or clear the search.",
                    "Clear search",
                    self.overview_search.clear,
                )
            else:
                self.overview_empty.set_content(
                    "inbox",
                    "No contacts yet",
                    "Add the first company and contact for this domain.",
                    "Add contact",
                    self._add_contact,
                )
        if not rows:
            self.overview_stack.setCurrentWidget(self.overview_empty)
        else:
            self.overview_stack.setCurrentWidget(self.workspace_table)

    def _update_contacts_empty(self, rows: list[dict]) -> None:
        has_domain = self._selected_domain() is not None
        query = self.contacts_search.text().strip()
        if not has_domain:
            self.contacts_empty.set_content(
                "globe",
                "No domain selected",
                "Choose a domain from the sidebar to open its workspace.",
            )
        elif not rows:
            if query:
                self.contacts_empty.set_content(
                    "search",
                    "No matches",
                    "Try a different search term or clear the search.",
                    "Clear search",
                    self.contacts_search.clear,
                )
            else:
                self.contacts_empty.set_content(
                    "inbox",
                    "No contacts yet",
                    "Add a contact to see it here.",
                    "Add contact",
                    self._add_contact,
                )
        if not rows:
            self.contacts_stack.setCurrentWidget(self.contacts_empty)
        else:
            self.contacts_stack.setCurrentWidget(self.contacts_table)

    def run(self) -> None:
        self.showMaximized()
