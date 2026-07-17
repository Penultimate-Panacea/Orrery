# coding=utf-8
from wizard import Wizard
from code_plumbing import lib
from PyQt6.QtGui import QTextDocument
from PyQt6.QtWidgets import QTextEdit, QDialog, QVBoxLayout
class Necromancer(Wizard):
    def __init__(self,planetary_conjunction_dict):
        super().__init__(planetary_conjunction_dict)

    def make_magic_number(self):
        conjunctions = self.planet_conjunction_dict
        print("Conjunctions are: " + str(conjunctions))
        saturn_conjunctions = conjunctions[lib.SATURN]
        necromancer_magic_number =0b0000000
        if len(saturn_conjunctions) == 0:
            print ("Saturn Stands Alone")
            necromancer_magic_number ^= ( 1 << 0)
        if lib.MERCURY in saturn_conjunctions:
            print ("Mercury in Conjunction")
            necromancer_magic_number ^= (1 << 1)
        if lib.VENUS in saturn_conjunctions:
            print ("Venus in Conjunction")
            necromancer_magic_number ^= (1 << 2)
        if lib.MARS in saturn_conjunctions:
            print ("Mars in Conjunction")
            necromancer_magic_number ^= (1 << 3)
        if lib.JUPITER in saturn_conjunctions:
            print ("Jupiter in Conjunction")
            necromancer_magic_number ^= (1 << 4)
        if lib.SOL in saturn_conjunctions:
            print ("Sol in Conjunction")
            necromancer_magic_number ^= (1 << 5)
        print(necromancer_magic_number)
        return necromancer_magic_number
            ## TODO: Magic number bits 6 & 7 are reserved for calamity and extinction which are beyond the scope of the project at the moment
    def necromancer_popup(self):
        necro_pop = QDialog()
        necro_pop.setWindowTitle("Necromancer Reads the Stars")

        magic_number = self.make_magic_number()

        layout = QVBoxLayout(necro_pop)  # attach layout to the dialog

        saturn_alone_html = ""
        if magic_number & (1 << 0):
            saturn_alone_html = """
                <h2> Saturn Stands Alone -- Tragedy outside Death brings many new souls to its Gates. </h2>
                Add a total of eight Souls to the Red, Yellow, and Black Gates, distributed in whatever way you please.
            """

        saturn_mercury_html = ""
        if magic_number & (1 << 1):
            saturn_mercury_html = """
                <h2> Mercury in Conjunction -- The dead claw against the Gates. </h2>
                Advance all Foes forward in Death. If a Foe is in a Near Gate, and nothing bars its way, it Escapes.
            """

        saturn_venus_html = ""
        if magic_number & (1 << 2):
            saturn_venus_html = """
                       <h2> Venus in Conjunction -- A Foe consolidates Power. </h2>
                       Create a new Foe within Death, a recent enemy of the Pact or a familiar face. Place them within any Far Gate.
                   """

        saturn_mars_html = ""
        if magic_number & (1 << 3):
            saturn_mars_html = """
                               <h2> Mars in Conjunction -- Primoridal evil festers in the furthest Gates. </h2>
                               I.   Move all Foes in Far and Furthest Gates forward. <br>
                               II.  Create a new Foe within Death, an ancient evil forgotten by the Pact who has finally escaped their bondage. Place them within Terminus.
                           """

        saturn_jupiter_html = ""
        if magic_number & (1 << 4):
            saturn_jupiter_html = """
                                    <h2> Jupiter in Conjunction -- A new Disruptive Ghoulcaller. </h2>
                                    Create a Ghoulcaller and place them in any Near Gate. As long as they continue their operations unchecked, every month all Souls and Foes of Death in an attached Far or Furthest Gate will advance towards them, like a piece of wriggling bait.
                                """

        saturn_sol_html = ""
        if magic_number & (1 << 5):
            saturn_sol_html = """
                                       <h2> Sol in Conjunction --The armies of death coordinate together and march against you. </h2>
                                       I.  Exhaust all Allies. <br>
                                       II. Advance all Foes.
                                   """
        self.read_the_stars_html = f"""
            <div style="font-family: serif;">
              <h1 class="break-page"> Keeper of the Gates whose fate is controlled by %s </h1>
              {saturn_alone_html}
              {saturn_mercury_html}
              {saturn_venus_html}
              {saturn_mars_html}
              {saturn_jupiter_html}
              {saturn_sol_html}
            </div>
        """ % lib.SATURN

        saturn_document = QTextDocument()
        saturn_document.setHtml(self.read_the_stars_html)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setDocument(saturn_document)

        layout.addWidget(text)

        necro_pop.resize(900, 600)
        necro_pop.exec()