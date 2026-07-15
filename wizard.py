# coding=utf-8
import lib

class Wizard:
    def __init__(self,planet_conjunction_dict):
        self.associated_planet = None
        self.water = None
        self.fire = None
        self.earth = None
        self.air = None
        self.planet_conjunction_dict = planet_conjunction_dict


    def update_conjunctions(self, new_dict):
        self.planet_conjunction_dict = new_dict
