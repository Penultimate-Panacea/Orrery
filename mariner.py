from wizard import Wizard
import lib
from PyQt6.QtGui import QTextDocument
from PyQt6.QtWidgets import QTextEdit, QDialog, QVBoxLayout
class Mariner(Wizard):
    def __init__(self,planetary_conjunction_dict):
        super().__init__(planetary_conjunction_dict)
        self.season = None #TODO Season class
