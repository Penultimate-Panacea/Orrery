# coding=utf-8
from code_wizards.wizard import Wizard
from code_plumbing import lib
from PyQt6.QtGui import QTextDocument
from PyQt6.QtWidgets import QTextEdit, QDialog, QVBoxLayout
from collections import Counter

class Sage(Wizard):
    def __init__(self,planetary_conjunction_dict, planet_list, dreaming):
        super().__init__(planetary_conjunction_dict)
        self.planets = planet_list
        self.dreaming = dreaming
        self.alignments = [0,0,0,0,0,0,0,0,0,0,0,0]

    def set_dreaming(self, new_dreaming):
        self.dreaming = new_dreaming

    def popup(self):
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
        houses = lib.SIGNS
        all_conjunction_tables = []
        for p in self.planets:
            all_conjunction_tables.append(p.conjunction_table[p.current_step])
        all_houses = [x for lst in all_conjunction_tables for x in lst]
        counts = Counter(all_houses)
        celestial_alignment = max(counts.values(), default=0)



        result = ""

        if self.dreaming == "Calm":
            if celestial_alignment == 1:
                result = f"""<h2>The Dreaming is Calm and the Celestial Alignment is 1.</h2>
                            A cataclysmic Omen appears — perhaps a falling star, monstrous dragon, or approaching fleet. The Dreamscape immediately becomes Chaotic.
                        """
            elif celestial_alignment == 2:
                result = f"""<h2>The Dreaming is Calm and the Celestial Alignment is 2.</h2>
                                Choose two Denizens who struggle against one another, give them each an Omen, and present them to the Celestial Audience. They enter a contest of wills, words, swords, or law. Ask the Celestial Audience who triumphs. If the Celestial Audience confidently and unanimously chooses one victor over another, give any wizard a Gift. If the Celestial Audience disagrees or debates, instead there is no clear winner, and remove an Omen from the Pact.
                            """
            elif celestial_alignment == 3:
                result = f"""<h2>The Dreaming is Calm and the Celestial Alignment is 3.</h2>
                                Choose or create a Denizen with advice for the Pact. Give them an Omen and present them to any wizard. That wizard may schedule Time on them to hear their issues. He spends that Time to have a short scene with them. If the wizard has this scene, place an Omen on him. If the wizard refuses, remove an Omen from the Pact.
                            """
            elif celestial_alignment >= 4:
                 result = f"""<h2>The Dreaming is Calm and the Celestial Alignment is 4 or more.</h2>
                                A newcomer arrives to Isha with strange tidings. Create a Denizen from a distant land and give them a Destiny. They are the embodiment of this destiny in all ways, and consciously seek to model it. Create a major Complication for another wizard related to their arrival. The Dreaming becomes Uncertain.
                            """
        elif self.dreaming == "Uncertain":
            if celestial_alignment == 1:
                result = f"""<h2>The Dreaming is Uncertain and the Celestial Alignment is 1.</h2>
                            The Dreaming settles into peace. Place an Omen on any Denizen who exemplifies calmness and reflection. The Dreaming becomes Calm.
                        """
            elif celestial_alignment == 2:
                result = f"""<h2>The Dreaming is Uncertain and the Celestial Alignment is 2.</h2>
                            Choose two Denizens who suffer a deep and violent betrayal. Give them each an Omen and present them to the Celestial Audience, asking which one betrayed the other. If the Celestial Audience confidently and unanimously chooses one victor over another, place a second Omen on the traitor and the betrayed manages to survive. If the Celestial Audience disagrees or debates, instead they destroy each other, and give a minor Complication to any wizard as a result.
                        """
            elif celestial_alignment == 3:
                result = f"""<h2>The Dreaming is Uncertain and the Celestial Alignment is 3.</h2>
                            Choose or create a Denizen who needs the Pact's help. Give them an Omen and present them to any wizard. That wizard may schedule Time on them to hear their issues. He spends that Time to have a short scene with them. If the wizard refuses to help them, give him a Complication.
                        """
            elif celestial_alignment >= 4:
                result = f"""<h2>The Dreaming is Uncertain and the Celestial Alignment is 4 or more.</h2>
                            A powerful Denizen arrives to Isha with dark intentions. Create a Denizen from a distant land with a random King or Beast Destiny. They are the embodiment of this destiny in all ways, and consciously seek to model it. Create a major Complication for another wizard related to their arrival. The Dreaming becomes Chaotic.
                        """
        elif self.dreaming == "Chaotic":
            if celestial_alignment == 1:
                result = f"""<h2>The Dreaming is Chaotic and the Celestial Alignment is 1.</h2>
                            An ancient bylaw crumbles and a forgotten power betrays the Pact. Create a major Complication for each other wizard.
                        """
            elif celestial_alignment == 2:
                result = f"""<h2>The Dreaming is Chaotic and the Celestial Alignment is 2</h2>
                            Choose two Denizens who are both placed in a tragic set of circumstances. Give them both an Ome, describe the circumstances. Give them both an Omen, describe the circumstances and present them to the Celestial Audience, asking who manages to live. If the Celestial Audience confidently and unanimously chooses one survivor over the other, the one who lives gains all the Omens of the one who died. If the Celestial Audience disagrees or debates, they both die. Create a minor Complication for each other wizard.
                        """
            elif celestial_alignment == 3:
                result = f"""<h2>The Dreaming is Chaotic and the Celestial Alignment is 3.</h2>
                            Choose or create a Denizen who threatens the Pact. Give them an Omen and present them to any wizard. That wizard may schedule Time on them to parlay with them. He spends that Time to have a short scene with them. If the wizard does not take their threat seriously, give him a major Complication.
                        """
            elif celestial_alignment >= 4:
                result = f"""<h2>The Dreaming is Chaotic and the Celestial Alignment is 4 or more.</h2>
                            A kind soul arrives to Isha with desires to help the Pact. Create a Denizen from a distant land with a random Page or Knight Destiny. They are the embodiment of this destiny in all ways, and consciously seek to model it. If they die by the end of the month in pursuit of their Destiny, the Dreaming becomes Calm.
                        """
        elif self.dreaming == "Bleak":
            if celestial_alignment == 1:
                result = f"""<h2>The Future of the Pact is Bleak and the Celestial Alignment is 1.</h2>
                            Magic grows rarer and harder to cast. Choose the spell in <i>The Grimoire</i> which you believe has been cast most frequently. It cannot be cast as long as the Dreaming is Bleak.
                        """
            elif celestial_alignment == 2:
                result = f"""<h2>The Future of the Pact is Bleak and the Celestial Alignment is 2.</h2>
                            The Pact's magic starts to fail them. Choose a Treasure which you believe has been especially vital for the Pact's endurance up to this point. It has been stolen and cannot be recovered as long as the Dreaming is Bleak.
                        """
            elif celestial_alignment == 3:
                result = f"""<h2>The Future of the Pact is Bleak and the Celestial Alignment is 3.</h2>
                            A former ally of the Pact now struggles against the darkness. Give them an Omen and present them to any wizard. That wizard may schedule Time on them to meet with them. He spends that Time to have a short scene with them. If the wizard doesn't, give every other wizard a Complication, and that ally will never trust the Pact again.
                        """
            elif celestial_alignment >= 4:
                result = f"""<h2>The Future of the Pact is Bleak and the Celestial is 4 or more.</h2>
                            The world violently changes the future turns away from the Pact. Create a Gamechanging Impact for any wizard.
                            """

        self.set_date_string()
        self.read_the_stars_html = f"""
                        <div style="font-family: serif;">
                          <h1 class="break-page"> Keeper of the Stars whose fate is controlled by the %s Estate</h1>
                            {result}
                          <br><br><br>
                          <center><h3> Report produced for {self.date_string}</h3> </center>
                        </div>
                    """ % self.dreaming