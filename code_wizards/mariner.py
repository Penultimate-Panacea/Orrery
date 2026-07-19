# coding=utf-8
from code_wizards.wizard import Wizard
from code_plumbing import lib
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

    def popup(self):
        mariner_pop = QDialog()
        mariner_pop.setWindowTitle("Mariner")

        layout = QVBoxLayout(mariner_pop)
        self.read_the_stars()

        mariner_document = QTextDocument()
        mariner_document.setHtml(self.read_the_stars_html)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setDocument(mariner_document)

        layout.addWidget(text)

        mariner_pop.resize(900,600)
        mariner_pop.exec()

    def read_the_stars(self):
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
                        <h2> The Winds of Spring </h2>
                        Governed by <i>Zephyrus</i>, the West Wind, which blows from the Western Horizon towards the East. Move Storms towards the East.
                    """
        elif season == "Summer":
            general_seasonal_effects = """
                        <h2> The Winds of Summer </h2>
                        Governed by <i>Auster</i>, the South Wind, which blows from the Southern Horizon towards the North. Move Storms towards the North.
                    """
        elif season == "Autumn":
            general_seasonal_effects = """
                        <h2> The Winds of Autumn </h2>
                        Governed by <i>Volturnus</i>, the East Wind, which blows from the Eastern Horizon towards the West. Move Storms towards the West.
                    """
        elif season == "Winter":
            general_seasonal_effects = """
                        <h2> The Winds of Winter </h2>
                        Governed by <i>Boreas</i>, the North Wind, which blows from the Northern Horizon towards the South. Move Storms towards the South.
                    """

        if (lib.MERCURY in planets_in_season) ^ (lib.VENUS in planets_in_season):
            if season == "Spring":
                mercury_venus = """
                            <h2> Mercury or Venus in Season -- The West Wind brings gentle rains.</h2>
                            Choose a Storm. Place another Storm in any adjacent Sea.
                        """
            if season == "Summer":
                mercury_venus = """
                            <h2> Mercury or Venus in Season -- The South Wind brings warm weather.</h2>
                            Choose a Storm. Place a Storm in each adjacent Sea.
                        """
            if season == "Autumn":
                mercury_venus = """
                            <h2> Mercury or Venus in Season -- The East wind brings a biting gale.</h2>
                            For each Storm, place a Storm in an adjacent Sea.
                        """
            if season == "Winter":
                mercury_venus = """
                            <h2> Mercury or Venus in Season -- The North wind brings a freezing wind.</h2>
                            For each Storm, place a Storm in an adjacent Sea.
                        """
        if (lib.MERCURY in planets_in_season) and (lib.VENUS in planets_in_season):
            if season == "Spring":
                mercury_venus = """
                            <h2> Mercury and Venus in Season -- The West Wind brings heavy rains which threaten farmland.</h2>
                            Choose a Storm. Place a Storm in an adjacent Sea. For the duration of the Season, each Isle adjacent to a Storm takes -1 Stability.
                        """
            if season == "Summer":
                mercury_venus = """
                            <h2> Mercury and Venus in Season -- The South Wind brings a warm storm.</h2>
                            Choose a Storm. Place a Storm in each adjacent Sea. Each Storm with at least three adjacent Storms becomes a Typhoon.
                        """
            if season == "Autumn":
                mercury_venus = """
                            <h2> Mercury and Venus in Season -- The East Wind brings treacherous winds.</h2>
                            For each Storm, place a Storm in an adjacent Sea. Flip a coin each Market, and remove that Market on Tails.
                        """
            if season == "Winter":
                mercury_venus = """
                            <h2> Mercury and Venus in Season -- The North Wind brings heavy snows and ports freeze over.</h2>
                            For each Storm, place a Storm in an adjacent Sea. For the rest of the Season, all Isles have -1 Stability.
                        """
        if lib.MARS in planets_in_season:
            if season == "Spring":
                mars = """
                            <h2>Mars in Season -- Beasts of Air act.</h2>
                            A Distrusting Beast of Air arrives in Isha. Add a Roc, a Sphinx, or other Beast of Air to any empty Sea on the Map.<br>
                            <b><i>If there was already a Beast of Air in Isha,</i></b> instead the Beast's flight changes weather patterns. Move each Storm away from the Beast. This cannot cause Storms to move out of Isha.
                            
                        """
            if season == "Summer":
                mars = """
                            <h2>Mars in Season -- Beasts of Fire.</h2>
                            A Distrusting Beast of Fire arrives in Isha. Add a Dragon, Chimera, or other beast of Fire to any empty Sea on the Map.<br>
                            <b><i>If there was already a Beast of Fire in Isha,</i></b> instead bounty hunters upset the great beast. Place a Raider Ship in an adjacent Route.
                        """
            if season == "Autumn":
                mars = """
                            <h2>Mars in Season -- Beasts of Earth.</h2>
                            A Nesting Beast of Earth awakens in Isha. Add a Titan, Goliath, or other Beast of Earth to any Isle.<br>
                            <b><i>If there was already a Beast of Earth in Isha,</i></b> was present within the season last month, instead the inhabitants of the Isle being illegal operations to bring it food. Place a Raider Ship from that Isle <i>(replacing a Ship if necessary)</i>
                        """
            if season == "Winter":
                mars = """
                            <h2>Mars in Season -- Beasts of Water.</h2>
                            A Distrusting Beast of Water arrives in Isha. Add a Kraken, Leviathan, or other Beast of Water to any empty Sea on the Map.<br>
                            <b><i>If there was already a Beast of Water in Isha,</i></b> the Beast instead asserts its domain. Destroy all adjacent Ships.
                        """
        if lib.JUPITER in planets_in_season:
            if season == "Spring":
                jupiter = """
                            <h2> Jupiter is in Season, the people of Isha establish trade routes with the world</h2>
                            Place three Ships along any three Connecting Routes.<br>
                            <b><i>If the placements of these Routes create a Market that Connects to the Western Horizon,</i></b> place a Rarity within the Market, as merchants from the Druj-Lands sell silks, ancient tomes, and forbidden magic.<br>
                            <b><i>If fewer than three Ships can be placed in this fashion,</i></b> instead turn two Connecting Ships into Raider Ships both pointing towards the same Isle.
                        """
            if season == "Summer":
                jupiter = """
                            <h2> Jupiter is in Season, the people of Isha establish trade routes with each other.</h2>
                            Place three Ships along any three Connecting Routes.<br>
                            <b><i>If the placements of these Routes create a Market that Connects to the Southern Horizon,</i></b> place a Rarity within the Market, as merchants from the Hecares sell figs, herbs, and rare spices.<br>
                            <b><i>If fewer than three Ships can be placed in this fashion,</i></b> instead turn two Connecting Ships into Raider Ships both pointing towards the same Isle.
                        """
            if season == "Autumn":
                jupiter = """
                            <h2> Jupiter is in Season, the people of Isha reach out to each other.</h2>
                            Place two Ships along any three Connecting Routes.<br>
                            <b><i>If the placement of these Routes create a Market that Connects to the Eastern Horizon,</i></b> place a Rarity within the Market, as merchants from distant Ur bring clay tablets, pottery, and jade.<br>
                            <b><i>If fewer than three Ships can be placed in this fashion,</i></b> instead turn two Connecting Ships into Raider Ships both pointing towards the same Isle.
                        """
            if season == "Winter":
                jupiter = """
                            <h2> Jupiter is in Season, the people of Isha reach out to each other.</h2>
                            Place two Ships along any three Connecting Routes.<br>
                            <b><i>If the placement of these Routes create a Market,</i></b> place a Rarity within the Market, then place two Raiding ships <i>(replacing Ships if necessary)</i> Connected to the Northern Horizon.
                        """
        if lib.SATURN in planets_in_season:
            if season == "Spring":
                saturn = """
                        <h2> Saturn is in Season, still winds bring rotten fish to the shores of Isha.</h2>
                        Remove each Ship which <i>isn't</i> adjacent to a Storm.
                        """
            if season == "Summer":
                saturn = """
                        <h2> Saturn is in Season, a heatwave washes across Isha, and crops wither in the drought.</h2>
                         For each Isle tied for the highest Stability, place a Raider Ship raiding an adjacent Isle.
                        """
            if season == "Autumn":
                saturn = """
                        <h2> Saturn is in Season, upon sacred Tahv the slumbering Mt. Ithax rumbles, and lava pours from its peak.</h2>
                        Place a Storm in two Seas adjacent to Tahv. If Tahv is already surrounded by Storms, Mt. Ithax instead erupts. Ravage Tahv, and place a Storm in every Sea adjacent to Tahv.                
                        """
            if season == "Winter":
                saturn = """
                        <h2> Saturn is in Season, Isha's ports freeze over, and a wretched cold settles across the archipelago.</h2>
                         Remove half of all Ships, rounding up.
                        """
        if len(planets_in_season) == 0:
            if season == "Spring":
                none_in_season = """
                            <h2> No planets lie within Spring and an earthquake strikes Isha.</h2>
                            Choose any two random Isles across Isha, and draw a straight line connecting them. Ravage each Isle touching that line.
                        """
            if season == "Summer":
                none_in_season = """
                            <h2> No planets lie within Summer and powerful merchants demand tithes from their lands.</h2>
                            For each Isle tied for the highest Stability, replace one Ship with a Raider Ship raiding an adjacent Isle.
                        """
            if season == "Autumn":
                none_in_season = """
                            <h2> No planets lie within Autumn and fickle winds bring disarray to Isha's shipping lanes.</h2>
                            Remove three Ships, then place a Storm in each Sea without any adjacent Storms.
                        """
            if season == "Winter":
                none_in_season = """
                            <h2> No planets lie within Winter and the starving and desperate are forced to take action.</h2>
                            For each Isle tied for lowest Stability, place a Raiding Ship from that Isle.
                        """
        self.set_date_string()
        self.read_the_stars_html = f"""
                            <div style="font-family: serif;">
                              <h1 class="break-page"> Wilds-Watcher who is concerned with the movements of the Seasons </h1>
                              {general_seasonal_effects}
                              {none_in_season}
                              {mercury_venus}
                              {mars}
                              {jupiter}
                              {saturn}
                              <br><br><br>
                          <center><h3> Report produced for {self.date_string}</h3> </center>
                            </div>
                        """
