# coding=utf-8
from code_wizards.wizard import Wizard
from code_plumbing import lib
from PyQt6.QtGui import QTextDocument
from PyQt6.QtWidgets import QTextEdit, QDialog, QVBoxLayout

class Faustian(Wizard):
    def __init__(self,planetary_conjunction_dict, house_planet_conjunctions):
        super().__init__(planetary_conjunction_dict)
        self.house_planet_conjunctions = house_planet_conjunctions

    def faustian_popup(self):
        faust_pop = QDialog()
        faust_pop.setWindowTitle("Faustian Reads the Stars")

        faust_document = QTextDocument()
        self.read_the_stars()
        faust_document.setHtml(self.read_the_stars_html)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setDocument(faust_document)
        layout = QVBoxLayout(faust_pop)
        layout.addWidget(text)

        faust_pop.resize(900, 600)
        faust_pop.exec()

    def read_the_stars(self):

        self.set_date_string()
        self.read_the_stars_html = f"""
                    <div style="font-family: serif;">
                      <h1 class="break-page"> Keeper of the Chains whose fate is controlled by %s </h1>
                      {}
                      {}
                      <br><br><br>
                          <center><h3> Report produced for {self.date_string}</h3> </center>
                    </div>
                """ % lib.MERCURY
        return