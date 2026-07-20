# coding=utf-8
from code_wizards.wizard import Wizard
from code_plumbing import lib
from PyQt6.QtGui import QTextDocument
from PyQt6.QtWidgets import QTextEdit, QDialog, QVBoxLayout


class Necromancer(Wizard):
    def __init__(self, planetary_conjunction_dict):
        super().__init__(planetary_conjunction_dict)

    def make_magic_number(self):
        conjunctions = self.planet_conjunction_dict
        print("Conjunctions are: " + str(conjunctions))
        saturn_conjunctions = conjunctions[lib.SATURN]
        necromancer_magic_number = 0b0000000
        if len(saturn_conjunctions) == 0:
            print("Saturn Stands Alone")
            necromancer_magic_number ^= (1 << 0)
        if lib.MERCURY in saturn_conjunctions:
            print("Mercury in Conjunction")
            necromancer_magic_number ^= (1 << 1)
        if lib.VENUS in saturn_conjunctions:
            print("Venus in Conjunction")
            necromancer_magic_number ^= (1 << 2)
        if lib.MARS in saturn_conjunctions:
            print("Mars in Conjunction")
            necromancer_magic_number ^= (1 << 3)
        if lib.JUPITER in saturn_conjunctions:
            print("Jupiter in Conjunction")
            necromancer_magic_number ^= (1 << 4)
        if lib.SOL in saturn_conjunctions:
            print("Sol in Conjunction")
            necromancer_magic_number ^= (1 << 5)
        print(necromancer_magic_number)
        return necromancer_magic_number

    def popup(self):
        necro_pop = QDialog()
        necro_pop.setWindowTitle("Necromancer Reads the Stars")
        layout = QVBoxLayout(necro_pop)

        self.read_the_stars()
        saturn_document = QTextDocument()
        saturn_document.setHtml(self.read_the_stars_html)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setDocument(saturn_document)

        layout.addWidget(text)

        necro_pop.resize(900, 600)
        necro_pop.exec()

    def read_the_stars(self):
        magic_number = self.make_magic_number()

        saturn_alone_html = ""
        if magic_number & (1 << 0):
            saturn_alone_html = """
                        <h2> Saturn Stands Alone -- Tragedy outside Isha brings many new souls to its Gates. </h2>
                        Add a total of eight Souls to the Edge of Life, distributed in any fashion.
                    """

        saturn_mercury_html = ""
        if magic_number & (1 << 1):
            saturn_mercury_html = """
                        <h2> Mercury in Conjunction with Saturn -- The dead claw against the Gates. </h2>
                        Move all Foes closer to life again.
                    """

        saturn_venus_html = ""
        if magic_number & (1 << 2):
            saturn_venus_html = """
                               <h2> Venus in Conjunction with Saturn -- Allies of Death grow distant and long for release. </h2>
                                Move any Ally of your choice to a connected further Gate.
                           """

        saturn_mars_html = ""
        if magic_number & (1 << 3):
            saturn_mars_html = """
                                       <h2> Mars in Conjunction with Saturn -- Primordial evil festers in distant lands. </h2>
                                       I. The furthest non-Hostile Gate becomes Hostile. <br>
                                       II. Move all Foes in Hostile Gates (or in spaces adjacent to Hostile Gates) closer to life.
                                   """

        saturn_jupiter_html = ""
        if magic_number & (1 << 4):
            saturn_jupiter_html = """
                                            <h2> Jupiter in Conjunction with Saturn -- The Allies of the Necromancer lack their power entirely.</h2>
                                            As long as this conjunction remains, they cannot prevent Foes from moving closer to life. <italic>(This does not apply to Reliable Ghoul-Callers.)</italic>
                                        """

        saturn_sol_html = ""
        if magic_number & (1 << 5):
            saturn_sol_html = """
                                               <h2> Sol in Conjunction with Saturn -- The armies of death coordinate together and march against you.</h2>
                                               Move all Foes closer to life. If they would be stopped by an Ally, destroy that Ally.
                                           """
        self.set_date_string()
        self.read_the_stars_html = f"""
                    <div style="font-family: serif;">
                      <h1 class="break-page"> Gate-Watcher who is concerned with the movement of %s </h1>
                      {saturn_alone_html}
                      {saturn_mercury_html}
                      {saturn_venus_html}
                      {saturn_mars_html}
                      {saturn_jupiter_html}
                      {saturn_sol_html}
                      <br><br><br>
                          <center><h3> Report produced for {self.date_string}</h3> </center>
                    </div>
                """ % lib.SATURN
