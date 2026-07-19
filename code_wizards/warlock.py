# coding=utf-8
from code_wizards.wizard import Wizard
from code_plumbing import lib
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

        layout = QVBoxLayout(warlock_pop)
        self.read_the_stars()
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

    def read_the_stars(self):
        test_king = {'name': 'john', 'sun': 'Aries', 'moon': 'Aries', 'rising': 'Aries', 'aristocracy': 6, 'mercantilism': 6, 'orthodoxy': 6, 'piracy': 6, 'rebellion': 6, 'ergoism': 6, 'monarchy': 6}
        king = test_king
        #king = self.king for later

        mercury = ""

        # MERCURY
        if (self.determine_if_in_sign(self.planets[0], king['sun']) or self.determine_if_in_sign(self.planets[0], king['moon']) or self.determine_if_in_sign(self.planets[0], king['rising'])):
            mercury += f"""
                        <h2> Mercury is aligned with any sign, the King struggles to maintain power.  </h2>
                        Move one Authority from the King to any Ideology with the lowest Authority.
                        """
        # VENUS
        venus = ""
        if (self.determine_if_in_sign(self.planets[1], king['sun']) or self.determine_if_in_sign(self.planets[1],king[ 'moon']) or self.determine_if_in_sign(self.planets[1], king['rising'])):
            venus += f"""
                            <h2> Venus is aligned with any sign, power leeches from the King's grasp.</h2>
                            Move one Authority from the King to any Ideology with the highest Authority.
                            """
        # MARS
        mars = ""
        if (self.determine_if_in_sign(self.planets[2], king['sun']) or self.determine_if_in_sign(self.planets[2], king['moon']) or self.determine_if_in_sign(self.planets[2], king['rising'])):
            mars += f"""<h2> Mars is aligned with any sign, the King turns to outside advice to guide his hand. </h2>
            Draw a random Lord from any Clan who didn't otherwise contribute to the Agenda this month.
                """
            if king.aristocracy >= 6:
                mars += f""" <h3>Aristocracy has at least 6 Authority, the Clans with the most and least Favor Duel.</h3>
                    Flip over the top Lord or each Clan and determine who, in your opinion, would win. The winner takes all Favor and Authority from the losing Clan. The loser dies.
                """
            if king.mercantilism >= 6:
                mars += f""" <h3>Mercantilism has at least 6 Authority, new Markets open across Isha.</h3>
                    Take a Market from the Mariner's Domain and a Garrison and place it in any wizard's Domain. At the start of each month, give the associated wizard a minor Gift and move 1 Authority from the King to this Market.
                """
            if king.orthodoxy >= 6:
                mars += f""" <h3>Orthodoxy has at least 6 Authority, the Clans must prove their devotion to Isha.</h3>
                    Each other Clan (the Orthodoxy becomes a new Clan) must spend 1 Conviction or demonstrate penance, moving a Lord from their Clan into the Orthodoxy and gaining 2 Conviction.
                """
            if king.piracy >= 6:
                mars += f""" <h3>Piracy has at least 6 Authority, Lords turn to crime.</h3>
                    Flip over a Lord from each Clan. These Lords are involved in criminal conspiracies. If that Lord's associated Ideology has at least 1 Authority, the Lord profits from his criminal endeavors and that Clan gains 1 Favor. If that Lord's associated Ideology has 0 Authority, the Lord dies.
                """
            if king.rebellion >= 6:
                mars += f""" <h3>Rebellion has at least 6 Authority, the Rebellion sets its own Agenda.</h3>
                    Flip over all Lords in Rebellion and enact their Agendas <i>immediately.</i> Then move 1 Authority from the King to the Rebellion.
                """
            if king.ergoism >= 6:
                mars += f""" <h3>Ergoism has at least 6 Authority, the King works in concert with his servants to cast a spell of <u>Mighty Import</u> at any point during the month.</h3>
                    He rolls a number of dice equal to the total Authority on Ergoism.
                """
            if king.monarchy >= 6:
                mars += f""" <h3>Monarchy has at least 6 Authority, the true King decisively strikes against those who oppose his rule.</h3>
                    The King Garrisons any other Domain. Each Garrison counts towards the Monarchy's Authority for the purposes of determining who Truly Wields Power.
                """

        #JUPITER
        jupiter = ""
        if self.determine_if_in_sign(self.planets[3], king['sun']):
            jupiter += f"""<h2> Jupiter is in conjunction with the King's Sun Sign, one of the King's lovers gives birth to a son.</h2>
            Choose a Lady. During the Royal Ball this season, if that Lady is still alive, place a <i>Bastard Son of the King</i> Title in that Confidant's associated Clan. <i>(If this conjunction has occurred multiple times this season, its associated event only happens once.)</i>
            """
        if self.determine_if_in_sign(self.planets[3], king['moon']):
            jupiter += f"""<h2> Jupiter is in conjunction with the King's Moon Sign, one of the King's lovers gives birth to a daughter.</h2>
            Choose a Lady. During the Royal Ball this season, if that Lady is still alive, add a Lady from that Clan to the King's Family. <i>(If this conjunction has occurred multiple times this season, its associated event only happens once.)</i>
            """
        if self.determine_if_in_sign(self.planets[3], king['rising']):
            jupiter += f"""<h2> Jupiter is in conjunction with the King's Rising Sign, the King offers the hand of one of his daughters in marriage to another.</h2>
            Choose a Lady. During the Royal Ball this season, if that Lady is still alive, add a Lady from that Clan to the King's Family. <i>(If this conjunction has occurred multiple times this season, its associated event only happens once.)</i>
            """

        #SATURN
        saturn = ""
        if self.determine_if_in_sign(self.planets[4], king['sun']):
            saturn += f"""<h2> Saturn is in conjunction with the King's Sun Sign, the loves of the King grow weak.</h2>
            Roll two D10s \u2014 one for the King's Family and one for his Confidants. For each "{lib.SATURN}" (<i>Saturn</i>) rolled, a Lady of your choice from that group dies.
            """
        if self.determine_if_in_sign(self.planets[4], king['moon']):
            saturn += f"""<h2> Saturn is in conjunction with the King's Moon Sign, the Lords of Isha take stock of their health.</h2>
                        For each Clan, roll a D10. For each "{lib.SATURN}" (<i>Saturn</i>) rolled, kill a random Lord from that Clan.
                        """
        if self.determine_if_in_sign(self.planets[4], king['rising']):
            saturn += f"""<h2> Saturn is in conjunction with the King's Rising Sign, the King of Isha's health is threatened.</h2>
                        Roll a D12. If "{lib.SATURN}" (<i>Saturn</i>) is rolled, the King grows deathly ill. Unless someone can aid him, through magic or medical care, he will die at the end of the month.
                        """
        #SOL
        sol = ""
        if self.determine_if_in_sign(self.planets[5], king['sun']):
            sol += f"""<h2> Sol is in conjunction with the King's Sun Sign, it's the King's birthday</h2>
            Each wizard may schedule Time on the King this month to attend a collective scene celebrating the King's birthday, during which they must follow the Laws of the Court and present the King with a present that pleases him. Give each wizard who fails to do this a Complication.
            """
        if self.determine_if_in_sign(self.planets[5], king['moon']):
            sol += f"""<h2> Sol is in conjunction with the King's Moon Sign, the King passes a new Law reflecting the positive qualities of how he wants people to perceive him.</h2>
                        Choose any Law and inform the Celestial Audience and ask them if they plan to follow it. If they do, move an Authority from any Ideology to the King. If they don't move two Authority from the King to any two Ideologies that most fervently oppose the Law.
                        """
        if self.determine_if_in_sign(self.planets[5], king['rising']):
            sol += f"""<h2> Sol is in conjunction with the King's Rising Sign, the King passes a new Law reflecting the negative qualities of how people perceive him.</h2>
                        Choose any Law and inform the Celestial Audience and ask them if they plan to follow it. If they do, move an Authority from any Ideology to the King. If they don't, move two Authority from the King to any two Ideologies that most fervently oppose the Law.  
                        """
        self.set_date_string()
        self.read_the_stars_html = f"""
            <div style="font-family: serif;">
                      <h1 class="break-page"> Keeper of the Flames whose fate is controlled by %s </h1> 
                      {mercury}
                      {venus}
                      {mars}
                      {jupiter}
                      {saturn}
                      {sol}
                      <br><br><br>
                          <center><h3> Report produced for {self.date_string}</h3> </center>
                    </div>
            """
        return