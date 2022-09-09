# Python GUI for Quantics

## General

To create/edit gui_files

- use PyQT5 bindings to QT GUI (can install with anaconda, conda install pyqt)
(also Pyside which has more restrictive license)

- for designer get QT designer
    -install with qttools5-dev-tools & qttools5-dev

- The .ui file from designer can either be converted directly to a .py file using
    pyuic5 <file>.ui -o <file>.py
- or it can be loaded dynamically in a python file using

~~~python
window = uic.loadUi("./test.ui")
window.show()
~~~

## Input GUI

Run the quantics_inp_gui.py script, this will import necessary files

Each section has its own tab, there is a check box at the top that must be checked if you wish the section to be included in the calculation.
When options have been selected choose either generate input from file menu or button on Input tab.
This will refresh the text in the file text box on the input tab (note this will overwrite the current contents.)
The text in this box can be editted freely if extra options or more control is needed

When happy go Files -> Save File to create actual input file

### Implementation

- ui
  - contains the ui files and the main gui library, this is used for all gui actions
- MCTDH_
  - contains the MCTDH input file parser from the opt control, has been updated and altered a bit
- gui_parsers
  - contains modules to parse cli arguments passed to programme

The GUI works by letting each control have dynamic variables that link to a dictionary in the MCTDH parser.
If adding a control add a quantp dynamics library and set the value to be name of the argument.

for example, the name of the calculation would be set to 'name'.

The control must then be added to the appropriate function in gui_lib using findchild.

For example the name control (called 'name_txt') is under the run tab. So in the function find_run_cntrls the following line is added

~~~ python
self.run_control.append(self.findChild(QtWidgets.QPlainTextEdit,'name_txt'))
~~~

note that the nature of the control (i.e QPlainTextEdit) must be correct

Each section is represented by a tab in the GUI, if a new section is added this needs several dynamic variables to work:

- secname - the name of the section
- func - the name of the function to find the controls
- ctl_list - the name of the list that contains the controls in the section
- sec_chk - the name of the check box that indicates if a section is needed or not
- sec_str - the string name of the section that will be append to -SECTION and END- -SECTION for creating the section in the MCTDH library

For example, taking the run section:

- secname - runsection
- func - find_run_cntrls
- ctl_list - run_control
- sec_chk - run_inc
- sec_str - RUN

## Analysis GUI

To compile simpsys for pygui (for now)
May need to remove old libraries
rm -rf  bin/binary/x86_64  object/x86_64

to compile.cnf add -fPIC to the following flags to relevant compiler section:
QUANTICS_FFLAGS_DEB
QUANTICS_FFLAGS_OPT
QUANTICS_CFLAGS

Run compilation of analyse programmes with:
' compile analyse'
Then in gui_files folder run:
Note f2py can be any version just replace 3.8 as needed (e.g. 3.6 for python 3.6)
Remove the --debug_capi for final version

~~~bash
f2py3.8 --debug-capi -c -m simp ~/quantics/source/analyse/gui_sys.F90 -I/home/mike/quantics/object/x86_64/gfortran/include \
/home/mike/quantics/object/x86_64/gfortran/propwf.a \
/home/mike/quantics/object/x86_64/gfortran/geninwf.a \
/home/mike/quantics/object/x86_64/gfortran/genoper.a \
/home/mike/quantics/object/x86_64/gfortran/gendvr.a \
/home/mike/quantics/object/x86_64/gfortran/quanticslib.a \
/home/mike/quantics/object/x86_64/gfortran/opfuncs.a \
/home/mike/quantics/object/x86_64/gfortran/libode.a \
/home/mike/quantics/object/x86_64/gfortran/quanticsmod.a \
/home/mike/quantics/object/x86_64/gfortran/includes.a   \
/home/mike/quantics/object/x86_64/gfortran/libnum.a \
/home/mike/quantics/object/x86_64/gfortran/libsys.a \
/home/mike/quantics/object/x86_64/gfortran/liblapack.a \
/home/mike/quantics/object/x86_64/gfortran/libblas.a \
/home/mike/quantics/object/x86_64/gfortran/libomp.a \
/home/mike/quantics/object/x86_64/gfortran/mctdh.a \
/home/mike/quantics/object/x86_64/gfortran/potfit.a \
/home/mike/quantics/object/x86_64/gfortran/analyse.a \
/home/mike/quantics/object/x86_64/gfortran/includes.a \
/home/mike/quantics/object/x86_64/gfortran/quanticsmod.a \
/home/mike/quantics/object/x86_64/gfortran/versions.o \
/home/mike/quantics/object/x86_64/gfortran/libsys.a


-L /home/mike/quantics/bin/dyn_libs -lsrf -lusrf
~~~

to create library

To create/edit gui_files

- use PyQT5 bindings to QT GUI (can install with anaconda, conda install pyqt)
(also Pyside which has more restrictive license)

- for designer get QT designer
   -install with qttools5-dev-tools & qttools5-dev
- The .ui file from designer can either be converted directly to a .py file using
   pyuic5 <file>.ui -o <file>.py
- or it can be loaded dynamically in a python file using
    window = uic.loadUi("./source/analyse/gui_files/test.ui")
    window.show()

To debug python and Fortran see following:
<https://nadiah.org/2020/03/01/example-debug-mixed-python-c-in-visual-studio-code/>
use following launch.json

~~~json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "(gdb) Attach",
            "type": "cppdbg",
            "request": "attach",
            "program": "/home/mike/miniconda3/bin/python", 
            "processId": "${command:pickProcess}",
            "MIMode": "gdb",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ]
        },
        
        
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}/.vscode/ar_he_nacm_35b_S_4_19_mom_st12_4/"
        }
    ]
} 
~~~
