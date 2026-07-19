# coding=utf-8
from code_wizards.wizard import Wizard
from code_plumbing import lib
from PyQt6.QtGui import QTextDocument
from PyQt6.QtWidgets import QTextEdit, QDialog, QVBoxLayout

class Faustian(Wizard):
    def __init__(self,planetary_conjunction_dict, planets):
        super().__init__(planetary_conjunction_dict)
        self.planets = planets

    def popup(self):
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
        effected_houses_by_index = self.planets[0].conjunction_table[self.planets[0].current_step]
        cards_by_house = [0,0,0,0,0,0,0,0,0,0,0,0] # list with cards by house

        for house in effected_houses_by_index:
            if (house in self.planets[1].conjunction_table[self.planets[1].current_step]) ^ (house in self.planets[2].conjunction_table[self.planets[2].current_step]):
                cards_by_house[house] += 1 # add one card to the house if just one of merc and venus are present
            elif (house in self.planets[1].conjunction_table[self.planets[1].current_step]) and (house in self.planets[2].conjunction_table[self.planets[2].current_step]):
                cards_by_house[house] += 2 # add two cards to the house if both merc and venus are present
            outer_planet_count = 0 # less elegant but easier to write version of three if ands
            if house in self.planets[3].conjunction_table[self.planets[3].current_step]:
                outer_planet_count += 1
            if house in self.planets[4].conjunction_table[self.planets[4].current_step]:
                outer_planet_count += 1
            if house in self.planets[5].conjunction_table[self.planets[5].current_step]:
                outer_planet_count += 1
            if outer_planet_count != 0:
                outer_planet_card_increase = outer_planet_count * 2
                cards_by_house[house] += outer_planet_card_increase

        aires = ""
        taurus = ""
        gemini = ""
        cancer = ""
        leo = ""
        virgo = ""
        libra = ""
        scorpio = ""
        sagittarius = ""
        capricorn = ""
        aquarius = ""
        pisces = ""
        none = ""

        if cards_by_house[0] != 0:
            aires = f"""
                    <h2> The Devil Schemes among the monks and pilgrims of the Temples in the Hierophant's domain.</h2>
                    Add %s Scheme cards from the Devil's Deck to this Community.
                    """ % cards_by_house[0]
        if cards_by_house[1] != 0:
            taurus = f"""
                    <h2> The Devil Schemes among the merchants and bankers of the Blue City in the Hierophant's domain.</h2>
                    Add %s Scheme cards from the Devil's Deck to this Community.
                    """ % cards_by_house[1]
        if cards_by_house[2] != 0:
            gemini = f"""
                    <h2> The Devil Schemes among the farmers and shepherds of the Chalk Cliffs in the Hierophant's domain.</h2>
                    Add %s Scheme cards from the Devil's Deck to this Community.
                    """ % cards_by_house[2]
        if cards_by_house[3] != 0:
            cancer = f"""
                    <h2> The Devil Schemes among the beggars and thieves in the Hierophant's domain.</h2>
                    Add %s Scheme cards from the Devil's Deck to this Community.
                    """ % cards_by_house[3]
        if cards_by_house[4] != 0:
            leo = f"""
                    <h2> The Devil Schemes among the lords and ladies of the Noble Clans in the Warlock's domain.</h2>
                    Add %s Scheme cards from the Devil's Deck to this Community.
                    """ % cards_by_house[4]
        if cards_by_house[5] != 0:
            virgo = f"""
                    <h2> The Devil Schemes among the soldiers and servants of the Halcyon Isles in the Warlock's domain.</h2>
                    Add %s Scheme cards from the Devil's Deck to this Community.
                    """ % cards_by_house[5]
        if cards_by_house[6] != 0:
            libra = f"""
                    <h2> The Devil Schemes among the fishermen and divers of the Reaches in the Mariner's domain.</h2>
                    Add %s Scheme cards from the Devil's Deck to this Community.
                    """ % cards_by_house[6]
        if cards_by_house[7] != 0:
            scorpio = f"""
                    <h2> The Devil Schemes among the sailors and travellers of Foreign Lands in the Mariner's domain.</h2>
                    Add %s Scheme cards from the Devil's Deck to this Community.
                    """ % cards_by_house[7]
        if cards_by_house[8] != 0:
            sagittarius = f"""
                    <h2> The Devil Schemes among the scholars and researchers of Spyrholm University in the Sorcerer's domain.</h2>
                    Add %s Scheme cards from the Devil's Deck to this Community.
                    """ % cards_by_house[8]
        if cards_by_house[9] != 0:
            capricorn = f"""
                    <h2> The Devil Schemes among the dead and nearly-dead of the Graven Isle in the Necromancer's domain.</h2>
                    Add %s Scheme cards from the Devil's Deck to this Community.
                    """ % cards_by_house[9]
        if cards_by_house[10] != 0:
            aquarius = f"""
                    <h2> The Devil Schemes among the druids and hermits of the Moonlit Atoll in the Sage's domain.</h2>
                    Add %s Scheme cards from the Devil's Deck to this Community.
                    """ % cards_by_house[10]
        if cards_by_house[11] != 0:
            pisces = f"""
                    <h2> The Devil Schemes among the dreamers, the wanderers, and all those without a home in the Sage's domain.</h2>
                    Add %s Scheme cards from the Devil's Deck to this Community.
                    """ % cards_by_house[11]
        if sum(cards_by_house) == 0:
            none = f"""
                    <h2>The Devil seeks the affection of another wizard.</h2>
                    The wizard receives an invitation to schedule Time and have a scene with the Devil, in which the Devil will make him a Bargain. If the wizard refuses to schedule Time with the Devil, the Devil places a Scheme onto each of that wizard's Communities.
            """
        self.set_date_string()
        self.read_the_stars_html = f"""
                    <div style="font-family: serif;">
                      <h1 class="break-page"> Chain-Watcher who is concerened with the movements of %s </h1>
                      <h2> First, shuffle the Devil's Deck</h2>
                      {aires}
                      {taurus}
                      {gemini}
                      {cancer}
                      {leo}
                      {virgo}
                      {libra}
                      {scorpio}
                      {sagittarius}
                      {capricorn}
                      {aquarius}
                      {pisces}
                      {none}
                      <br><br><br>
                          <center><h3> Report produced for {self.date_string}</h3> </center>
                    </div>
                """ % lib.MERCURY
        return