##module quantic gui library
'''
python library for quantics
'''
import argparse #import for parsing of command line options
import os   #for file stuff
from PyQt5 import QtWidgets, uic, QtCore

# from PyQt5.uic.uiparser import QtCore
# from PyQt5.QtGui import Qt    #QT functions for GUI
#
# import simp #the quantics analyse wrapper

# class parsy():
#     '''
#     class for the parsing stuff
#     '''
def parsing():
    '''
    Function create the cmd line argument parsing
    returns the parsing function
    would make sense to go in its own library separate to gui things
    '''

    #the - means optional argument, no dash means must be given and error is raised if not
    parse = argparse.ArgumentParser(description='Purpose: \
                                    Enables 2D plotting of the wavefunction or PES.')
    parse.add_argument('-i',
                        metavar='DIR',
                        type=str,
                        default='./',
                        #fortran showsys variable = name
                        help='data is stored in directory DIR')
    parse.add_argument('-f',
                        metavar='FILE',
                        type=str,
                        default =' ',
                        #fortran showsys variable = psifile
                        help='the wavefunction is read FILE rather than from ./psi. \
                            The string FILE may be a relative or a full path-name ')
    parse.add_argument('-n',
                        metavar='NUM',
                        type=int,
                        default=999999,
                        #fortran showsys variable = ncut
                        help='only the first num WFs are read from psi-file.')
    parse.add_argument('-skip',
                        metavar='SKIP',
                        type=int,
                        default=0,
                        #fortran showsys variable = nskip
                        help='the first m WFs are skipped.')
    parse.add_argument('-p',
                        metavar='FILE',
                        type=str,
                        default=' ',
                        #fortran showsys variable = operfile,
                        help='the PES is read from FILE rather than from ./oper \
                            The string FILE may be a relative or a full path-name.')
    parse.add_argument('-o',
                        metavar='oFILE',
                        type=str,
                        default='surface',
                        #fortran showsys variable = fileout
                        help='The ouput is written to file FILE.pl rather than to ./surface.pl \
                            The string FILE may be a relative or a full path-name.')
    parse.add_argument('-D',
                        metavar='DIR',
                        type=str,
                        #fortran showsys variable = dirout
                        #needs to be converted into abs path
                        #no default defined in showsys so use CWD
                        default=os.path.curdir,
                        help='The output is written to directory DIR. \
                            This is useful, \
                            if one has no right to write to the name directory. \
                            The directory DIR must exist. \
                            The string DIR may be a relative or a full path-name.')
    parse.add_argument('-pes',
                        metavar='PES',
                        type=bool,
                        default=True,
                        #fortran showsys variable = lshowpsi
                        #ncut = 1 in showsys
                        help='only the OPER file is read, i.e. no wavefunction plotting.')
    parse.add_argument('-nopes',
                        metavar='NOPES',
                        type=bool,
                        default=False,
                        #fortran showsys variable = lnopes
                        help='the OPER file is not read, no potential plotting, no dia->ad trafo.')
    parse.add_argument('-ddraw',
                        metavar='DDRAW',
                        type=bool,
                        default=False,
                        #fortran showsys variable = lshowpsi
                        #ncut not changed in showsys
                        #lrediab = .false. in showsys
                        help='the raw adiabatic PES from a DD,calculation is plotted.')
    parse.add_argument('-rst',
                        metavar='RST',
                        type=bool,
                        default=True,
                        #fortran showsys variable = lshowrst
                        #ncut = 1 in showsys
                        help='the restart file is read, rather than the psi file.')
    parse.add_argument('-step',
                        metavar='STEP',
                        type=int,
                        #fortran showsys variable = step
                        default=1, #set to 1 in adefault.f90
                        help='only every step''s WF will be processed.')
    parse.add_argument('-nw',
                        metavar='NW',
                        type=bool,
                        default=False, #not set in showsys
                        #fortran showsys variable = lnw
                        help='No weights are employed. \
                        Plot the "naked" DVR populations. (WF only).')
    parse.add_argument('-nofs',
                        metavar='FS',
                        type=float,
                        default = 1.0,
                        #fortran showsys variable = fs
                        #no default set in showsys
                        help='No transformation to fs. Use when time-not-fs was set in mctdh.')
    parse.add_argument('-u',
                        metavar='UNITS',
                        type=str,
                        default='ev',
                        #fortran shows sys variable = zaxunitlab
                        #sets zaxunit value to 1, does odd things lines 1163 of showsys
                        help='The energy unit UNIT is applied. (default for pes: eV).\
                            NOT FULLY IMPLEMENTED')
    parse.add_argument('-pop2',
                        metavar='POP2',
                        type=bool,
                        default = False,
                        #fortran showsys variable = lpop2
                        #sets lnw to true
                        help='the basis set occupations are plotted rather than grid \
                        populations. For FFT this implies momentum \
                        space representation. Note: -pop2 sets -nw.')
    parse.add_argument('-pop2all',
                        metavar='POP2ALL',
                        type=bool,
                        default = False,
                        #fortran showsys variable = lpop2all
                        #sets lnw and pop2 to true
                        help='Similar to -pop2, but now all DOFs \
                             are transformed to second population. \
                        This is only useful for cuts. Note: -pop2all sets -pop2 and -nw.')
    parse.add_argument('-plgrd',
                        metavar='MAXPLGRID',
                        type=int,
                        default = 8001, #in plot
                        #fortran showsys variable = maxplgrid
                        #no default is set
                        help='The maximum number of points for a grid.')
    parse.add_argument('-DB',
                        metavar='DBPATH',
                        type=str,
                        default=' ',
                        #fortran showsys variable = ddpath
                        #default is ' ' in global.f90
                        help='The path to a direct dynamics DB.')
    parse.add_argument('-DBG',
                        metavar='DBGPATH',
                        type=str,
                        default=' ',
                        #fortran showsys variable = ddpath
                        #default is ' ' in global.f90
                        #sets lgausspot to true
                        help='The path to a direct dynamics DB.')
    parse.add_argument('-shepord',
                        metavar='I',
                        type=int,
                        default=24,
                        #fortran showsys variable = dbinterord
                        #default set in dirdyn.f90
                        help='Order I will be used for the Shephard interpolation. \
                            NOT FULLY IMPLEMENTED')
    parse.add_argument('-shepard',
                        metavar='I',
                        type=int,
                        default=24,
                        #fortran showsys variable = dbinterord
                        #default set in dirdyn.f90
                        help='Order I will be used for the Shephard interpolation.\
                            NOT FULLY IMPLEMENTED')
    parse.add_argument('-ddlocal',
                        metavar='DDLOCAL',
                        type=bool,
                        default = True,
                        #fortran showsys variable = ldblocal
                        help='The local rather than interpolated energy is plotted.')
    # parse.add_argument('-ver',
    #                     #action=version,
    #                     version='XX YY',
    #                     help='Version information about the program.')

    return parse
