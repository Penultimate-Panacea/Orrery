# coding=utf-8
from wizard import Wizard
from dataclasses import dataclass
import lib
from PyQt6.QtGui import QTextDocument
from PyQt6.QtWidgets import QTextEdit, QDialog, QVBoxLayout
class Warlock(Wizard):
    def __init__(self,planetary_conjunction_dict):
        super().__init__(planetary_conjunction_dict)


@dataclass
class King:
    def __init__(self):
        self.rising_sign = lib.JUPITER
