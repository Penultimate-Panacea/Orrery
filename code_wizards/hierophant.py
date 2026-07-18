# coding=utf-8
from code_wizards.wizard import Wizard
from code_plumbing import lib
from PyQt6.QtGui import QTextDocument
from PyQt6.QtWidgets import QTextEdit, QDialog, QVBoxLayout
class Hierophant(Wizard):
    def __init__(self,planetary_conjunction_dict):
        super().__init__(planetary_conjunction_dict)

    def make_magic_number(self):
        conjunctions = self.planet_conjunction_dict
        print("Conjunctions are: " + str(conjunctions))
        sol_conjunctions = conjunctions[lib.SOL]
        hierophant_magic_number = 0b0000000
        if len(sol_conjunctions) == 0:
            print("Sol Stands Alone")
            hierophant_magic_number ^= (1 << 0)

        if lib.MERCURY in sol_conjunctions:
            print("Mercury in Conjunction with Sol")
            hierophant_magic_number ^= (1 << 1)

        if lib.VENUS in sol_conjunctions:
            print("Venus in Conjunction with Sol")
            hierophant_magic_number ^= (1 << 2)

        if lib.MARS in sol_conjunctions:
            print("Mars in Conjunction with Sol")
            hierophant_magic_number ^= (1 << 3)

        if lib.SATURN in sol_conjunctions:
            print("Saturn in Conjunction with Sol")
            hierophant_magic_number ^= (1 << 4)
        if lib.JUPITER in sol_conjunctions:
            print("Jupiter in Conjunction with Sol")
            hierophant_magic_number ^= (1 << 5)
        print(hierophant_magic_number)
        return hierophant_magic_number
        ## TODO: Magic number bits 6 & 7 are reserved for calamity and extinction which are beyond the scope of the project at the moment


    def hierophant_popup(self):
        hiero_pop = QDialog()
        hiero_pop.setWindowTitle("Hierophant Reads the Stars")
        self.read_the_stars()

        jupiter_document = QTextDocument()
        jupiter_document.setHtml(self.read_the_stars_html)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setDocument(jupiter_document)

        layout = QVBoxLayout(hiero_pop)
        layout.addWidget(text)

        hiero_pop.resize(900, 600)
        hiero_pop.exec()

    def read_the_stars(self):
        magic_number = self.make_magic_number()

        sol_alone_html = ""
        if magic_number & (1 << 0):
            sol_alone_html = """
                        <h2> Sol Stands Alone -- The Temples reflect and re-evaluate their Doctrine </h2>
                            Each Temple tied for the lowest Conviction must change its Doctrine to any random other Doctrine.
                        """

        mercury_html = ""
        if magic_number & (1 << 1):
            mercury_html = """
                        <h2> Mercury in Conjunction with Sol -- The Temples are in need of repair. </h2>
                        Each Temple takes -1 Abundance. If any Temple has no Abundance, it instead gains a random Supplicant and takes -1 Conviction.
                    """

        venus_html = ""
        if magic_number & (1 << 2):
            venus_html = f"""
                               <h2> Venus in Conjunction with Sol -- A new Supplicant arrives at the Temples, looking for guidance and advice</h2>
                               For each Temple tied for the fewest Supplicants (besides Temple Hestar) roll a D6, adding a Supplicant with three Woe based on the result.
                               <ul>
                               <li>If {lib.SALT} was rolled add a Gentry. </li>
                               <li>If {lib.JUPITER} was rolled add a Peasant. </li>
                               <li>If {lib.MARS} was rolled add an Artisan. </li>
                               <li>If {lib.VENUS} was rolled add a Merchant. </li>
                               </ul>
                           """

        mars_html = ""
        if magic_number & (1 << 3):
            ars_html = f"""
                                       <h2> Mars in Conjunction with Sol -- Violence and conflict brings a Supplicant to the Temples, someone whose life has been marred by war.</h2>
                                       For each Temple tied for the least Abundance (besides Temple Hestar) roll a D6, adding a Supplicant with four Woe based on the result.
                                           <ul>
                                           <li>If {lib.SALT} was rolled add a Pariah. </li>
                                           <li>If {lib.JUPITER} was rolled add a Peasant. </li>
                                           <li>If {lib.MARS} was rolled add an Artisan. </li>
                                           <li>If {lib.VENUS} was rolled add a Merchant. </li>
                                           </ul>
                                   """

        saturn_html = ""
        if magic_number & (1 << 4):
            saturn_html = f"""
                                            <h2> Saturn in Conjunction with Sol -- The populaces flood the Temple, seeking respite from the chaos of the outside world.</h2>
                                            For each Temple tied for the most Abundance (besides Temple Hestar) roll a D6, adding a Supplicant with four Woe based on the result.
                                           <ul>
                                           <li>If {lib.SALT} was rolled add a Pariah. </li>
                                           <li>If {lib.JUPITER} was rolled add a Peasant. </li>
                                           <li>If {lib.MARS} was rolled add an Artisan. </li>
                                           <li>If {lib.VENUS} was rolled add a Merchant. </li>
                                           </ul>
                                        """

        jupiter_html = ""
        if magic_number & (1 << 5):
            jupiter_html = """
                                               <h2> Jupiter is in Conjunction with Sol -- The populace look to the Flames for guidance.</h2>
                                               Each Temple with a Holiday Marker takes -2 Conviction. <br>
                                               <b><i>If it is a Feast Day,</i></b> then create a new Prophet at any Temple with the most Conviction.
                                           """
        self.set_date_string()
        self.read_the_stars_html = f"""
                    <div style="font-family: serif;">
                      <h1 class="break-page"> Keeper of the Flames whose fate is controlled by %s </h1> 
                      {sol_alone_html}
                      {mercury_html}
                      {venus_html}
                      {mars_html}
                      {saturn_html}
                      {jupiter_html}
                      <br><br><br>
                          <center><h3> Report produced for {self.date_string}</h3> </center>
                    </div>
                """ % lib.JUPITER
        return