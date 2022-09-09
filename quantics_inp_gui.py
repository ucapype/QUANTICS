'''
Gui to create quantics input files

'''
#Imports
import sys  #for command line arguments to pass to qt

#unused imports
#import os   #for file handling things
#import MCTDH_.mctdhinp as mctdhinp  #quantics file reading functions

import gui_parsers.gui_parse #cli arguments
import ui.gui_lib as gui_lib    #gui interface


#import gui_lib  #library of functions

if __name__ == '__main__':
        #get any command line arguments and set variables
    parser = gui_parsers.gui_parse.parsing()
    parsed_args, unparsed_args = parser.parse_known_args()

    # Create the Qt Application
    # QApplication expects the first argument to be the program name.
    qt_args = sys.argv[:1] + unparsed_args

    app = gui_lib.QtWidgets.QApplication(qt_args)

    # Create and show the form
    window = gui_lib.Ui(parsed_args)
    #window.load_cl_arg(parsed_args)
    #Run the main Qt loop
    sys.exit(app.exec_())
