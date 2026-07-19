# coding=utf-8
import code_plumbing.lib as lib
from math import floor
from PyQt6.QtGui import QTextDocument
from PyQt6.QtWidgets import QTextEdit, QDialog, QVBoxLayout

class Wizard:
    def __init__(self,planet_conjunction_dict):
        self.associated_planet = None
        self.water = None
        self.fire = None
        self.earth = None
        self.air = None
        self.planet_conjunction_dict = planet_conjunction_dict
        self.read_the_stars_html = f"""<h1>NO READ THE STARS TEXT FOUND</h1>"""
        self.date_string = None

    def update_conjunctions(self, new_dict):
        self.planet_conjunction_dict = new_dict

    def set_date_string(self) -> None:
        months = [
            'April', 'May', 'June', 'July', 'August', 'September',
            'October', 'November', 'December', 'January', 'February', 'March'
        ]
        date_string = str(months[lib.current_cycle % 12])
        date_string += ' of Year '
        date_string += str(floor(lib.current_cycle / 12))
        date_string += ' in the '
        date_string += lib.name_of_calendar
        self.date_string = date_string

    def popup(self):
        wiz_pop = QDialog()
        wiz_pop.setWindowTitle("Generic Wizard Popup")
        layout = QVBoxLayout(wiz_pop)
        wiz_document = QTextDocument()
        wiz_document.setHtml("""<h1>ERROR: Generic Wizard Popup</h1>""")

        text = QTextEdit()
        text.setReadOnly(True)
        text.setDocument(wix_document)

        layout.addWidget(text)

        wiz_pop.resize(900, 600)
        wiz_pop.exec()