def empty_string_list(length, depth):
    '''
    creates an emptry string of spaces
    '''
    mystr = ""
    for x in range(length):
        mystr = mystr + " "
    
    mylist = []
    for x in range(depth):
        mylist.append(mylist)
    
    return mylist

def pad_string_list(string_sec,length):
    '''
    Function takes python string and pads it out to match length in fortran
    string_sec is string to pad out
    length is length to match to
    '''
    if len(string_sec) < length:
        #lets pad
        for x in range(length-len(string_sec)):
            string_sec = string_sec + " "
    return string_sec



def set_inputs(parser):
    '''
    This function takes the parser and goes through to create a list of the variable values
    This is then passed over to simpsys to set variables
    '''
    #append file names and characters into string list
    #needs to be same size that fortran is expecting
    #so generate 'empty string list'
    size_fortran = 65   #this is the character size in gui_sys setinputs sub_routine
    #string_variables=empty_string_list(65,1)
    string_variables=[]
    #string_variables = np.empty((7, 65), dtype='c')
    string_variables.append(pad_string_list(parser.i,size_fortran))   #name
    string_variables.append(pad_string_list(parser.f,size_fortran))  #psifile
    string_variables.append(pad_string_list(parser.p,size_fortran))  #operfile
    string_variables.append(pad_string_list(parser.o + ".pl",size_fortran))   #fileout
    string_variables.append(pad_string_list(os.path.abspath(parser.D),size_fortran))  #dirout
    string_variables.append(pad_string_list(parser.u,size_fortran))  #zaxunitlab
    string_variables.append(pad_string_list(parser.DB,size_fortran)) #ddpath



    #append any integers into integer list
    int_variables=[]
    int_variables.append(parser.n)  #ncut
    int_variables.append(parser.skip) #nskip
    int_variables.append(parser.step)   #step
    for x in range(5):
        int_variables.append(0)

    #append any flags into boolean list
    flag_variables=[]
    flag_variables.append(parser.pes)   #set lshowpsi, if false ncut = 1
    if not parser.pes:
        int_variables[0] = 1    #lshowpsi false so ncut = 1
    flag_variables.append(parser.nopes) #lnopes
    flag_variables.append(parser.ddraw) #lrediab (if true lshowpsi is false)
    if parser.ddraw:
        flag_variables[0]=False
    flag_variables.append(parser.ddlocal) #ldblocal
    flag_variables.append(parser.rst)   #lshowrst (if true ncut = 1)
    if parser.rst:
        int_variables[0] = 1
    flag_variables.append(parser.nw)    #lnw
    flag_variables.append(parser.pop2) #lpop2 also lnw is true
    if parser.pop2:
        flag_variables[6] = True    #set lnw to true
    flag_variables.append(parser.pop2all)   #lpop2all, also lpop2 and lnw are trye
    if parser.pop2all:
        flag_variables[6] = True
        flag_variables[7] = True
    out = 0
    #set values from cmdline
    #print(simp.set_inputs(int_variables,100,flag_variables,string_variables,len(int_variables),len(flag_variables),len(string_variables)))
    #set up log file
    log_handle = open_log_file(os.getcwd(), False, "")


