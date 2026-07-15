# coding=utf-8
from wizard import Wizard
import lib
from PyQt6.QtGui import QTextDocument
from PyQt6.QtWidgets import QTextEdit, QDialog, QVBoxLayout
class Faustian(Wizard):
    def __init__(self,planetary_conjunction_dict):
        super().__init__(planetary_conjunction_dict)

    def generate_faust_factor(self):
        conjunctions = self.planet_conjunction_dict()
        print("Conjunctions are: " + str(conjunctions))
        mercury_conjunctions = conjunctions[lib.MERCURY]
        faust_factor = len(mercury_conjunctions)
        self.faustian_popup(faust_factor)
        return
    def faustian_popup(self, magic_number):
        faust_pop = QDialog()
        faust_pop.setWindowTitle("Faustian Reads the Stars")

        layout = QVBoxLayout(faust_pop)
        mercury_alone_html = ""
        mercury_among_html = ""
        if magic_number == 0:
            mercury_alone_html = """
                <h3> The Devil seeks the affection of another Wizard.</h3>
                    Another Wizard recieves an invitation to Spend Time and have a Scene with the Devil, in which the Devil will make him a Bargain. If a Wizard refuses to meet with the Devil at all, the Devil places a Scheme onto each of that Wizard's Communities.
                """
        else:
            mercury_among_html = """
            <h3> The Devil Schemes </h3>
            Place two Scheme Cards per planet in conjunction with the current house.
            """

        mercury_stars_html = f"""
            <div style="font-family: serif;">
              <h2> Faustian </h2>
              {mercury_alone_html}
              {mercury_among_html}
            </div>
        """

        faust_document = QTextDocument()
        faust_document.setHtml(mercury_stars_html)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setDocument(faust_document)

        layout.addWidget(text)

        faust_pop.resize(900, 600)
        faust_pop.exec()