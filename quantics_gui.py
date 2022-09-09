'''
Python gui to link to quantics analysis codes

'''
import sys  #for command line arguments to pass to qt

import gui_lib  #library of functions


if __name__ == '__main__':

    #get any command line arguments and set variables
    parser = gui_lib.parsing()
    parsed_args, unparsed_args = parser.parse_known_args()
    #pass arugments on to gui_sys and set defaults/set it all up
    #gui_lib.set_inputs(parsed_args)
    #test = ""

    #print(gui_lib.open_log_file(gui_lib.os.getcwd(), False, ""))


    # Create the Qt Application
    # QApplication expects the first argument to be the program name.
    qt_args = sys.argv[:1] + unparsed_args
    app = gui_lib.QtWidgets.QApplication(qt_args)
    #gui_lib.Ui.load_cl_arg(app,parsed_args)
    # Create and show the form
    window = gui_lib.Ui(parsed_args)
    #window.load_cl_arg(parsed_args)
    # Run the main Qt loop
    sys.exit(app.exec_())
    #gui_lib.close_all_files(log_handle)