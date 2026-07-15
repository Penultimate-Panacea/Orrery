# coding=utf-8
from wizard import Wizard
import lib
from PyQt6.QtGui import QTextDocument
from PyQt6.QtWidgets import QTextEdit, QDialog, QVBoxLayout
class Sorcerer(Wizard):
    def __init__(self,planetary_conjunction_dict):
        super().__init__(planetary_conjunction_dict)

    def make_magic_number(self):
        conjunctions = self.planet_conjunction_dict
        print("Conjunctions are: " + str(conjunctions))
        sol_conjunctions = conjunctions[lib.SOL]
        sorcerer_magic_number =0b0000000
        if len(sol_conjunctions) == 0:
            print ("Sol Stands Alone")
            sorcerer_magic_number ^= ( 1 << 0)

        if (lib.MERCURY in sol_conjunctions) ^ (lib.VENUS in sol_conjunctions):
            print ("Mercury or Venus in Conjunction")
            sorcerer_magic_number ^= (1 << 1)

        if lib.MERCURY in sol_conjunctions and lib.VENUS in sol_conjunctions:
            print ("Mercury and Venus in Conjunction")
            sorcerer_magic_number ^= (1 << 2)

        if lib.MARS in sol_conjunctions:
            print ("Mars in Conjunction")
            sorcerer_magic_number ^= (1 << 3)

        if lib.JUPITER in sol_conjunctions:
            print ("Jupiter in Conjunction")
            sorcerer_magic_number ^= (1 << 4)

        if lib.SATURN in sol_conjunctions:
            print ("Saturn in Conjunction")
            sorcerer_magic_number ^= (1 << 5)
        print(sorcerer_magic_number)
        self.sorcerer_popup(sorcerer_magic_number)
        return
            ## TODO: Magic number bits 6 & 7 are reserved for calamity and extinction which are beyond the scope of the project at the moment
    def sorcerer_popup(self, magic_number):
        sorc_pop = QDialog()
        sorc_pop.setWindowTitle("Sorcerer Reads the Stars")

        layout = QVBoxLayout(sorc_pop)  # attach layout to the dialog

        sol_alone_html = ""
        if magic_number & (1 << 0):
            sol_alone_html = """
                <h3> Sol Stands Alone -- Magic dreams of Wildness, and it sparks across the land</h3>
                    For each Region with any number of Hidden Traces on it, double the number of Traces in that region. If there are no hidden traces, instead ask the Celestial Audience which Wizard has the last control over his Domain. Place a Hidden Trace in each Region of that Wizard's Domain.
                """

        sol_mercury_OR_venus_html = ""
        if magic_number & (1 << 1):
            sol_mercury_OR_venus_html = """
                <h3> Mercury or Venus in Conjunction -- Magic dreams of Power, and those who serve it feel its call.</h3>
                Place a hidden trace on each Occultist. If there are no Occultists, place a new Occultist, accompanied by three Hidden Traces, in one of the Wizard's Authorities.
            """

        sol_mercury_AND_venus_html = ""
        if magic_number & (1 << 2):
            sol_mercury_AND_venus_html = """
                       <h3> Mercury and Venus in Conjunction -- Magic dreams of Power, and those who serve it feel its call </h3>
                       I.   Place a hidden trace on each Occultist. <br>
                       II.  Place a new Occultist, accompanied by three Hidden Traces, in one of the Wizard's Authorities.
                   """

        sol_mars_html = ""
        if magic_number & (1 << 3):
            sol_mars_html = """
                               <h3> Mars in Conjunction -- Magic dreams of excitement, and across the Faraway Sea, the world hears its call.</h3>
                               For each Region with a Trace on it, place another Hidden Trace upon it. If fewer than three Traces are placed in this way, then place two Hidden Traces on three different Islands.
                           """

        sol_jupiter_html = ""
        if magic_number & (1 << 4):
            sol_jupiter_html = """
                                    <h3> Jupiter in Conjunction -- Magic dreams of wisdom, and its students become fascinated with its seductive power.</i></h3>
                                    I.  Put a Hidden Trace on one of your Agents. <br>
                                    II. They become an Occultist.<br>
                                    The Agent will remain loyal (and the Academy will thus remain under your Control) until you Confiscate the Agent's Traces, at which point they will depart the Academy and move into an adjacent Domain. <br>
                                    <b>If there is already an Occultist on an Academy,</b> or if you have no Agents, instead ask the Celestial Audience which Domain is stealing from your own, and move half of all Traces in your Tower into that Domain's Authority. These Traces become Hidden.
                                """

        sol_saturn_html = ""
        if magic_number & (1 << 5):
            sol_saturn_html = """
                                       <h3> Saturn in Conjunction -- Magic dreams of desolation, and its presence in Isha leads to calamity.</h3>
                                       Place three Hidden Traces in one of the Secret Regions, as dangerous power builds at the edge of the world. Ask the Wizard whose Domain it falls under to invent a mighty enemy Occultist, but to keep them secret from you for now --- you can discover who they are when you Investigate.
                                   """
        sol_stars_html = f"""
            <div style="font-family: serif;">
              <h2> Hierophant </h2>
              {sol_alone_html}
              {sol_mercury_OR_venus_html}
              {sol_mercury_AND_venus_html}
              {sol_mars_html}
              {sol_saturn_html}
              {sol_jupiter_html}
            </div>
        """

        sol_document = QTextDocument()
        sol_document.setHtml(sol_stars_html)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setDocument(sol_document)

        layout.addWidget(text)

        sorc_pop.resize(900, 600)
        sorc_pop.exec()