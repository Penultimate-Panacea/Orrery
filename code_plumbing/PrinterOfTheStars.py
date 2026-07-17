# coding=utf-8
import time
from code_plumbing.lib import current_year
from PyQt6.QtWidgets import QApplication, QDialog, QLabel,QProgressBar,QVBoxLayout
from PyQt6.QtCore import Qt,QTimer
from PyQt6.QtGui import QTextDocument, QPageSize
from PyQt6.QtPrintSupport import QPrinter, QPrinterInfo

class SpoolingDialog(QDialog):
    def __init__(self, parent=None, message: str = "Sending print job…"):
        super().__init__(parent)
        self.setWindowTitle("Printing")
        self.setModal(True)

        layout = QVBoxLayout(self)

        self.label = QLabel(message)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.bar = QProgressBar()
        self.bar.setRange(0, 0)  # indeterminate to avoid thread issues

        layout.addWidget(self.label)
        layout.addWidget(self.bar)

        self.resize(320, 90)


class PrinterOfTheStars:
    def __init__(self, wizards, planets, timeout_s: int = 30, printer_name: str | None = None):
        self.wizards = wizards
        month_index = planets[5].current_step
        months = [
            'April', 'May', 'June', 'July', 'August', 'September',
            'October', 'November', 'December', 'January', 'February', 'March'
        ]
        self.date = months[month_index].join(str(current_year))

        self.timeout_s = timeout_s
        self.printer_name = printer_name

        self.document = self.assemble_document()

    def assemble_document(self) -> str:
        full_html = f"""<html><head></head><body>
<h1 class="break-page"> The Report on the Stars as of {self.date} </h1>"""
        for w in self.wizards:
            full_html += w.read_the_stars_html
        full_html += "</body></html>"
        return full_html

    def _configure_printer(self) -> QPrinter:
        printer = QPrinter(QPrinterInfo.defaultPrinter())

        # a bit of future proofing if multiplre printers are to be used
        if self.printer_name:
            chosen = next(
                (p for p in QPrinterInfo.availablePrinters() if p.printerName() == self.printer_name),
                None
            )
            if chosen is not None:
                printer.setPrinterName(chosen.printerName())

        printer.setPageSize(QPageSize(QPageSize.PageSizeId.Letter))
        printer.setFontEmbeddingEnabled(True)

        # Make Qt fill the page
        printer.setFullPage(True)

        return printer

    def print_html_to_default_printer(self) -> None:
        # Qt requires a QApplication for printing
        app = QApplication.instance()
        # if app is None:
       #     app = QApplication([])

        printer = self._configure_printer()

        doc = QTextDocument()
        doc.setHtml(self.document)

        dlg = SpoolingDialog(message="Sending to printer (spooling may take a moment)…")
        dlg.show()
        doc.print(printer)
        grace_ms = 2500  # was effectively ~2s sleep
        QTimer.singleShot(grace_ms, dlg.accept)

    def print_html(self) -> None:
        self.print_html_to_default_printer()