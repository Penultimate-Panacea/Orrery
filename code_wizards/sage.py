# coding=utf-8
from code_wizards.wizard import Wizard
from code_plumbing import lib
from PyQt6.QtGui import QTextDocument
from PyQt6.QtWidgets import QTextEdit, QDialog, QVBoxLayout
class Sage(Wizard):
    def __init__(self,planetary_conjunction_dict, planet_list, estate):
        super().__init__(planetary_conjunction_dict)
        self.planets = planet_list
        self.estate = estate

    def set_estate(self, new_estate):
        self.estate = new_estate

    def generate_planets_in_estate(self):
        in_estate_names = []
        for p in self.planets:
            if self.determine_if_in_estate(p):
                in_estate_names.append(p.name)
        print("The following planets are in estate: %s" % in_estate_names)
        return in_estate_names

    def determine_if_in_estate(self, planet):
        estate = self.estate
        estate_houses = []
        print("Estate is is: %s" % estate)
        if estate == "Terrestrial":
            estate_houses = [0,1,2,3]
        if estate == "Spiritual":
            estate_houses = [4,5,6,7]
        if estate == "Cosmic":
            estate_houses = [8,9,10,11]
        print("Houses in Estate: %s" % estate_houses)
        print("Conjunction Table: %s" % planet.conjunction_table)
        if any(p in planet.conjunction_table[planet.current_step] for p in estate_houses):
            return True
        else:
            return False

    def sage_popup(self):
        sage_pop = QDialog()
        sage_pop.setWindowTitle("Sage")

        layout = QVBoxLayout(sage_pop)

        self.read_the_stars()

        sage_document = QTextDocument()
        sage_document.setHtml(self.read_the_stars_html)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setDocument(sage_document)

        layout.addWidget(text)

        sage_pop.resize(900,600)
        sage_pop.exec()

    def read_the_stars(self):
        planets_in_estate = self.generate_planets_in_estate()
        print("self.estate is %s" % self.estate)
        print("planets_in_estate %s" % planets_in_estate)
        none_in_estate = ""
        mercury = ""
        venus = ""
        mars = ""
        jupiter_xor_saturn = ""
        jupiter_and_saturn = ""

        if self.estate == "Terrestrial":
            if lib.MERCURY in planets_in_estate:
                mercury = """
                            <h3> Mercury is in the First Estate, the dreaming world is dominated by the petty cruelty of mortal men </h3>
                            Choose two Sleepers, Mark them, and present them before the Celestial Audience. They enter a contest of wills, words, swords, or law. Ask the Celestial Audience who triumphs. If the Celestial Audience confidently and unanimously chooses one victor over another, give an associated Wizard a Gift. If the Celestial Audience disagrees or debates, instead there is no clear winner, and give an associated Wizard a Complication as a result.
                        """
            if lib.VENUS in planets_in_estate:
                venus = """
                            <h3> Venus is in the First Estate, a  Sleeper goes to a Wizard seeking his assistance, advice, or companionship.</h3>
                            ark that Sleeper. If the Wizard will Spend Time with them this month, give him a Gift as a result, and that Sleeper will attempt to achieve one of their Star Sign’s Goals. If the Wizard refuses, give him a Complication.
                        """
            if lib.MARS in planets_in_estate:
                mars = """
                            <h3> Mars in in the First Estate, a Sleeper is influenced by the Paradigms of the Cosmic Estate.</h3>
                            Choose a Paradigm’s Plot, and either invent or choose a Sleeper who would be a good fit. Describe a vision to the Celestial Audience of that Character setting off that Plot, Mark them, and ask an associated Keepers any appropriate questions about the vision. Give one Wizard a Gift and another a Complication as a result.
                        """
            if (lib.JUPITER in planets_in_estate) ^ (lib.SATURN in planets_in_estate):
                jupiter_xor_saturn = """
                            <h3> Jupiter or Saturn is in the First Estate, magic slowly drains from the world. </h3>
                            Choose one piece of Lore in any Codex (perhaps a Wizard’s Isle or Sanctum) and Change it to be less magical, more modern, or more unremarkable.
                        """
            if (lib.JUPITER in planets_in_estate) and (lib.SATURN in planets_in_estate):
                jupiter_and_saturn = """
                            <h3> Jupiter and Saturn are in the First Estate, magic slowly drains from the world. </h3>
                            I.  Choose one piece of Lore in any Codex (perhaps a Wizard’s Isle or Sanctum) and Change it to be less magical, more modern, or more unremarkable. <br>
                            II. <b>Move towards Extinction.</b>
                        """
            if len(planets_in_estate) == 0:
                none_in_estate = """
                            <h3> The First Estate is empty of planets, the dreaming world is struck by tragedy</h3>
                            I. Choose any Sleeper and ask the Gate-Keeper how they suddenly and unfairly died. Give an associated Wizard a Complication as a result. If any member of the Pact wishes for this Sleeper not to die, they must take a major Complication to subconsciously save their life.<br>
                            II. <b>Move towards Extinction.</b>
                        """

        elif self.estate == "Spiritual":
            if lib.MERCURY in planets_in_estate:
                mercury = """
                            <h3> Mercury is present in the Second Estate, a Luminary takes action and shapes the world around them.</h3>
                            Choose any other Luminary and, if they’re not a Wizard, ask a Keeper to speak for them. Present them with a simple situation in which one of the options involves completing a Quest (without revealing that Quest to them). If they choose the path with the Quest, give the associated Wizard a Complication. If they make a different choice, give the associated Wizard a Gift.
                        """
            if lib.VENUS in planets_in_estate:
                venus = """
                            <h3> Venus is present in the Second Estate, a Luminary makes a new friend. </h3>
                             Choose any other Luminary and create a new Sleeper who is urging the Luminary towards their Destiny. If the Luminary is a Wizard, the Sleeper will request their audience. If the Wizard Spends Time with them this month, give him a Gift, and during that scene, attempt to nudge the Wizard towards a Destiny. If the Wizard refuses, give him a Complication associated with that Sleeper.
                        """
            if lib.MARS in planets_in_estate:
                mars = """
                            <h3> Mars is present in the Second Estate, a Luminary is called to action. </h3>
                            Choose any one Luminary tied for fewest Quests completed. This month, they <i>must</i> complete at least one Quest. If they do, give an associated Wizard a Gift. If they fail to do so, give an associated Wizard a Complication. Replace their Destiny with a random different Destiny.
                        """
            if (lib.JUPITER in planets_in_estate) ^ (lib.SATURN in planets_in_estate):
                jupiter_xor_saturn = """
                            <h3> Jupiter or Saturn is present in the Second Estate, the world responds to the power of the Pact.</h3>
                             Choose one piece of Lore from any Codex (perhaps a Wizard’s Isle or Sanctum) and Change it to reflect that Wizard’s behavior, the changing of the seasons, or the events of the narrative as it unfolds.
                        """
            if (lib.JUPITER in planets_in_estate) and (lib.SATURN in planets_in_estate):
                jupiter_and_saturn = """
                            <h3> Jupiter and Saturn are present in the Second Estate, the world responds to the power of the Pact.</h3>
                             I.     Choose one piece of Lore from any Codex (perhaps a Wizard’s Isle or Sanctum) and Change it to reflect that Wizard’s behavior, the changing of the seasons, or the events of the narrative as it unfolds.<br>
                             II.    Give the associated Wizard a Complication.
                        """
            if len(planets_in_estate) == 0:
                none_in_estate = """
                            <h3> The Second Estate is empty of planets, a new Luminary arrives</h3>
                            Choose a random Destiny and create a new character based on that Destiny. They arrive at the Wizardmoot this month carrying ill news, demands for change, or long-forgotten grudges. If they die, give each other Wizard a major Complication.
                        """

        elif self.estate == "Cosmic":
            if lib.MERCURY in planets_in_estate:
                mercury = """
                            <h3> Mercury is present within the Third Estate, the Pact is shaped by the winds of fate.</h3>
                            Choose a Paradigm and give a different associated Wizard a minor Complication for each Unresolved Plot.
                        """
            if lib.VENUS in planets_in_estate:
                venus = """
                            <h3> Venus is present within the Third Estate, an agent of a Paradigm makes its will known to a member of the Pact.</h3>
                            Choose or create a Sleeper, Mark them, and have them send a request for a meeting to a Wizard. If the Wizard Spends Time with them this month, give him a Gift, and attempt to Set Up one of that Paradigm’s Plots. If the Wizard refuses, give him a Complication associated with the Paradigm.
                        """
            if lib.MARS in planets_in_estate:
                mars = """
                            <h3> Mars is present within the Third Estate, a Paradigm moves openly against the Pact.</h3>
                            Create a new Luminary to serve as the face of the Paradigm and place them within another Domain. Now, and at the start of each month the Luminary remains present in that Domain, give that Domain’s Wizard a Gift associated with the Luminary, and ask that Domain’s Keeper to give another Wizard a Complication. 
                        """
            if (lib.JUPITER in planets_in_estate) ^ (lib.SATURN in planets_in_estate):
                jupiter_xor_saturn = """
                            <h3> Jupiter or Saturn is within the Third Estate, the world spins towards madness.</h3>
                            Choose one piece of Lore in any Codex (perhaps a Wizard’s Sanctum or Isle) and Change it to be more magical, more fantastical, or more dangerous.
                        """
            if (lib.JUPITER in planets_in_estate) and (lib.SATURN in planets_in_estate):
                jupiter_and_saturn = """
                            <h3 Jupiter and Saturn are within the Third Estate, the world spins towards madness.</h3>
                            I. Choose one piece of Lore in any Codex (perhaps a Wizard’s Sanctum or Isle) and Change it to be more magical, more fantastical, or more dangerous.<br>
                            II. <b>Move towards Calamity</b>
                        """
            if len(planets_in_estate) == 0:
                none_in_estate = """
                            <h3> The Third Estate is empty of planets.</h3>
                            I. Add a new Paradigm of your choice and give a Complication to each other Wizard as the dreaming world quakes in fear of its arrival.<br>
                            II. <b>Move towards Extinction.</b>
                        """
        self.set_date_string()
        self.read_the_stars_html = f"""
                        <div style="font-family: serif;">
                          <h1 class="break-page"> Keeper of the Stars whose fate is controlled by the %s Estate</h1>
                          {mercury}
                          {venus}
                          {mars}
                          {jupiter_xor_saturn}
                          {jupiter_and_saturn}
                          {none_in_estate}
                          <br><br><br>
                          <center><h3> Report produced for {self.date_string}</h3> </center>
                        </div>
                    """ % self.estate