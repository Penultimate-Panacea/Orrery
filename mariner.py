# coding=utf-8
from wizard import Wizard
import lib
from PyQt6.QtGui import QTextDocument
from PyQt6.QtWidgets import QTextEdit, QDialog, QVBoxLayout
class Mariner(Wizard):
    def __init__(self,planetary_conjunction_dict, planet_list):
        super().__init__(planetary_conjunction_dict)
        self.planets = planet_list
    def determine_season(self):
        current_house = self.planets[5].current_step
        season = ""
        print("Sol is at position %s" % current_house)
        if current_house in range(0,3):
            season = "Spring"
        elif current_house in range(3,6):
            season = "Summer"
        elif current_house in range(6,9):
            season = "Autumn"
        elif current_house in range(9,12):
            season = "Winter"
        return season

    def generate_planets_in_season(self):
        in_season_names = []
        self.determine_season()
        for p in self.planets:
            if p.name != lib.SOL: # avoid duplicate
                if self.determine_if_in_season(p):
                    in_season_names.append(p.name)
        print("The following planets are in season: %s" % in_season_names)
        return in_season_names

    def determine_if_in_season(self, planet):
        season = self.determine_season()
        season_houses = []
        print("Season is: %s" % season)
        if season == "Spring":
            season_houses = [0,1,2]
        if season == "Summer":
            season_houses = [3,4,5]
        if season == "Autumn":
            season_houses = [6,7,8]
        if season == "Winter":
            season_houses = [9,10,11]
        print("Houses in Season: %s" % season_houses)
        print("Conjunction Table: %s" % planet.conjunction_table)
        if any(p in planet.conjunction_table[planet.current_step] for p in season_houses):
            return True
        else:
            return False

    def mariner_popup(self):
        mariner_pop = QDialog()
        mariner_pop.setWindowTitle("Mariner")

        layout = QVBoxLayout(mariner_pop)

        season = self.determine_season()
        planets_in_season = self.generate_planets_in_season()

        none_in_season = ""
        mercury_venus = ""
        mars = ""
        jupiter = ""
        saturn = ""
        general_seasonal_effects = ""

        if season == "Spring":
            general_seasonal_effects = """
                <h2> Spring </h2>
                Governed by <i>Zephyrus</i>, the West Wind, which blows from the Western Horizon towards the East. <br><br>Move all Storms one Sea Eastwards, then place a Storm in either the Northwest or Southwest Horizon.
            """
        elif season == "Summer":
            general_seasonal_effects = """
                <h2> Summer </h2>
                Governed by <i>Auster</i>, the South Wind, which blows from the Southern Horizon towards the North. <br><br>Move all Storms one Sea Northwards, then place a Storm in either the Southwest or Southeast Horizon.
            """
        elif season == "Autumn":
            general_seasonal_effects = """
                <h2> Autumn </h2>
                Governed by <i>Volturnus</i>, the East Wind, which blows from the Eastern Horizon towards the West. <br><br>Move all Storms one Sea Westwards, then place a Storm in either the Northwest or Southwest Horizon.
            """
        elif season == "Winter":
            general_seasonal_effects = """
                <h2> Winter </h2>
                GGoverned by <i>Boreas</i>, the North Wind, which blows from the Northern Horizon towards the South. <br><br>Move all Storms one Sea Southwards, then place a Storm in either the Northwest or Northeast Horizon.
            """

        if (lib.MERCURY in planets_in_season) ^ (lib.VENUS in planets_in_season):
            if season == "Spring":
                mercury_venus = """
                    <h3> Mercury or Venus in Season -- The West Wind brings gentle rains</h3>
                    Place three Routes on any paths.
                """
            if season == "Summer":
                mercury_venus = """
                    <h3> Mercury or Venus in Season -- The South Wind brings warm weather</h3>
                    Place three Routes on any paths.
                """
            if season == "Autumn":
                mercury_venus = """
                    <h3> Mercury or Venus in Season -- The East wind brings cool tidings</h3>
                    Place two Routes on any paths.
                """
            if season == "Winter":
                mercury_venus = """
                    <h3> Mercury or Venus in Season -- The North wind brings cold weather</h3>
                    Place one Route on any paths.
                """
        if (lib.MERCURY in planets_in_season) and (lib.VENUS in planets_in_season):
            if season == "Spring":
                mercury_venus = """
                    <h3> Mercury and Venus in Season -- The West Wind brings rains.</h3>
                    I.  Place three Routes on any paths. <br>
                    II. Place three Storms adjacent to any Storm
                """
            if season == "Summer":
                mercury_venus = """
                    <h3> Mercury and Venus in Season -- The South Wind brings warm weather and a tropical storm.</h3>
                    I.  Place three Routes on any paths. <br>
                    II. For each Storm, place another Storm in the Sea north of it.
                """
            if season == "Autumn":
                mercury_venus = """
                    <h3> Mercury and Venus in Season -- The East Wind brings cool tidings and a hurricane.</h3>
                    I.  Place two Routes on any paths. <br>
                    II. For each Storm, place two Storms in adjacent Seas.
                """
            if season == "Winter":
                mercury_venus = """
                    <h3> Mercury and Venus in Season -- The North Wind brings freezing weather.</h3>
                    I.  Place one Route on any paths. <br>
                    II. For each Storm, place one a Storm in <i>every</i> adjacent Seas.
                """
        if lib.MARS in planets_in_season:
            if season == "Spring":
                mars = """
                    <h3>Mars in Season -- The Triarchy of Ur bring wealth to Isha</h3>
                    Place an extra Bounty on each Isle connected to the Western Horizon. If there are no Isles connected in this way, instead place two Parasitic Routes, pointing towards the Western Horizon (or Connecting to Isles with Parasitic Routes connecting to the Western Horizon), as Urite warships move to extract wealth on their own terms.
                """
            if season == "Summer":
                mars = """
                    <h3>Mars in Season -- The Jarls of Nebelheim turn their gaze southwards, towards warmer seas</h3>
                    Place an extra Bounty on each Isle connected to the Northern Horizon. If there are no Isles connected in this way, instead place three Parasitic Routes, pointing towards the Northern Horizon (or Connecting to Isles with Parasitic Routes connecting to the Southern Horizon), as the hrotingmen raid Isha.
                """
            if season == "Autumn":
                mars = """
                    <h3>Mars in Season -- The black ships of the Drujlands smuggle illegal treasures into Isha</h3>
                    Place an extra Bounty on each Isle connected to the Western Horizon. If there are no Isles connected in this way, instead place two Parasitic Routes, pointing towards the Western Horizon (or Connecting to Isles with Parasitic Routes connecting to the Western Horizon), as the Drujites seek forbidden reagents for their magic.
                """
            if season == "Winter":
                mars = """
                    <h3>Mars in Season -- The golden ships of the Hecares bring rare spices north</h3>
                    Place an extra Bounty on each Isle connected to the Southern Horizon. If there are no Isles connected in this way, instead place three Parasitic Routes, pointing towards the Southern Horizon (or Connecting to Isles with Parasitic Routes connecting to the Southern Horizon), as King Elpenor raids Isha to fuel his war efforts.
                """
        if lib.JUPITER in planets_in_season:
            if season == "Spring":
                jupiter = """
                    <h3> Jupiter is Season -- A Beast of Air acts </h3>
                    <b><u>IF this is the First Time Jupiter has appeared in Spring</u></b><br>
                    A strange beast arrives in Isha from the distant west. Add a Roc, a Sphinx, or other Beast of Air to any empty Sea on the Map. <br><br>
                    <b><u>ELSE</u></b><br>
                    The Beast's flight changes weather patterns. Move each Storm away from the Beast. 
                """
            if season == "Summer":
                jupiter = """
                    <h3> Jupiter is Season -- A Beast of Fire acts </h3>
                    <b><u>IF this is the First Time Jupiter has appeared in Summer</u></b><br>
                    A beautiful beast arrives from the distant south. Add a Dragon, Phoenix, or other Beast of Fire to any empty Sea on the Map. <br><br>
                    <b><u>ELSE</u></b><br>
                    Bounty hunters upset the great beast. Replace all Routes adjacent to the Beast with Parasitic Routes. 
                """
            if season == "Autumn":
                jupiter = """
                    <h3> Jupiter is Season -- A Beast of Earth acts </h3>
                    <b><u>IF this is the First Time Jupiter has appeared in Autumn</u></b><br>
                    A great beast awakens from beneath the soil Add a Giant, Behemoth, or other Beast of Earth Nesting the Isle with the lowest Commerce. <br><br>
                    <b><u>ELSE</u></b><br>
                    The inhabitants of the Isle begin illegal operations to bring it food. Place a Parasitic Route connecting that Isle to any other Isle. 
                """
            if season == "Winter":
                jupiter = """
                    <h3> Jupiter is Season -- A Beast of Water acts </h3>
                    <b><u>IF this is the First Time Jupiter has appeared in Winter</u></b><br>
                    An enormous beast arrives from the freezing north, seeking warmer waters. Add a Kraken, Sea Serpent, or other Beast of Water to any empty Sea on the Map. <br><br>
                    <b><u>ELSE</u></b><br>
                    The Beast asserts its domain. Destroy all adjacent Routes.
                """
        if lib.SATURN in planets_in_season:
            if season == "Spring":
                saturn = """
                <h3> Saturn in Season -- An Earthquake strikes Isha</h3>
                Choose any two random Isles across Isha, and draw a straight line connecting them. Remove all Bounty from Isles touching this straight line.
                """
            if season == "Summer":
                saturn = """
                <h3> Saturn in Season -- Pirates roam the archipelago</h3>
                 For each Isle tied for the fewest Bounty, place a Parasitic Route pointing towards that Isle.
                """
            if season == "Autumn":
                saturn = """
                <h3> Saturn in Season -- Upon sacred Tahv the slumbering Mt. Ithax rumbles, and lava pours from its peak.</h3>
                Place a Storm in two Seas adjacent to Tahv. If Tahv is already surrounded by Storms, Mt. Ithax instead erupts. Ravage Tahv, and place a Storm in every Sea adjacent to Tahv.                
                """
            if season == "Winter":
                saturn = """
                <h3> Saturn in Season -- A wretched rot strikes Isha's storehouses</h3>
                 For the rest of the Season, reduce the Commerce of all Isles by 1.
                """
        if len(planets_in_season) == 0:
            if season == "Spring":
                none_in_season = """
                    <h3> No Celestial Bodies within Season -- Still winds bring rotten fish to the shores of Isha.</h3>
                    Remove each Route which isn't itself adjacent to a Storm.
                """
            if season == "Summer":
                none_in_season = """
                    <h3> No Celestial Bodies within Season -- A heatwave washes across Isha, and crops wither in the drought.</h3>
                    Remove each Route which isn't itself adjacent to a Storm.
                """
            if season == "Autumn":
                none_in_season = """
                    <h3> No Celestial Bodies within Season -- Fickle winds bring disarray to Isha's shipping lanes.</h3>
                    I.  Remove three Routes<br>
                    II. Pace a Storm in each Sea without any adjacent Storms.
                """
            if season == "Winter":
                none_in_season = """
                    <h3> No Celestial Bodies within Season -- Isha's ports freeze over, and a wretched cold settles across the archipelago.</h3>
                    Remove half of all Routes, rounding up.
                """

        self.read_the_stars_html = f"""
                    <div style="font-family: serif;">
                      <h1> Mariner </h1>
                      {general_seasonal_effects}
                      {none_in_season}
                      {mercury_venus}
                      {mars}
                      {jupiter}
                      {saturn}
                    </div>
                """
        mariner_document = QTextDocument()
        mariner_document.setHtml(self.read_the_stars_html)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setDocument(mariner_document)

        layout.addWidget(text)

        mariner_pop.resize(900,600)
        mariner_pop.exec()


