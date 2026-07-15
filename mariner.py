# coding=utf-8
from wizard import Wizard
import lib
from PyQt6.QtGui import QTextDocument
from PyQt6.QtWidgets import QTextEdit, QDialog, QVBoxLayout
class Mariner(Wizard):
    def __init__(self,planetary_conjunction_dict, planet_list):
        super().__init__(planetary_conjunction_dict)
        self.planets = planet_list
        self.season = None
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
        in_season_bool_dict = {}
        self.determine_season()
        for p in self.planets:
            if p.name != lib.SOL: # avoid duplicate
                in_season_bool_dict[p.name] = self.determine_if_in_season(p)
        print("The following planets are in season: %s" % in_season_bool_dict)

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


