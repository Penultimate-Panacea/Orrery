# coding=utf-8
from wizard import Wizard
import lib
from PyQt6.QtGui import QTextDocument
from PyQt6.QtWidgets import QTextEdit, QDialog, QVBoxLayout


def house_scheme_cards(array, target):
    # START SHAMEFUL AI GENERATED FUNCTION REPLACE AT ONCE
    # Normalize into (label, list) pairs
    pairs = []
    i = 0
    while i < len(array):
        if isinstance(array[i], str):
            label = array[i]
            values = array[i + 1]
            pairs.append((label, values))
            i += 2
        else:
            # handles cases like ['A', [1,2,3]]
            if isinstance(array[i], (list, tuple)) and len(array[i]) == 2:
                label, values = array[i]
                pairs.append((label, values))
            i += 1
    # END SHAMEFUL AI GENERATED FUNCTION
    out = {}
    for label, values in pairs:
        values = list(values)
        cnt_target = values.count(target)
        if cnt_target:
            out[label] = (len(values) - cnt_target) * 2  # exclude the target elements themselves and place two cards

    return out

class Faustian(Wizard):
    def __init__(self,planetary_conjunction_dict, house_planet_conjunctions):
        super().__init__(planetary_conjunction_dict)
        self.house_planet_conjunctions = house_planet_conjunctions

    def generate_faust_factor(self):
        conjunctions = self.planet_conjunction_dict
        print("Conjunctions are: " + str(conjunctions))
        mercury_conjunctions = conjunctions[lib.MERCURY]
        faust_factor = len(mercury_conjunctions)
        return
    
    def faustian_popup(self):
        faust_pop = QDialog()
        faust_pop.setWindowTitle("Faustian Reads the Stars")
        magic_number = self.generate_faust_factor()
        locations_with_cards = house_scheme_cards(self.house_planet_conjunctions, '☿')
        if 'Aries' in locations_with_cards:
            locations_with_cards["The monks and pilgrims of the Temples <i> (Aries, Hierophant) </i>"] = locations_with_cards.pop('Aries')
        if 'Taurus' in locations_with_cards:
            locations_with_cards["The merchants and bankers of the Blue City <i> (Taurus, Hierophant) </i>"] = locations_with_cards.pop('Taurus')
        if 'Gemini' in locations_with_cards:
            locations_with_cards["The farmers and shepherds of the Chalk Cliffs <i> (Gemini, Hierophant) </i>"] = locations_with_cards.pop('Gemini')
        if 'Cancer' in locations_with_cards:
            locations_with_cards["The beggars and thieves of Scuttleport <i> (Cancer, Hierophant) </i>"] = locations_with_cards.pop('Cancer')
        if 'Leo' in locations_with_cards:
            locations_with_cards["The lords and ladies of the Noble Clans <i> (Leo, Warlock) </i>"] = locations_with_cards.pop('Leo')
        if 'Virgo' in locations_with_cards:
            locations_with_cards["The soldiers and servants of the Halcyon Isles <i> Virgo, Warlock </i>"] = locations_with_cards.pop('Virgo')
        if 'Libra' in locations_with_cards:
            locations_with_cards["The fishermen and divers of the Far Reach <i> Libra, Mariner </i>"] = locations_with_cards.pop('Libra')
        if 'Scorpio' in locations_with_cards:
            locations_with_cards["The sailors and travelers beyond Isha <i> Scorpio, Mariner </i>"] = locations_with_cards.pop('Scorpio')
        if 'Sagittarius' in locations_with_cards:
            locations_with_cards["The students and professors of Spyrholm University <i> Sagittarius, Sorcerer </i>"] = locations_with_cards.pop('Sagittarius')
        if 'Capricorn' in locations_with_cards:
            locations_with_cards["The researchers and scholars of the Ancient Archives <i> Capricorn, Sorcerer </i>"] = locations_with_cards.pop('Capricorn')
        if 'Aquarius' in locations_with_cards:
            locations_with_cards["The druids and hermits of the Starlit Atoll <i> Aquarius, Sage </i>"] = locations_with_cards.pop('Aquarius')
        if 'Pisces' in locations_with_cards:
            locations_with_cards["The dead and nearly dead of the Graven Isle <i> Pisces, Necromancer </i>"] = locations_with_cards.pop('Pisces')
        layout = QVBoxLayout(faust_pop)
        mercury_alone_html = ""
        card_string = "%s" % "".join(["<h2>%s</h2> now have %s schemes of the devil in their midst.<br>" % (k, locations_with_cards[k]) for k in sorted(locations_with_cards)])
        mercury_among_html = ""
        if magic_number == 0:
            mercury_alone_html = """
                <h2> The Devil seeks the affection of another Wizard.</h2>
                    Another Wizard recieves an invitation to Spend Time and have a Scene with the Devil, in which the Devil will make him a Bargain. If a Wizard refuses to meet with the Devil at all, the Devil places a Scheme onto each of that Wizard's Communities.
                """
        else:
            mercury_among_html = f"""
            <h2> The Devil Schemes </h2>
            {card_string}
            """

        self.read_the_stars_html = f"""
            <div style="font-family: serif;">
              <h1 class="break-page"> Keeper of the Chains whose fate is controlled by %s </h1>
              {mercury_alone_html}
              {mercury_among_html}
            </div>
        """ % lib.MERCURY

        faust_document = QTextDocument()
        faust_document.setHtml(self.read_the_stars_html)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setDocument(faust_document)

        layout.addWidget(text)

        faust_pop.resize(900, 600)
        faust_pop.exec()