def open_log_file(name, laeoutd, dirout):
    '''
        open up showsys log file for writing to
        name is current directory to save to
        laeoutd is whether to use different directory to save to
        dirout is the name of different output directory

        returns log_handler as the file_handler for the log file
    '''
    
    if laeoutd:
        logname = os.path.join(dirout, "showsys.log")
    else:
        logname = os.path.join(name, "showsys.log")

    log_handle = open(logname,'w')

    return log_handle

def close_all_files(log_handle):
    '''
    closes the log file
    '''
    log_handle.close()

class Ui(QtWidgets.QMainWindow):
    '''
    Class to hold the gui info
    '''
    def __init__(self, parser):
        '''
        initialise class by loading the .ui file
        '''
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('showquant.ui', self) # Load the .ui file
        #uic.loadUi('/home/graham/quantics_gui/source/analyse/gui_files/ui/quant_inp_main.ui', self)
        #find controls
        #buttons
        self.run_button = self.findChild(QtWidgets.QPushButton, 'run_button') # Find the button

        #find text boxes
        self.info_txt = self.findChild(QtWidgets.QTextBrowser,'info_txt')

        #find spin box (number input)
        self.ncut_inp = self.findChild(QtWidgets.QSpinBox,'ncut')
        self.nskip_inp = self.findChild(QtWidgets.QSpinBox,'nskip')
        self.step_inp = self.findChild(QtWidgets.QSpinBox,'step')

        #find checkboxes
        self.lshowpsi = self.findChild(QtWidgets.QCheckBox,'lshowpsi')
        self.lnopes = self.findChild(QtWidgets.QCheckBox,'lnopes')
        self.lrediab = self.findChild(QtWidgets.QCheckBox,'lrediab')
        self.ldblocal = self.findChild(QtWidgets.QCheckBox,'ldblocal')
        self.lshowrst = self.findChild(QtWidgets.QCheckBox,'lshowrst')
        self.lnw = self.findChild(QtWidgets.QCheckBox,'lnw')
        self.lpop2 = self.findChild(QtWidgets.QCheckBox,'lpop2')
        self.lpop2all = self.findChild(QtWidgets.QCheckBox,'lpop2all')

        #find textboxes
        self.dir_path = self.findChild(QtWidgets.QPlainTextEdit,'dir_path')
        self.psi_path = self.findChild(QtWidgets.QPlainTextEdit,'psi_path')
        self.pes_path = self.findChild(QtWidgets.QPlainTextEdit,'pes_path')
        self.out_path = self.findChild(QtWidgets.QPlainTextEdit,'out_path')
        self.out_dir = self.findChild(QtWidgets.QPlainTextEdit,'out_dir')


        #set up actions and controls

        #run button is pressed
        self.run_button.clicked.connect(self.run_button_pressed)

        #logic changes
        self.lshowpsi.stateChanged.connect(self.showpsi_check)
        self.lrediab.stateChanged.connect(self.rediab_check)
        self.lshowrst.stateChanged.connect(self.showrst_check)
        self.lpop2.stateChanged.connect(self.pop2_check)
        self.lpop2all.stateChanged.connect(self.pop2all_check)

        #read in cli
        self.load_cl_arg(parser)
        #activate log file
        self.log_handle = open_log_file(os.getcwd(), False, "")

        self.set_output_texts("Running Analysis Programme")
        #self.set_text_info("Running Analysis Programme")

        #set up system with given options (either CLI or Default)
        self.set_output_texts("Loading options")

        self.set_gui_inputs()


        self.show() # Show the GUI

    #def closeEvent(self, a0: QtGui.QCloseEvent):
    def closeEvent(self, event):
        close_all_files(self.log_handle)
        event.accept()
        #return super().closeEvent(a0)

    def get_image_name(self):
        '''
        get the name of the image in the graph canvas
        '''

        return self.graph_canvas.pixmap()
    #ACTIONS are here

    def run_button_pressed(self):
        '''
        run button is pressed
        This should have the same effect as pressing the plot button in showsys
        '''

        self.set_output_texts("Run buton is pressed")
        self.ncut_inp.setValue(1)

        #set up variables from inputs


    #below are if certain options are changed - control allowed options in programme
    def showpsi_check(self, state):
        '''
        lshowpsi is checked so other options need flagging up
        if false ncut = 1
        '''
        if state != QtCore.Qt.Checked:
            self.ncut_inp.setValue(1)


    def showrst_check(self,state):
        '''
        lshowrst is checked so other options need flagging up
        if true ncut = 1
        '''
        if state == QtCore.Qt.Checked:
            self.ncut_inp.setValue(1)


    def rediab_check(self,state):
        '''
        lrediab is checked, if so showpsi must be off
        ncut though remains the same
        '''

        if state == QtCore.Qt.Checked:
            ntemp = self.ncut_inp.value()
            self.lshowpsi.setChecked(False)
            self.ncut_inp.setValue(ntemp)

    def pop2_check(self,state):
        '''
        lrediab is checked, if so showpsi must be off
        ncut though remains the same
        '''

        if state == QtCore.Qt.Checked:
            self.lnw.setChecked(True)

    def pop2all_check(self,state):
        '''
        lrediab is checked, if so showpsi must be off
        ncut though remains the same
        '''

        if state == QtCore.Qt.Checked:
            self.lpop2.setChecked(True)

    def load_cl_arg(self, parser):
        '''
        load the values from the command line
        '''
        #load strings
        self.dir_path.clear()
        self.dir_path.setPlainText(parser.i)    #name in gui_sys
        self.psi_path.clear()
        self.psi_path.setPlainText(parser.f)    #psifile
        self.pes_path.clear()
        self.pes_path.setPlainText(parser.p)    #operfile
        self.out_path.clear()
        self.out_path.setPlainText(parser.o)    #fileout
        self.out_dir.clear()
        self.out_dir.setPlainText(parser.D)     #dirout

        #load numbers
        self.ncut_inp.setValue(parser.n)    #ncut
        self.nskip_inp.setValue(parser.skip)    #nskip
        self.step_inp.setValue(parser.step) #step

        #load flags - and correct things when done
        self.lshowpsi.setChecked(parser.pes)  #lshowpsi
        self.lnopes.setChecked(parser.nopes)  #lnopes
        self.lrediab.setChecked(parser.ddraw)  #lrediab
        self.ldblocal.setChecked(parser.ddlocal) #ldblocal
        self.lshowrst.setChecked(parser.rst)   #lshowrst (if true ncut = 1)
        self.lnw.setChecked(parser.nw)    #lnw
        self.lpop2.setChecked(parser.pop2) #lpop2 also lnw is true
        self.lpop2all.setChecked(parser.pop2all)   #lpop2all, also lpop2 and lnw are trye

    #other functions
    def set_output_texts(self, text):
        '''
        Function takes text and sends it to text box in programme and log file
        '''
        self.set_text_info(text)
        self.set_text_log(self.log_handle,text)

    def set_text_info(self, info):
        '''
        Display given info string in text box
        '''
        self.info_txt.append(str(info))

    def set_text_log(self,log_handle,text):
        '''
        Send text to log file at log_handle
        Will write to new line
        '''
        log_handle.write("\n" + str(text) + "\n")


    def set_gui_inputs(self):
        '''
        This functions takes the variables defined in the gui and creates list of variables
        suitable to send to Fortran gui_sys
        '''
        #append file names and characters into string list
        #needs to be same size that fortran is expecting
        size_fortran = 200   #this is the character size in gui_sys setinputs sub_routine
        string_variables=[]
        #pad_string_list is a function that pads any string up to the required character number
        #this is defined by size_fortran
        #Before setting strings check what each file name is:

        if not self.lnopes.isChecked():
            if self.pes_path.toPlainText() == " ":
                operfile = "oper"
            else:
                operfile = self.pes_path.toPlainText()
            operfile =os.path.abspath(operfile)

        if self.lshowrst.isChecked():
            if self.psi_path.toPlainText() == " ":
                psifile = "restart"
            else:
                psifile = self.psi_path.toPlainText()
            psifile =os.path.abspath(psifile)
        elif self.lshowpsi.isChecked():
            if self.psi_path.toPlainText() == " ":
                psifile = "psi"
            else:
                psifile = self.psi_path.toPlainText()
            psifile =os.path.abspath(psifile)

        string_variables.append(pad_string_list(os.path.abspath(self.dir_path.toPlainText()),size_fortran))   #name
        string_variables.append(pad_string_list(psifile,size_fortran))  #psifile
        string_variables.append(pad_string_list(operfile,size_fortran))  #operfile
        string_variables.append(pad_string_list(os.path.abspath(self.out_path.toPlainText()) + ".pl",size_fortran))   #fileout
        string_variables.append(pad_string_list(os.path.abspath(self.out_dir.toPlainText()),size_fortran))  #dirout
        string_variables.append(pad_string_list("eV",size_fortran))  #zaxunitlab -NEEDS FIXING
        string_variables.append(pad_string_list(self.dir_path.toPlainText(),size_fortran)) #ddpath -NEEDS FIXING
        self.set_output_texts(string_variables)
        self.set_output_texts("Using following options for gui_sys")
        #self.set_output_texts(string_variables)

        #append any integers into integer list
        int_variables=[]
        int_variables.append(int(self.ncut_inp.value()))  #ncut
        int_variables.append(int(self.nskip_inp.value())) #nskip
        int_variables.append(int(self.step_inp.value()))   #step
        for x in range(5):
            int_variables.append(0)
        
        #self.set_output_texts(str(int_variables))
        #append any flags into boolean list
        #do logic checks, done earlier but enforce here too
        flag_variables=[]
        flag_variables.append(self.lshowpsi.isChecked())   #set lshowpsi, if false ncut = 1
        if not self.lshowpsi.isChecked():
            int_variables[0] = 1    #lshowpsi false so ncut = 1
        flag_variables.append(self.lnopes.isChecked()) #lnopes
        flag_variables.append(self.lrediab.isChecked()) #lrediab (if true lshowpsi is false)
        if self.lrediab.isChecked():
            flag_variables[0]=False
        flag_variables.append(self.ldblocal.isChecked()) #ldblocal
        flag_variables.append(self.lshowrst.isChecked())   #lshowrst (if true ncut = 1)
        if self.lshowrst.isChecked():
            int_variables[0] = 1
        flag_variables.append(self.lnw.isChecked())    #lnw
        flag_variables.append(self.lpop2.isChecked()) #lpop2 also lnw is true
        if self.lpop2.isChecked():
            flag_variables[6] = True    #set lnw to true
        flag_variables.append(self.lpop2all.isChecked())   #lpop2all, also lpop2 and lnw are trye
        if self.lpop2all.isChecked():
            flag_variables[6] = True
            flag_variables[7] = True
        #out = 0
        #set values from cmdline
        #self.set_output_texts(simp.set_inputs(int_variables,100,flag_variables,string_variables,len(int_variables),len(flag_variables),len(string_variables)))
        #self.set_output_texts(simp.set_inputs(int_variables,100,flag_variables,string_variables,len(int_variables),len(flag_variables),len(string_variables)))
        #after this now ready to run plotsys
