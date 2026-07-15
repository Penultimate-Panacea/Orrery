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
                Governed by <i>Zephyrus</i>, the West Wind, which blows from the Western Horizon towards the East. Move all Storms one Sea Eastwards, then place a Storm in either the Northwest or Southwest Horizon.
            """

        if (lib.MERCURY in planets_in_season) ^ (lib.VENUS in planets_in_season):
            if season == "Spring":
                mercury_venus = """
                    <h3> Mercury or Venus in Season -- The West Wind brings gentle rains</h3>
                    Place three Routes on any paths.
                """
        if (lib.MERCURY in planets_in_season) and (lib.VENUS in planets_in_season):
            if season == "Spring":
                mercury_venus = """
                    <h3> Mercury and Venus in Season -- The West Wind brings rains.</h3>
                    I.  Place three Routes on any paths. <br>
                    II. Place three Storms adjacent to any Storm
                """
        if lib.MARS in planets_in_season:
            if season == "Spring":
                mars = """
                    <h3>Mars in Season -- The Triarchy of Ur bring wealth to Isha</h3>
                    Place an extra Bounty on each Isle connected to the Western Horizon. If there are no Isles connected in this way, instead place two Parasitic Routes, pointing towards the Western Horizon (or Connecting to Isles with Parasitic Routes connecting to the Western Horizon), as Urite warships move to extract wealth on their own terms.
                """
        if lib.JUPITER in planets_in_season:
            if season == "Spring":
                jupiter = """
                    <h3> Jupiter is Season -- A Beast of Air acts </h3>
                    <b><u>IF THIS IS THE FIRST TIME JUPITER HAS APPEARED IN THE CURRENT SEASON</u></b><br>
                    A strange beast arrives in Isha from the distant west. Add a Roc, a Sphinx, or other Beast of Air to any empty Sea on the Map. <br><br>
                    <b><u>ELSE</u></b><br>
                    The Beast's flight changes weather patterns. Move each Storm away from the Beast. 
                """
        if lib.SATURN in planets_in_season:
            if season == "Spring":
                saturn = """
                <h3> Saturn in Season -- An Earthquake strikes Isha</h3>
                Choose any two random Isles across Isha, and draw a straight line connecting them. Remove all Bounty from Isles touching this straight line.
                """
        if len(planets_in_season) == 0:
            if season == "Spring":
                none_in_season = """
                    <h3> No Celestial Bodies within Season -- Still winds bring rotten fish to the shores of Isha</h3>
                    Remove each Route which isn't itself adjacent to a Storm.
                """

        season_stars_html = f"""
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
        mariner_document.setHtml(season_stars_html)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setDocument(mariner_document)

        layout.addWidget(text)

        mariner_pop.resize(900,600)
        mariner_pop.exec()


