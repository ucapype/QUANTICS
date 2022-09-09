##module quantic gui library
'''
python library for quantics
'''

import os

import MCTDH_.mctdhinp as mctdhinp  #quantics file reading functions
import gui_logic.gui_logic as gui_logic #logic tests for controls
#import gui bits
#import PyQt5
from PyQt5 import QtWidgets, uic, QtCore
#from PyQt5.QtWidgets import QFileDialog

class Ui(QtWidgets.QMainWindow):
    '''
    Class to hold the gui info
    '''
    def __init__(self, parser):
        '''
        initialise class by loading the .ui file
        '''
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        # Load the .ui file
        #find directory path for ui folder
        uidir = os.path.dirname(__file__)
        #create path for ui file
        uifile = os.path.join(uidir, 'Input_main.ui')
        #load the ui
        uic.loadUi(uifile, self)
        
        #uic.loadUi(uifile, self)
        print(self.file_text.toPlainText())
        #find controls
        #first nontab controls
        self.find_inp_cntrls()
        self.find_tab_info()
        for tab in self.sections:
            getattr(self,self.sections[tab]['function'])()
        
        self.info_txt.append(self.file_text.toPlainText())
        #get special controls for actions etc
        self.level_cntrls()
        #set up menu actions
        self.menu_actions()
        #set up button actions
        self.butt_actions()
        #load values from input file (if given)
        if parser.f != "":
            self.load_inp_file(parser.f)

        #save current geometry
        self.main_geometry = self.geometry()
        #save all tabs
        self.main_tabs = []
        self.main_tab_texts = []
        self.main_tab_num = self.maintab.count()
        for tab_index in reversed(range(self.main_tab_num)):
            self.main_tabs.append(self.maintab.widget(tab_index))
            self.main_tab_texts.append(self.maintab.tabText(tab_index))
        #initialize menu
        self.page_kind_select_init()

        #initialize the dynamic layout of spf_tab and spdo_tab
        self.spf_nuclear_layout_ini()
        self.spdo_nuclear_layout_ini()

        self.show() # Show the GUI

    def wf_stackedwidget_updata(self):
        '''
        updata the stackedwidget in wf_tab
        '''
        if self.wfReadFileRBtn.isChecked():
            self.wfStackedWidget.setCurrentIndex(0)
        elif self.wfBuildRBtn.isChecked():
            self.wfStackedWidget.setCurrentIndex(1)

    def wf_mode_updata(self):
        '''
        updata the string in wf_tab
        '''
        self.unique_wf_mode = []
        if self.wfReadFileRBtn.isChecked() and self.wfFileNameEdit.text() != "":
            self.unique_wf_mode.append("file = " + self.wfFileNameEdit.text())
        elif self.wfBuildRBtn.isChecked():
            self.unique_wf_mode.append("el el " + str(self.wfElecSBox.value()))
            for i in range(self.wfNuclSBox.value()):
                self.unique_wf_mode.append("Q_" + str(i + 1) + " HO 15 0.0 1.0 1.0")

    def spf_nuclear_layout_ini(self):
        '''
        initialize the layout about nuclear in spf_tab
        '''
        self.spf_nuclear_checkboxes = []
        self.spf_nuclear_spinboxes = []
        self.spf_nuclear_current_num = 0
        self.spf_nuclear_name = "R"

    def spf_nuclear_layout_updata(self):
        '''
        updata the layout about nuclear in spf_tab
        '''
        #if nuclear_num overflow, fill the list
        nuclear_num_new = self.spfNuclSBox.value()
        if nuclear_num_new >  len(self.spf_nuclear_checkboxes):
            for i in range(len(self.spf_nuclear_checkboxes), nuclear_num_new):
                self.spf_nuclear_checkboxes.append(QtWidgets.QCheckBox(self))
                self.spf_nuclear_checkboxes[i].setCheckState(QtCore.Qt.CheckState.Unchecked)
                self.spf_nuclear_checkboxes[i].stateChanged.connect(self.spf_nuclear_layout_updata)
                self.spf_nuclear_spinboxes.append(QtWidgets.QSpinBox(self))
                self.spf_nuclear_spinboxes[i].setRange(0, 999)
                self.spf_nuclear_spinboxes[i].setValue(0)
                self.spf_nuclear_spinboxes[i].setEnabled(False)

        #if nuclear_num increased, add widget
        if nuclear_num_new > self.spf_nuclear_current_num:
            for i in range(self.spf_nuclear_current_num, nuclear_num_new):
                self.spfNuclearGridLayout.addWidget(self.spf_nuclear_checkboxes[i], i, 0)
                self.spf_nuclear_checkboxes[i].show()
                self.spfNuclearGridLayout.addWidget(self.spf_nuclear_spinboxes[i], i, 1)
                self.spf_nuclear_spinboxes[i].show()
        #if nuclear_num reduced, remove redundant widget
        elif nuclear_num_new < self.spf_nuclear_current_num:
            for i in range(nuclear_num_new, self.spf_nuclear_current_num):
                self.spfNuclearGridLayout.removeWidget(self.spf_nuclear_checkboxes[i])
                self.spf_nuclear_checkboxes[i].hide()
                self.spfNuclearGridLayout.removeWidget(self.spf_nuclear_spinboxes[i])
                self.spf_nuclear_spinboxes[i].hide()
        self.spf_nuclear_current_num = nuclear_num_new

        # updata the name
        if self.spfDefaultRBtn.isChecked():
            self.spf_nuclear_name = "R"
        else:
            self.spf_nuclear_name = self.spfCustomEdit.text()
        for i in range(nuclear_num_new):
            self.spf_nuclear_checkboxes[i].setText(self.spf_nuclear_name + "_" + str(i + 1))

        #enable checked QSpinBox
        for i in range(self.spf_nuclear_current_num):
            if self.spf_nuclear_checkboxes[i].isChecked():
                self.spf_nuclear_spinboxes[i].setEnabled(True)
            else:
                self.spf_nuclear_spinboxes[i].setEnabled(False)


    def spf_nuclear_updata(self):
        '''
        updata the string about nuclear in spf_tab
        '''
        self.unique_spf_nuclear = []
        for i in range(self.spf_nuclear_current_num):
            if self.spf_nuclear_checkboxes[i].isChecked():
                self.unique_spf_nuclear.append(" " + self.spf_nuclear_name + "_" + str(i+1) + " = " + str(self.spf_nuclear_spinboxes[i].value()))

    def spf_set_update(self):
        '''
        updata the string about set mode in spf_tab
        '''
        self.unique_spf_set = []
        if self.spfSingleSetRBtn.isChecked():
            self.unique_spf_set.append("single-set")
        elif self.spfMultiSetRbtn.isChecked():
            self.unique_spf_set.append("multi-set")
            
    def spdo_nuclear_layout_ini(self):
        '''
        initialize the layout about nuclear in spdo_tab
        '''
        self.spdo_nuclear_checkboxes = []
        self.spdo_nuclear_spinboxes = []
        self.spdo_nuclear_current_num = 0
        self.spdo_nuclear_name = "R"

    def spdo_nuclear_layout_updata(self):
        '''
        updata the layout about nuclear in spdo_tab
        '''
        #if nuclear_num overflow, fill the list
        nuclear_num_new = self.spdoNuclSBox.value()
        if nuclear_num_new >  len(self.spdo_nuclear_checkboxes):
            for i in range(len(self.spdo_nuclear_checkboxes), nuclear_num_new):
                self.spdo_nuclear_checkboxes.append(QtWidgets.QCheckBox(self))
                self.spdo_nuclear_checkboxes[i].setCheckState(QtCore.Qt.CheckState.Unchecked)
                self.spdo_nuclear_checkboxes[i].stateChanged.connect(self.spdo_nuclear_layout_updata)
                self.spdo_nuclear_spinboxes.append(QtWidgets.QSpinBox(self))
                self.spdo_nuclear_spinboxes[i].setRange(0, 999)
                self.spdo_nuclear_spinboxes[i].setValue(0)
                self.spdo_nuclear_spinboxes[i].setEnabled(False)

        #if nuclear_num increased, add widget
        if nuclear_num_new > self.spdo_nuclear_current_num:
            for i in range(self.spdo_nuclear_current_num, nuclear_num_new):
                self.spdoNuclearGridLayout.addWidget(self.spdo_nuclear_checkboxes[i], i, 0)
                self.spdo_nuclear_checkboxes[i].show()
                self.spdoNuclearGridLayout.addWidget(self.spdo_nuclear_spinboxes[i], i, 1)
                self.spdo_nuclear_spinboxes[i].show()
        #if nuclear_num reduced, remove redundant widget
        elif nuclear_num_new < self.spdo_nuclear_current_num:
            for i in range(nuclear_num_new, self.spdo_nuclear_current_num):
                self.spdoNuclearGridLayout.removeWidget(self.spdo_nuclear_checkboxes[i])
                self.spdo_nuclear_checkboxes[i].hide()
                self.spdoNuclearGridLayout.removeWidget(self.spdo_nuclear_spinboxes[i])
                self.spdo_nuclear_spinboxes[i].hide()
        self.spdo_nuclear_current_num = nuclear_num_new

        # updata the name
        if self.spdoDefaultRBtn.isChecked():
            self.spdo_nuclear_name = "R"
        else:
            self.spdo_nuclear_name = self.spdoCustomEdit.text()
        for i in range(nuclear_num_new):
            self.spdo_nuclear_checkboxes[i].setText(self.spdo_nuclear_name + "_" + str(i + 1))

        #enable checked QSpinBox
        for i in range(self.spdo_nuclear_current_num):
            if self.spdo_nuclear_checkboxes[i].isChecked():
                self.spdo_nuclear_spinboxes[i].setEnabled(True)
            else:
                self.spdo_nuclear_spinboxes[i].setEnabled(False)

    def spdo_nuclear_updata(self):
        '''
        updata the string about nuclear in spdo_tab
        '''
        self.unique_spdo_nuclear = []
        for i in range(self.spdo_nuclear_current_num):
            if self.spdo_nuclear_checkboxes[i].isChecked():
                self.unique_spdo_nuclear.append(" " + self.spdo_nuclear_name + "_" + str(i+1) + " = " + str(self.spdo_nuclear_spinboxes[i].value()))

    def spdo_set_update(self):
        '''
        updata the string about set mode in spdo_tab
        '''
        self.unique_spdo_set = []
        if self.spdoSingleSetRBtn.isChecked():
            self.unique_spdo_set.append("single-set")
        elif self.spdoMultiSetRbtn.isChecked():
            self.unique_spdo_set.append("multi-set")

    def run_file_to_generate_updata(self):
        '''
        updata the string about file to generate in run_tab
        '''
        self.unique_run_file = []
        str_tem = "file to generate = "
        if self.runGridpopRBtn.isChecked():
            str_tem += "gridpop"
        elif self.runAutoRBtn.isChecked():
            str_tem += "auto"
        elif self.runStepsRBtn.isChecked():
            str_tem += "steps"
        self.unique_run_file.append(str_tem)

    def run_name_updata(self):
        '''
        updata the name in run_tab, ensure it not empty
        '''
        if self.name_txt.toPlainText().strip() == "":
            self.name_txt.setPlainText("NULL")

    def prim_electronic_updata(self):
        '''
        updata the string about No.of electronic in prim_tab
        '''
        self.unique_prim_electronic = []
        self.unique_prim_electronic.append("el el " + str(self.primElecSBox.value()))

    def prim_nuclear_updata(self):
        '''
        updata the string about No.of nuclear in prim_tab
        '''
        self.unique_prim_nuclear = []
        if self.primDefaultRBtn.isChecked():
            name = "R"
        else:
            name = self.primCustomEdit.text()
        for i in range(self.primNuclSBox.value()):
            self.unique_prim_nuclear.append(name + "_" + str(i+1) + " HO 15 0.0 1.0 1.0")

    def uniques_updata(self):
        '''
        updata all unique strings
        '''
        self.run_file_to_generate_updata()
        self.prim_electronic_updata()
        self.prim_nuclear_updata()
        self.spf_nuclear_updata()
        self.spf_set_update()
        self.spdo_nuclear_updata()
        self.spdo_set_update()
        self.wf_mode_updata()

    def previous_page_clicked(self):
        '''
        switch QStackedWidget back to page_MCTDH_select or page_direct_select
        '''
        #back to last page
        self.kind_start()

    def kind_start(self):
        '''
        start with selected kind (the first start action)
        '''
        if self.directRBtn.isChecked():
            self.page_direct_select_init()
            return
        elif self.MCTDHRBtn.isChecked():
            self.page_MCTDH_select_init()
            return
        else:
            return

    def direct_start(self):
        '''
        start Direct Dynamic mode with selected tabs (the second start action)
        '''
        self.include_tabs = []
        if self.directRunCBox.isChecked():
            self.include_tabs.append("Run")
        if self.directCBox.isChecked():
            self.include_tabs.append("Direct Dynamics")
        if self.geometryCBox.isChecked():
            self.include_tabs.append("Initial Geom")
        self.page_main_init()

    def MCTDH_start(self):
        '''
        start MCTDH mode with selected tabs (the second start action)
        '''
        #collect selected tabs
        self.include_tabs = []
        if self.MCTDHRunCBox.isChecked():
            self.include_tabs.append("Run")
        if self.operatorCbox.isChecked():
            self.include_tabs.append("Operator")
        if self.initWfCBox.isChecked():
            self.include_tabs.append("Initial WF")
        if self.basisCbox.isChecked():
            self.include_tabs.append("Primative-Basis")
            if self.mlRBtn.isChecked():
                self.include_tabs.append("ML-Basis")
            elif self.spfRBtn.isChecked():
                self.include_tabs.append("SPF-Basis")
            elif self.spdoRBtn.isChecked():
                self.include_tabs.append("SPDO-Basis")
        #switch to page_main
        self.page_main_init()

    def MCTDH_basisCbox_changed(self):
        '''
        updata enabling of QRadioBox in MCTDH mode page
        '''
        if self.basisCbox.isChecked():
            self.mlRBtn.setEnabled(True)
            self.spfRBtn.setEnabled(True)
            self.spdoRBtn.setEnabled(True)
        else:
            self.mlRBtn.setEnabled(False)
            self.spfRBtn.setEnabled(False)
            self.spdoRBtn.setEnabled(False)

    def page_kind_select_init(self):
        '''
        switch QStackedWidget to page_menu, and initialize it
        '''
        #switch QStackedWidget to page_menu
        self.stackedWidget.setCurrentIndex(0)
        #hide menubar
        self.menuBar().hide()
        #resize mainwindow
        self.resize(300, 300)

    def page_direct_select_init(self):
        '''
        switch QStackedWidget to page_direct_select, and initialize it
        '''
        #switch QStackedWidget to page_MCTDH_select
        self.stackedWidget.setCurrentIndex(1)
        #hide menubar
        self.menuBar().hide()
        #resize window
        self.resize(300, 300)

    def page_MCTDH_select_init(self):
        '''
        switch QStackedWidget to page_MCTDH_select, and initialize it
        '''
        #switch QStackedWidget to page_MCTDH_select
        self.stackedWidget.setCurrentIndex(2)
        #hide menubar
        self.menuBar().hide()
        #resize window
        self.resize(300, 300)

    def page_main_init(self):
        '''
        switch QStackedWidget to page_main, and initialize it
        '''
        #uncheck all include box
        self.run_inc.setCheckState(0)
        self.op_inc.setCheckState(0)
        self.dir_inc.setCheckState(0)
        self.spf_inc.setCheckState(0)
        self.ml_inc.setCheckState(0)
        self.spdo_inc.setCheckState(0)
        self.geom_inc.setCheckState(0)
        self.prim_inc.setCheckState(0)
        self.wf_inc.setCheckState(0)
        self.int_inc.setCheckState(0)
        #default check RUN include box
        if self.directRunCBox.isChecked() or self.MCTDHRunCBox.isChecked():
            self.run_inc.setCheckState(2)
        #hide all tabs
        tab_num = self.maintab.count()
        for tab_index in reversed(range(tab_num)):
            self.maintab.removeTab(tab_index)
        #add neccessary tabs
        for tab_index in reversed(range(self.main_tab_num)):
            if self.main_tab_texts[tab_index] in self.include_tabs:
                self.maintab.addTab(self.main_tabs[tab_index], self.main_tab_texts[tab_index])
        #switch QStackedWidget to page_main
        self.stackedWidget.setCurrentIndex(3)
        #recover geometry
        self.resize(self.main_geometry.width(), self.main_geometry.height())
        #show menu_bar
        self.menuBar().show()

    def chk_dyn(self, number):
        '''
        checking where dynamic stuff is lost
        '''
                #check which controls are getting dynamic variables set
        print(number)
        for ctl in self.run_control:
            print("Run")
            print(ctl.property('quantp'))
        for ctl in self.op_control:
            print("Op")
            print(ctl.property('quantp'))
        for ctl in self.dir_control:
            print("dir")
            print(ctl.property('quantp'))


    def find_tab_info(self):
        '''
        Get useful info from the tab pages
        '''
        self.tabs = self.findChild(QtWidgets.QTabWidget,'maintab')
        ntabs = self.tabs.count()
        self.sections = {}
        #get the tab info for automation
        for page in range(ntabs):
            info = {}
            #info['tabname'] = self.tabs.tabText(page)
            tabname = self.tabs.tabText(page)
            info['tabindex'] = page
            info['secname'] =self.tabs.widget(page).property('secname')
            info['function'] = self.tabs.widget(page).property('func')
            info['ctl_list'] = self.tabs.widget(page).property('ctl_list')
            info['sec_chk'] = self.tabs.widget(page).property('sec_chk')
            info['sec_str'] = self.tabs.widget(page).property('sec_str')
            info['sec_sta'] = info['sec_str'] + "-SECTION"
            info['sec_end'] = "END-" + info['sec_str'] + "-SECTION"

            self.sections[tabname]= info


    def find_run_cntrls(self):
        '''
        find and link to controls on run tab
        '''
        #make control list for runtab
        self.run_inc = self.findChild(QtWidgets.QCheckBox,'run_inc')
        self.run_control =  []
        #text boxes under run tab
        self.run_control.append(self.findChild(QtWidgets.QPlainTextEdit,'name_txt'))
        self.run_control.append(self.findChild(QtWidgets.QPlainTextEdit,'tit_txt'))

        #Find double spin boxs
        self.run_control.append(self.findChild(QtWidgets.QDoubleSpinBox,'tinit_inp'))
        self.run_control.append(self.findChild(QtWidgets.QDoubleSpinBox,'tfin_inp'))
        self.run_control.append(self.findChild(QtWidgets.QDoubleSpinBox,'tout_inp'))
        self.run_control.append(self.findChild(QtWidgets.QDoubleSpinBox,'tpsi_inp'))

        #Find radio buttons
        self.run_control.append(self.findChild(QtWidgets.QRadioButton,'prop_rad'))
        self.run_control.append(self.findChild(QtWidgets.QRadioButton,'cont_rad'))

        #Find free text box
        self.run_control.append(self.findChild(QtWidgets.QTextEdit,'run_free_text'))

        #Find time box
        self.run_control.append(self.findChild(QtWidgets.QTimeEdit,'tstop_tim'))

        #Find check boxes
        self.run_control.append(self.findChild(QtWidgets.QCheckBox,'run_ovr_chk'))



        #Find Radio box
        self.run_control.append(self.findChild(QtWidgets.QRadioButton,'wav_run_rad'))
        self.run_control.append(self.findChild(QtWidgets.QRadioButton,'den1_run_rad'))
        self.run_control.append(self.findChild(QtWidgets.QRadioButton,'den2_run_rad'))

        self.run_control.append(self.findChild(QtWidgets.QRadioButton,'gendvr_chk'))
        self.run_control.append(self.findChild(QtWidgets.QRadioButton,'genoper_chk'))
        self.run_control.append(self.findChild(QtWidgets.QRadioButton,'genpes_chk'))
        self.run_control.append(self.findChild(QtWidgets.QRadioButton,'geninwf_chk'))
        self.run_control.append(self.findChild(QtWidgets.QRadioButton,'prop_rad'))
        self.run_control.append(self.findChild(QtWidgets.QRadioButton,'cont_rad'))
        self.run_control.append(self.findChild(QtWidgets.QRadioButton,'test_rad'))
        self.run_control.append(self.findChild(QtWidgets.QRadioButton,'rel_rad'))

        #Find unique ctrls
        self.run_control.append(self.findChild(QtWidgets.QGroupBox, 'runFileGBox'))

    def find_op_cntrls(self):
        '''
        find and link to controls on operator tab
        '''
        self.op_inc = self.findChild(QtWidgets.QCheckBox,'op_inc')

        self.op_control =  []
         #text boxes under run tab
        self.op_control.append(self.findChild(QtWidgets.QPlainTextEdit,'opname_txt'))
        self.op_control.append(self.findChild(QtWidgets.QPlainTextEdit,'op_path_txt'))
        self.op_control.append(self.findChild(QtWidgets.QPlainTextEdit,'opparfile_text'))
        self.op_control.append(self.findChild(QtWidgets.QPlainTextEdit,'opspline_txt'))
        #Find free text box
        self.op_control.append(self.findChild(QtWidgets.QTextEdit,'op_free_text'))


    def find_dir_cntrls(self):
        '''
        find and link to controls on dir tab
        '''
        self.dir_inc = self.findChild(QtWidgets.QCheckBox,'dir_inc')

        self.dir_control =  []
        #text boxes under dir tab
        self.dir_control.append(self.findChild(QtWidgets.QPlainTextEdit,'dir_sub_txt'))
        self.dir_control.append(self.findChild(QtWidgets.QPlainTextEdit,'dir_data_txt'))

        #Find double spin boxs
        self.dir_control.append(self.findChild(QtWidgets.QDoubleSpinBox,'dir_er0_inp'))
        self.dir_control.append(self.findChild(QtWidgets.QDoubleSpinBox,'dir_nbasis_inp'))

        #find combo box
        self.dir_control.append(self.findChild(QtWidgets.QComboBox,'dir_qc_comb'))
        self.dir_control.append(self.findChild(QtWidgets.QComboBox,'dir_ab_comb'))
        self.dir_control.append(self.findChild(QtWidgets.QComboBox,'dir_db_comb'))

        #find check box
        self.dir_control.append(self.findChild(QtWidgets.QCheckBox,'dir_ascii_chk'))

        self.dir_control.append(self.findChild(QtWidgets.QTextEdit,'dir_free_text'))

    def find_spf_cntrls(self):
        '''
        find and link to controls on SPF-Basis tab
        '''
        self.spf_inc = self.findChild(QtWidgets.QCheckBox,'spf_inc')

        self.spf_control =  []

        self.spf_control.append(self.findChild(QtWidgets.QGroupBox,'spfSetGbox'))
        self.spf_control.append(self.findChild(QtWidgets.QSpinBox,'spfNuclSBox'))
        self.spf_control.append(self.findChild(QtWidgets.QTextEdit,'spf_free_text'))

    def find_ml_cntrls(self):
        '''
        find and link to controls on ML-Basis tab
        '''
        self.ml_inc = self.findChild(QtWidgets.QCheckBox,'ml_inc')

        self.ml_control =  []

        self.ml_control.append(self.findChild(QtWidgets.QTextEdit,'ml_free_text'))

    def find_spdo_cntrls(self):
        '''
        find and link to controls on ML-Basis tab
        '''
        self.spdo_inc = self.findChild(QtWidgets.QCheckBox,'spdo_inc')

        self.spdo_control =  []

        self.spdo_control.append(self.findChild(QtWidgets.QGroupBox,'spdoSetGbox'))
        self.spdo_control.append(self.findChild(QtWidgets.QSpinBox,'spdoNuclSBox'))
        self.spdo_control.append(self.findChild(QtWidgets.QTextEdit,'spdo_free_text'))

    def find_geom_cntrls(self):
        '''
        find and link to controls on ML-Basis tab
        '''
        self.geom_inc = self.findChild(QtWidgets.QCheckBox,'geom_inc')

        self.geom_control =  []

        self.geom_control.append(self.findChild(QtWidgets.QTextEdit,'geom_free_text'))

    def find_prim_cntrls(self):
        '''
        find and link to controls on ML-Basis tab
        '''
        self.prim_inc = self.findChild(QtWidgets.QCheckBox,'prim_inc')

        self.prim_control =  []

        self.prim_control.append(self.findChild(QtWidgets.QSpinBox,'primElecSBox'))
        self.prim_control.append(self.findChild(QtWidgets.QSpinBox,'primNuclSBox'))
        self.prim_control.append(self.findChild(QtWidgets.QTextEdit,'prim_free_text'))

    def find_wf_cntrls(self):
        '''
        find and link to controls on ML-Basis tab
        '''
        self.wf_inc = self.findChild(QtWidgets.QCheckBox,'wf_inc')

        self.wf_control =  []

        self.wf_control.append(self.findChild(QtWidgets.QGroupBox,'wfModeGbox'))
        self.wf_control.append(self.findChild(QtWidgets.QTextEdit,'wf_free_text'))

    def find_int_cntrls(self):
        '''
        find and link to controls on ML-Basis tab
        '''
        self.int_inc = self.findChild(QtWidgets.QCheckBox,'int_inc')

        self.int_control =  []

        self.int_control.append(self.findChild(QtWidgets.QTextEdit,'int_free_text'))

    def find_inp_cntrls(self):
        '''
        get controls in input tab
        '''
        self.genfile_but = self.findChild(QtWidgets.QPushButton,'genfile_but')

        self.file_txt = self.findChild(QtWidgets.QTextEdit,'file_text')

        self.info_txt = self.findChild(QtWidgets.QTextBrowser,'info_txt')

    def level_cntrls(self):
        '''
        find the level controls and related controls for relaxation etc...
        '''
        self.levels = {}
        self.levels["lev1_rad"] = self.findChild(QtWidgets.QRadioButton,'lev1_rad')
        self.levels["lev2_rad"] = self.findChild(QtWidgets.QRadioButton,'lev2_rad')
        self.levels["lev3_rad"] = self.findChild(QtWidgets.QRadioButton,'lev3_rad')
        self.levels["lev4_rad"] = self.findChild(QtWidgets.QRadioButton,'lev4_rad')

        # self.levels["lev1_rad"].clicked.connect(lambda:self.set_prop())
        # self.levels["lev2_rad"].clicked.connect(lambda:self.set_prop())
        # self.levels["lev3_rad"].clicked.connect(lambda:self.set_prop())
        # self.levels["lev4_rad"].clicked.connect(lambda:self.set_prop())
        self.levels["lev1_rad"].clicked.connect(lambda:gui_logic.set_prop(self))
        self.levels["lev2_rad"].clicked.connect(lambda:gui_logic.set_prop(self))
        self.levels["lev3_rad"].clicked.connect(lambda:gui_logic.set_prop(self))
        self.levels["lev4_rad"].clicked.connect(lambda:gui_logic.set_prop(self))
        #level 1 options
        self.levels["gendvr_chk"] = self.findChild(QtWidgets.QRadioButton,'gendvr_chk')
        #level 2 options
        self.levels["genoper_chk"] = self.findChild(QtWidgets.QRadioButton,'genoper_chk')
        self.levels["genpes_chk"] = self.findChild(QtWidgets.QRadioButton,'genpes_chk')
        #level 3 options
        self.levels["geninwf_chk"] = self.findChild(QtWidgets.QRadioButton,'geninwf_chk')
        #level 4 options
        self.levels["prop_rad"] = self.findChild(QtWidgets.QRadioButton,'prop_rad')
        self.levels["cont_rad"] = self.findChild(QtWidgets.QRadioButton,'cont_rad')
        self.levels["test_rad"] = self.findChild(QtWidgets.QRadioButton,'test_rad')
        self.levels["rel_rad"] = self.findChild(QtWidgets.QRadioButton,'rel_rad')

    def set_sect_cntrls(self,
                        quant_inp: mctdhinp.MctdhInput,
                        sec_name, control_list,
                        use_chk: QtWidgets.QCheckBox):
        '''
        search through input file and find parameters to set in the section
        needs section name in input file
        list of controls related to that section
        If new control type is added then the if statement needs to be extended
        '''

        if sec_name in quant_inp.sections:
            use_chk.setChecked(True)
            sec = quant_inp.sections[sec_name]
            for ctl in control_list:
                if quant_inp.sections[sec_name][ctl.property('quantp')] is not None:
                    if (isinstance(ctl,QtWidgets.QPlainTextEdit)
                        or isinstance(ctl,QtWidgets.QTextEdit)):
                        ctl.setPlainText(quant_inp.sections[sec_name][ctl.property('quantp')])
                    elif isinstance(ctl,QtWidgets.QDoubleSpinBox):
                        ctl.setValue(float(quant_inp.sections[sec_name][ctl.property('quantp')]))
                    elif isinstance(ctl,QtWidgets.QComboBox):
                        self.set_combobox(quant_inp,sec_name,ctl.property('quantp'),ctl)
                    elif (isinstance(ctl,QtWidgets.QCheckBox)
                        or isinstance(ctl,QtWidgets.QRadioButton)):
                        ctl.setChecked(quant_inp.sections[sec_name][ctl.property('quantp')])
                    elif isinstance(ctl,QtWidgets.QTimeEdit):
                        ctl.setTime(quant_inp.sections[sec_name][ctl.property('quantp')])
                else:
                    if ctl.property('quantp') == 'free':
                        #print out the free text box
                        for thing in sec.free:
                            for thingy in thing:
                                ctl.append(thingy)
        else:
            use_chk.setChecked(False)

    def get_sec_cntrls(self,
                        quant_out: mctdhinp.MctdhInput,
                        sec_name,
                        sec_text,
                        control_list,
                        use_chk: QtWidgets.QCheckBox):
        '''
        search through the controls in each tab and put them into input structure
        '''

        if use_chk.isChecked() is True:
            #create the section
            sec = mctdhinp.MctdhSection(sec_text[0],sec_text[1])
            #sec = mctdhinp.MctdhSection('RUN-SECTION','END-RUN-SECTION')
            quant_out.addsection(sec_name,sec)
            for ctl in control_list:
                if ctl.property('quantp') == "unique":
                    sec.setunique(getattr(self, ctl.property('unique_str')))
                elif (isinstance(ctl,QtWidgets.QPlainTextEdit)
                    or isinstance(ctl,QtWidgets.QTextEdit)):
                    if ctl.toPlainText() == "":
                        continue
                    if ctl.property('quantp') == "free":
                        sec.adddataitem(ctl.toPlainText())
                    else:
                        sec.setparam(ctl.property('quantp'),ctl.toPlainText())
                elif isinstance(ctl,QtWidgets.QDoubleSpinBox):
                    sec.setparam(ctl.property('quantp'),ctl.value())
                elif isinstance(ctl,QtWidgets.QComboBox):
                    sec.setparam(ctl.property('quantp'),ctl.currentText())
                elif (isinstance(ctl,QtWidgets.QCheckBox)
                        or isinstance(ctl,QtWidgets.QRadioButton)):
                    if ctl.isChecked():
                        #only output if actually checked
                        sec.setflag(ctl.property('quantp'))
                elif isinstance(ctl,QtWidgets.QTimeEdit):
                    sec.setparam(ctl.property('quantp'),ctl.time())
            quant_out.addsection(sec_name,sec)

    def menu_actions(self):
        '''
        function to connect all the menu actions
        '''
        #generate file text
        self.actionGenerate_Input.triggered.connect(self.gen_inp_file)
        #set file open action
        self.actionOpen_File.triggered.connect(self.get_inp_file)
        #set file save action
        self.actionSave_File.triggered.connect(self.get_sav_file)
        #close window
        self.actionExit.triggered.connect(self.close)


    def butt_actions(self):
        '''
        function to connect buttons to actions
        '''
        self.genfile_but.clicked.connect(self.gen_inp_file)
        self.kindStartBtn.clicked.connect(self.kind_start)
        self.directStartBtn.clicked.connect(self.direct_start)
        self.MCTDHStartBtn.clicked.connect(self.MCTDH_start)
        self.prePageBtn.clicked.connect(self.previous_page_clicked)

        self.spfNuclSBox.valueChanged.connect(self.spf_nuclear_layout_updata)
        self.spfDefaultRBtn.clicked.connect(self.spf_nuclear_layout_updata)
        self.spfCustomRbtn.clicked.connect(self.spf_nuclear_layout_updata)
        self.spfCustomEdit.textChanged.connect(self.spf_nuclear_layout_updata)
        self.spdoNuclSBox.valueChanged.connect(self.spdo_nuclear_layout_updata)
        self.spdoDefaultRBtn.clicked.connect(self.spdo_nuclear_layout_updata)
        self.spdoCustomRbtn.clicked.connect(self.spdo_nuclear_layout_updata)
        self.spdoCustomEdit.textChanged.connect(self.spdo_nuclear_layout_updata)
        self.wfReadFileRBtn.clicked.connect(self.wf_stackedwidget_updata)
        self.wfBuildRBtn.clicked.connect(self.wf_stackedwidget_updata)
        self.name_txt.textChanged.connect(self.run_name_updata)
        self.basisCbox.stateChanged.connect(self.MCTDH_basisCbox_changed)

    def get_inp_file(self):
        '''
        function to show file dialog and select input file
        '''
        #get the filename via a dialog
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file',
                                    os.getcwd(),"Quantics Input files (*.inp)")

        #now load it/ unless cancelled
        if filename[0] != "":
            self.load_inp_file(filename[0])
        else:
            print("File load cancelled")
            self.info_txt.append("File load cancelled")
        return filename

    def load_inp_file(self, filename):
        '''
        load the values from the file path
        '''
        #filename = parser.f
        #make sure have absolute path
        filename = os.path.abspath(filename)
        #check it exists
        if os.path.exists(filename):
            quant_inp = mctdhinp.MctdhInput(filename)
            self.file_txt.clear()
            self.file_txt.append(f"#Loaded from {filename}")
            self.file_txt.append(str(quant_inp))
            #now load values into controls
            if quant_inp is not None:
                print("File Loaded")
                self.info_txt.append("File Loaded")
                for tab in self.sections:
                    if tab != 'Input File':
                        self.set_sect_cntrls(quant_inp,
                                            self.sections[tab]['secname'],
                                            getattr(self,self.sections[tab]['ctl_list']),
                                            getattr(self,self.sections[tab]['sec_chk']))
                #set run values
                # self.set_sect_cntrls(quant_inp,'runsection',self.run_control,self.run_inc)
                # #call for operator
                # self.set_sect_cntrls(quant_inp,'opersection',self.op_control,self.op_inc)
                # #call for dynamics
                # self.set_sect_cntrls(quant_inp,"dirdynsection",self.dir_control,self.dir_inc)
                print("Values set")
                self.info_txt.append("Values set")

        else:
            #turn into proper logged error
            print("File does not exist")
            self.info_txt.append("File does not exist")

    def gen_inp_file(self):
        '''
        Go over controls and generate input file text
        '''
        print("Generating new input text")
        self.info_txt.append("Generating new input text")
        #updata unique strings
        self.uniques_updata()
        #create new MCTDH inp object without filename, so empty
        quant_out = mctdhinp.MctdhInput()
        for tab in self.sections:
            if tab != 'Input File':
                self.get_sec_cntrls(quant_out,self.sections[tab]['secname'],
                                    [self.sections[tab]['sec_sta'],
                                    self.sections[tab]['sec_end']],
                                    getattr(self,self.sections[tab]['ctl_list']),
                                    getattr(self,self.sections[tab]['sec_chk']))

        #clear current text
        self.file_txt.clear()
        self.file_txt.append(str(quant_out))

    def get_sav_file(self):
        '''
        function to show file dialog and save new file
        '''
                #get the filename via a dialog
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Open file',
                                    os.getcwd(),"Quantics Input files (*.inp)")

        #now saveit/ unless cancelled
        if filename[0] != "":
            print("File name choosen")
            self.info_txt.append("File name choosen")
            with open(filename[0], 'w') as writer:
                writer.write(self.file_txt.toPlainText())
        else:
            print("File load cancelled")
            self.info_txt.append("File load cancelled")
        return filename

    def set_combobox(self, quant_inp, sec_name, parameter, combo):
        '''
        set value of combobox
        '''

        qc_items = [ combo.itemText(i) for i in range( combo.count())]
        if quant_inp.sections[sec_name][parameter] in qc_items:
            combo.setCurrentText(quant_inp.sections[sec_name][parameter])
        else:
            combo.additems(quant_inp.sections[sec_name][parameter])

    def set_prop(self):
        '''
        Control which options are allowed when propagation level options get set
        '''
        if self.levels["lev1_rad"].isChecked():
            #only level 1 control can be checked
            #set level 1
            self.levels["gendvr_chk"].setCheckable(True)
            #blank level 2
            self.levels["genoper_chk"].setChecked(False)
            self.levels["genpes_chk"].setChecked(False)

            self.levels["genoper_chk"].setCheckable(False)
            self.levels["genpes_chk"].setCheckable(False)

            #blank level 3
            self.levels["geninwf_chk"].setChecked(False)

            self.levels["geninwf_chk"].setCheckable(False)
            #blank level 4

            self.levels["prop_rad"].setCheckable(False)
            self.levels["cont_rad"].setCheckable(False)
            self.levels["test_rad"].setCheckable(False)
            self.levels["rel_rad"].setCheckable(False)

            self.levels["prop_rad"].setChecked(False)
            self.levels["cont_rad"].setChecked(False)
            self.levels["test_rad"].setChecked(False)
            self.levels["rel_rad"].setChecked(False)

            self.update()
            # self.levels["lev2_rad"].setChecked(False)
            # self.levels["lev3_rad"].setChecked(False)
            # self.levels["lev4_rad"].setChecked(False)

        elif self.levels["lev2_rad"].isChecked():
        #     #only level 2 controls checked
            #only level 1 control can be checked
            #set level 1
            self.levels["gendvr_chk"].setCheckable(False)
            #blank level 2
            self.levels["genoper_chk"].setChecked(False)
            self.levels["genpes_chk"].setChecked(False)

            self.levels["genoper_chk"].setCheckable(True)
            self.levels["genpes_chk"].setCheckable(True)

            #blank level 3
            self.levels["geninwf_chk"].setChecked(False)

            self.levels["geninwf_chk"].setCheckable(False)
            #blank level 4
            self.levels["prop_rad"].setChecked(False)
            self.levels["cont_rad"].setChecked(False)
            self.levels["test_rad"].setChecked(False)
            self.levels["rel_rad"].setChecked(False)

            self.levels["prop_rad"].setCheckable(False)
            self.levels["cont_rad"].setCheckable(False)
            self.levels["test_rad"].setCheckable(False)
            self.levels["rel_rad"].setCheckable(False)

            self.update()
        elif self.levels["lev3_rad"].isChecked():
        #     #only level 3 controls checked
            #only level 1 control can be checked
            #set level 1
            self.levels["gendvr_chk"].setCheckable(False)
            #blank level 2
            self.levels["genoper_chk"].setChecked(False)
            self.levels["genpes_chk"].setChecked(False)

            self.levels["genoper_chk"].setCheckable(False)
            self.levels["genpes_chk"].setCheckable(False)

            #blank level 3
            self.levels["geninwf_chk"].setChecked(False)

            self.levels["geninwf_chk"].setCheckable(True)
            #blank level 4
            self.levels["prop_rad"].setChecked(False)
            self.levels["cont_rad"].setChecked(False)
            self.levels["test_rad"].setChecked(False)
            self.levels["rel_rad"].setChecked(False)

            self.levels["prop_rad"].setCheckable(False)
            self.levels["cont_rad"].setCheckable(False)
            self.levels["test_rad"].setCheckable(False)
            self.levels["rel_rad"].setCheckable(False)

            self.update()

        elif self.levels["lev4_rad"].isChecked():
        #     #only level 4 controls checked
            #only level 1 control can be checked
            #set level 1
            self.levels["gendvr_chk"].setCheckable(False)
            #blank level 2
            self.levels["genoper_chk"].setChecked(False)
            self.levels["genpes_chk"].setChecked(False)

            self.levels["genoper_chk"].setCheckable(False)
            self.levels["genpes_chk"].setCheckable(False)

            #blank level 3
            self.levels["geninwf_chk"].setChecked(False)

            self.levels["geninwf_chk"].setCheckable(False)
            #blank level 4
            self.levels["prop_rad"].setChecked(False)
            self.levels["cont_rad"].setChecked(False)
            self.levels["test_rad"].setChecked(False)
            self.levels["rel_rad"].setChecked(False)

            self.levels["prop_rad"].setCheckable(True)
            self.levels["cont_rad"].setCheckable(True)
            self.levels["test_rad"].setCheckable(True)
            self.levels["rel_rad"].setCheckable(True)

            self.update()
    # def closeEvent(self, event):
    #     '''
    #     stuff to do when window is closed
    #     '''
    #     event.accept()
    #     #return super().closeEvent(a0)
