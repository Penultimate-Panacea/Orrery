# coding=utf-8
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy, QTextBrowser
from PyQt6.QtSvgWidgets import QSvgWidget



class MoonPhaseWidget(QWidget):
    """
    Displays the current SVG from a list, a Next button, and an HTML info area.
    """
    def __init__(self, svg_paths: list[str], html_snippets: list[str] | None = None, parent=None):
        super().__init__(parent)

        self.svg_paths = svg_paths or []
        self.html_snippets = html_snippets or [""] * len(self.svg_paths)
        if len(self.html_snippets) < len(self.svg_paths):
            self.html_snippets += [""] * (len(self.svg_paths) - len(self.html_snippets))

        self.index = 0

        # --- UI ---
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        top_row = QHBoxLayout()
        top_row.setSpacing(10)

        self.svg_title = QLabel("Game Phase")
        self.svg_title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.next_btn = QPushButton("Next Phase")
        self.next_btn.clicked.connect(self.next_svg)

        top_row.addWidget(self.svg_title, 1)
        top_row.addWidget(self.next_btn, 1)

        self.svg_widget = QSvgWidget()
        self.svg_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.svg_widget.setMinimumHeight(260)

        self.info_browser = QTextBrowser()
        self.info_browser.setOpenExternalLinks(True)

        main_layout.addLayout(top_row)
        main_layout.addWidget(self.svg_widget, 0)
        main_layout.addWidget(self.info_browser, 2)

        if not self.svg_paths:
            self.info_browser.setHtml("<b>No SVGs provided.</b>")
            self.next_btn.setEnabled(False)
        else:
            self.update_view()

    def current_svg_path(self) -> str | None:
        if 0 <= self.index < len(self.svg_paths):
            return self.svg_paths[self.index]
        return None

    def update_view(self):
        path = self.current_svg_path()
        if not path or not os.path.exists(path):
            self.svg_widget.load(b"")
            self.info_browser.setHtml("<b>Missing SVG file.</b>")
            return

        self.svg_title.setText(f"Game Phase ({self.index + 1}/{len(self.svg_paths)})")
        self.svg_widget.load(path)

        html_item = self.html_snippets[self.index] if self.index < len(self.html_snippets) else ""

        # If html_item is a file path, load its contents
        if isinstance(html_item, str) and os.path.exists(html_item):
            with open(html_item, "r", encoding="utf-8") as f:
                html = f.read()
        else:
            # Otherwise assume html_item already IS the HTML string
            html = html_item or ""

        self.info_browser.setHtml(html)

        w = self.svg_widget.size().width()
        if w <= 0:
            return
        self.svg_widget.setMaximumHeight(w)

    def next_svg(self):
        if not self.svg_paths:
            return
        self.index = (self.index + 1) % len(self.svg_paths)
        self.update_view()

# -----------------------------