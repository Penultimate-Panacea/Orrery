# coding=utf-8
from wizard import Wizard
from dataclasses import dataclass
import lib
from PyQt6.QtGui import QTextDocument
from PyQt6.QtWidgets import QTextEdit, QDialog, QVBoxLayout
test_king = [{'name':"Joe",'sun': 'Taurus','moon':'Gemini','rising':'Aries'}]

class Warlock(Wizard):
    def __init__(self,planetary_conjunction_dict, planets, kings):
        super().__init__(planetary_conjunction_dict)
        self.planets = planets
        self.kings = kings

    def warlock_popup(self):
        warlock_pop = QDialog()
        warlock_pop.setWindowTitle("Warlock")

        # test_king = [{'name': "Joe", 'sun': 'Taurus', 'moon': 'Gemini', 'rising': 'Aries'}]

        layout = QVBoxLayout(warlock_pop)
        master_king_text = ""
        if not len(self.kings) == 0:
            print("HERE BE KINGS")
            for king in self.kings:
                print(self.king_string(king))
                master_king_text+=self.king_string(king)
                print(master_king_text)
        else:
            print("NO KINGS")

        self.read_the_stars_html = f""""
            <h1> Keeper of the Throne whose fate is controlled by the signs that the King was born under.</h1>
                      {master_king_text}
                      <h2> After processing all Courts as above:</h2>
                      Starting with the King's Guide and proceeding counterlockwise around the Court (<i>in order:</i> Guide, Love, Friend, and then Heir), resolve the Agenda of each Noble with a unique Allegiance in the King's Inner Circle. If a Noble's Agenda would occur, and the King has already put in motion the Agenda of another Noble of the same Allegiance, the King instead ignores the Noble's demands.
                    </div>
        """

        warlock_document = QTextDocument()
        warlock_document.setHtml(self.read_the_stars_html)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setDocument(warlock_document)

        layout.addWidget(text)

        warlock_pop.resize(900,600)
        warlock_pop.exec()

    def king_string(self, king):


        sun_string = ""
        if self.determine_if_in_sign(self.planets[0],king['sun']):
            sun_string += """
                <h3>Sun Sign contains Mercury</h3>
                Secure all Nobles of Ascendant Allegiance.
            """
        if self.determine_if_in_sign(self.planets[1],king['sun']):
            sun_string += """
                <h3>Sun Sign contains Venus</h3>
                Add a <i>Knight</i> from the Ascendant Allegiance to the Court.
            """
        if self.determine_if_in_sign(self.planets[2],king['sun']):
            sun_string += """
                <h3>Sun Sign contains Mars -- Insecurity and distrust ravage the court</h3>
               A rival faction within the Populous Allegiance reveals itself. Choose half of all Nobles within that Allegiance and create a new Allegiance from them.
            """
        if self.determine_if_in_sign(self.planets[3],king['sun']):
            sun_string += """
                <h3>Sun Sign contains Jupiter -- A royal pregnancy is discovered</h3>
                Ask the Celestial Audience who the mother is. Six months (two trimesters) from now, the child will be born and enter the Court as a Prince or Princess, unless their mother dies.
            """
        if self.determine_if_in_sign(self.planets[4],king['sun']):
            sun_string += """
                <h3>Sun Sign contains Saturn</h3>
                Roll an Arcane Import die for each non-Secure, non-Prince, male Noble. For each \"\U0001F714\", Dispose of that Noble.
            """
        if self.determine_if_in_sign(self.planets[5],king['sun']):
            sun_string += """
                <h3>Sun Sign contains Sun -- It is the King's birthday.</h3>
                All Wizards must Spend Time to attend and have a collective Scene, during which each Wizard must follow the rules of Court and give him a birthday present. Any errant Wizards receive a Complication.
            """
        moon_string = ""
        if self.determine_if_in_sign(self.planets[0],king['moon']):
            moon_string += """
                <h3>Moon Sign contains Mercury</h3>
                Secure all Nobles of Populous Allegiance.
            """
        if self.determine_if_in_sign(self.planets[1],king['moon']):
            moon_string += """
                <h3>Moon Sign contains Venus</h3>
                Add a <i>Lady</i> from the Frail Allegiance to the Court.
            """
        if self.determine_if_in_sign(self.planets[2],king['moon']):
            moon_string += """
                <h3>Moon Sign contains Mars</h3>
               Choose the most common Authority. All Nobles of that Authority become members of a new Allegiance, a secret society they swear themselves to.
            """
        if self.determine_if_in_sign(self.planets[3],king['moon']):
            moon_string += """
                <h3>Sun Sign contains Jupiter -- An attempt is made on the King's life.</h3>
                I. Flip a coin. <br>
                II. On heads, the King dies. Ask the Gate-Keeper who assassinated him.
            """



        rising_string = ""
        if self.determine_if_in_sign(self.planets[0],king['rising']):
            rising_string += """
                <h3>Rising Sign contains Mercury</h3>
                Secure all Nobles of Frail Allegiances.
            """
        if self.determine_if_in_sign(self.planets[1],king['rising']):
            rising_string += """
                <h3>Rising Sign contains Venus</h3>
                Add a <i>Bard</i> or <i>Mistress</i> from a new, previously unrepresented, Allegiance to the Court.
            """
        if self.determine_if_in_sign(self.planets[2],king['rising']):
            rising_string += """
                <h3>Rising Sign contains Mars</h3>
               Choose another Domain. A powerful force from that region (perhaps even the Wizard himself) has taken an interest in politics. Add a new <i>Advisor</i> with Allegiance to a force from that Domain to the Court.
            """

        unrepresented_string = ""
        if (not self.determine_if_in_sign(self.planets[0],king['sun'])) and (not self.determine_if_in_sign(self.planets[0],king['moon'])) and (not self.determine_if_in_sign(self.planets[0],king['rising'])):
            unrepresented_string += """ 
            <h3> Mercury is not aligned with any sign </h3>
                All Nobles with an unrevealed Secret are reduced in Standing.
            """
        if (not self.determine_if_in_sign(self.planets[1],king['sun'])) and (not self.determine_if_in_sign(self.planets[1],king['moon'])) and (not self.determine_if_in_sign(self.planets[1],king['rising'])):
            unrepresented_string.join(""" 
            <h3> Venus is not aligned with any sign </h3>
                A Noble of your choice from any non-Frail Allegiance returns home and peacefully departs. Remove them from the Court.
            """)


        king_string = f"""
        <h1> The Court of King %s </h1>
        {sun_string}
        {moon_string}
        {rising_string}
        {unrepresented_string}
        """ % king['name']
        return king_string

    def determine_if_in_sign(self, planet, sign):
        print("Sign is: %s" % sign)
        house = lib.SIGNS.index(sign)
        print("Conjunction Table: %s" % planet.conjunction_table)
        if house in planet.conjunction_table[planet.current_step]:
            return True
        else:
            return False