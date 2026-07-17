# coding=utf-8
from code_wizards.wizard import Wizard
from code_plumbing import lib
from PyQt6.QtGui import QTextDocument
from PyQt6.QtWidgets import QTextEdit, QDialog, QVBoxLayout
class Hierophant(Wizard):
    def __init__(self,planetary_conjunction_dict):
        super().__init__(planetary_conjunction_dict)

    def make_magic_number(self):
        conjunctions = self.planet_conjunction_dict
        print("Conjunctions are: " + str(conjunctions))
        jupiter_conjunctions = conjunctions[lib.JUPITER]
        hierophant_magic_number = 0b0000000
        if len(jupiter_conjunctions) == 0:
            print("Jupiter Stands Alone")
            hierophant_magic_number ^= (1 << 0)

        if lib.MERCURY in jupiter_conjunctions:
            print("Mercury in Conjunction")
            hierophant_magic_number ^= (1 << 1)

        if lib.VENUS in jupiter_conjunctions:
            print("Venus in Conjunction")
            hierophant_magic_number ^= (1 << 2)

        if lib.MARS in jupiter_conjunctions:
            print("Mars in Conjunction")
            hierophant_magic_number ^= (1 << 3)

        if lib.SATURN in jupiter_conjunctions:
            print("Saturn in Conjunction")
            hierophant_magic_number ^= (1 << 4)
        if lib.SOL in jupiter_conjunctions:
            print("Sol in Conjunction")
            hierophant_magic_number ^= (1 << 5)
        print(hierophant_magic_number)
        return hierophant_magic_number
        ## TODO: Magic number bits 6 & 7 are reserved for calamity and extinction which are beyond the scope of the project at the moment


    def hierophant_popup(self):
        hiero_pop = QDialog()
        hiero_pop.setWindowTitle("Hierophant Reads the Stars")
        self.read_the_stars()

        jupiter_document = QTextDocument()
        jupiter_document.setHtml(self.read_the_stars_html)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setDocument(jupiter_document)

        layout = QVBoxLayout(hiero_pop)
        layout.addWidget(text)

        hiero_pop.resize(900, 600)
        hiero_pop.exec()

    def read_the_stars(self):
        magic_number = self.make_magic_number()

        jupiter_alone_html = ""
        if magic_number & (1 << 0):
            jupiter_alone_html = """
                        <h2> Jupiter Stands Alone -- The masses are <i>Starving</i>. </h2>
                            Take from each Temple, then create a Throng of Petitioners in the Temple with the fewest Abundances, representing a community in desperate need of help.
                        """

        jupiter_mercury_html = ""
        if magic_number & (1 << 1):
            jupiter_mercury_html = """
                        <h2> Mercury in Conjunction -- The masses are <i>Demanding</i>. </h2>
                        All Petitioners gain another Hunger. If there are no Petitioners, create a Petitioner in a Temple --- a lost soul with nowhere else to turn.
                    """

        jupiter_venus_html = ""
        if magic_number & (1 << 2):
            jupiter_venus_html = """
                               <h2> Venus in Conjunction -- The masses are <i>Devoted</i>. </h2>
                               I.   Add a new Patron to a Temple. <br>
                               II.  Create a Throng of Petitioners at that Temple --- a surge of faithful looking for support
                           """

        jupiter_mars_html = ""
        if magic_number & (1 << 3):
            jupiter_mars_html = """
                                       <h2> Mars in Conjunction -- The masses are <i>Violent</i></h2>
                                       Each Petitioner Takes from their associated Temple (<i>this doesn't satisfy Hunger</i>). If there are no Petitioners, createa Petitoner in a Temple --- a heartbroken soul whose home was destroyed by violence.
                                   """

        jupiter_saturn_html = ""
        if magic_number & (1 << 4):
            jupiter_saturn_html = """
                                            <h2> Saturn in Conjunction -- The masses are <i>Superstitious</i></h2>
                                            You must Spend Time this month sacrificing a named character to the Immortal Flames. Choose someone, and ask the Celestial Audience if any of them have the right to stop the sacrifice (through the king's authority, someone's destiny, and so on). If someone stops you, they take a Major Complication. If you don't sacrifice somone by the end of the month, create a Throng of Petitoners in the Temple with the fewest Abundances, convinced that the world is ending once more.
                                        """

        jupiter_sol_html = ""
        if magic_number & (1 << 5):
            jupiter_sol_html = """
                                               <h2> Sol in Conjunction -- The masses are <i>Observant</i></h2>
                                               Choose a Holidat this month. It counts as a Feast Day for the rest of the month. If the current month is already a Feast Day, instead a new Prophet appears at the Temple with the greatest number of Abundances, preaching of a radical interpeation to the Orthodoxy of the Immortal Flame.
                                           """
        self.read_the_stars_html = f"""
                    <div style="font-family: serif;">
                      <h1 class="break-page"> Keeper of the Flames whose fate is controlled by %s </h1> 
                      {jupiter_alone_html}
                      {jupiter_mercury_html}
                      {jupiter_venus_html}
                      {jupiter_mars_html}
                      {jupiter_saturn_html}
                      {jupiter_sol_html}
                    </div>
                """ % lib.JUPITER
        return