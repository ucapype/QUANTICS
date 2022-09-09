"""
Module to wrap input data in classes mctdhsection, mctdhinput and mctdhoper

Sections have the following structure:
-- They are enclosed in an opening string and a closing string, e.g.
   "RUN-SECTION" and "END-RUN-SECTION"
-- They may contain parameters: variable names and assigned value, e.g.,
   "tfinal=100". These are stored in a dictionary 'parameters'
-- Boolean Flags may be set, e.g., "auto" and "geninwf"
   This is stored as in the 'flags' list
-- There may as well be other data of a different type, e.g.,
   specification of the primitive grid, the integrator etc.
   for which there is no need to parse it at this point
   this is just treated as stringsdata and is not processed
   (except concentration of blanks)

mctdhinput contains a dictionary with sections imported from file.

mctdhoper contains three dictionaries, one for sections, one for
   Hamiltonians and one for functions

No exception handling in this module. Exceptions have to be catched
in calling module

"""

#########################################################################
#
# CLASSES IN THIS MODULE
#
# - mctdhsection              Wrapping of a section object
# - mctdhinput                Wrapping of a complete input file
# - mctdhoper                 Wrapping of a complete operator file
#
# 04/2009 MS
#########################################################################




__all__ = ['MctdhSection', 'MctdhInput', 'MctdhOper']

#Imports here

import os
import re
#import MCTDH_.mctdheingabe as mctdheingabe
##############################################################################


class MctdhSection:
    """ Definition of a section object to wrap all
    XXX-SECTION patterns of MCTDH imput files
    """

    def __init__(self, ostr="", cstr=""):
        self.parameters = {}    # all data of form "key=value1[,value2[,...]]"
        self.flags = []         # flags that evaluate to True of False
        self.openstr = ostr     # opening 'tag' of a text section
        self.closestr = cstr    # closing 'tag' of a text section
        self.free = []          # any other stuff as free form
        self.subsect = {}       # any subsections the section might contain
        self.uniques = []


    def __str__(self):
        """ Return a string representation of section """
        strng = self.openstr+"\n"
        #if len(self.parameters):
        if self.parameters is not None:
            strng += " \n".join([" %s = %s " % (key, value) for key, value \
                                   in self.parameters.items()])
            strng += " \n"

        for str_list in self.uniques:
            for string in str_list:
                strng += " " + string + "\n"

        flagslen = len(self.flags)
        for i in range(flagslen):
            strng += " " + str(self.flags[i])
            if (i+1)%3 == 0:
                strng += "\n"

        if (flagslen)%3 != 0:
            strng += "\n"
        if flagslen:
            strng += " \n"
        del flagslen


        datalen = len(self.free)
        for i in range(datalen):
            strng += " "+ str(self.free[i]) + "\n"
        del datalen

        strng += self.closestr+'\n'

        return strng

    def __setitem__(self, key, item):
        """ Set a key-value-pair in parameters{} """
        self.parameters[key] = item

    def __getitem__(self, key):
        """ Return value of key in parameters{} """
        if key in self.parameters:
        #if self.parameters.has_key(key):   #no longer in python3
            return self.parameters[key]
        else:
            return None

    def setparam(self, key, item):
        """ Set a key-value-pair in parameters{} """
        self.parameters[key] = item

    def getparam(self, key):
        """ Return value of key in parameters{} """
        return self.parameters[key]

    def delparam(self, key):
        """ Return value of key in parameters{} """
        if self.parameters.has_key(key):
            return self.parameters.pop(key)

    def hasparam(self, key):
        """ Return true if key in parameters{} """
        return self.parameters.has_key(key)

    def setflag(self, flag=''):
        """ Set a flag in flags[] """
        if not self.hasflag(flag):
            self.flags.append(flag)

    def getflag(self, index):
        """ get a flag from flags[] by index """
        return self.flags[index]


    def hasflag(self, flag=''):
        """ Check for flag being in flags[] """
        return self.flags.__contains__(flag)


    def delflag(self, flag=''):
        """ If flags[] contains flag """
        if  self.flags.__contains__(flag):
            self.flags.remove(flag)
        else:
            return

    def setunique(self, unique_str_list):
        """ Set a unique in unique[] """
        if (not self.hasunique(unique_str_list)) and len(unique_str_list) > 0:
            self.uniques.append(unique_str_list)

    def getunique(self, index):
        """ get a unique from unique[] by index """
        return self.uniques[index]


    def hasunique(self, unique_str_list):
        """ Check for unique being in unique[] """
        return self.uniques.__contains__(unique_str_list)


    def delunique(self, unique_str_list):
        """ If unique[] contains unique """
        if  self.uniques.__contains__(unique_str_list):
            self.uniques.remove(unique_str_list)
        else:
            return

    def adddataitem(self, data):
        '''
        Adds unsorted lines into class as data
        '''
        self.free.append(data)

    def deldataitem(self, item=''):
        '''
        Delete something in the data of class
        '''
        if  self.free.__contains__(item):
            self.free.remove(item)
        else:
            return

    def readataitem(self, item=""):
        '''
        Find the item in a list
        '''
        if  item in self.free:
            return True
        else:
            return False

    def popdataitem(self, index):
        '''
        pops item out of list
        '''
        return self.free.pop(index)

    def isempty(self):
        '''
        Checks if lists are empty
        '''
        #if len(self.parameters) or len(self.flags) or len(self.data):
        #can this be replaced with just return self.paramers or ...?
        if self.parameters or self.flags or self.free:
            return False
        else:
            return True


    def copy(self, other):
        """ Copy a section object """
        self.clear()
        self.openstr = other.openstr
        self.closestr = other.closestr
        self.parameters = other.parameters.copy()
        self.flags = []
        for i in range(len(other.flags)):
            self.flags.append(other.flags[i])
        self.free = []
        for i in range(len(other.free)):
            self.free.append(other.free[i])
        self.uniques = []
        for i in range(len(other.uniques)):
            self.uniques.append(other.uniques[i])


    def clear(self):
        """ Clear flags parameters and data,
        set openstr and closestr to empty strings """
        self.parameters.clear()
        self.flags = []
        self.free = []
        self.openstr = ''
        self.closestr = ''

    def clearcontent(self):
        """ Clear flags parameters and data,
        but leave openstr and closestr unchanged """
        self.parameters.clear()
        self.flags = []
        self.free = []




#from MCTDH_.mctdheingabe import *
import MCTDH_.mctdheingabe as mctdheingabe
class MctdhInput:
    """ Wrapping of an MCTDH input file. class MCTDHInput
    contains a dictionary holding the sections of an input file """

# this could be extended with other input sections
    secimportmap = {
                  "runsection":      mctdheingabe.einrun,
                  "opersection":       mctdheingabe.einoper,
                  "octsection":        mctdheingabe.einoct,
                  "pbassection":       mctdheingabe.einpbasis,
                  "spfbassection":     mctdheingabe.einspf,
                  "initwfsection":     mctdheingabe.eininitwf,
                  "intsection":        mctdheingabe.einintegrator,
                  "targetsection":     mctdheingabe.eintarget,
                  "filtersection":     mctdheingabe.einfilter,
                  "dirdynsection":      mctdheingabe.eindirdyn,
                  "initgeomsection":    mctdheingabe.eininitgeom
                  }


    def __init__(self, filename=''):
        self.sections = {}
        if filename:
            self.importfile(filename)

    def __str__(self):
        " retuns a string representing an MCTDH input file "

        strng = "## MCTDH input file:\n\n"
        #for key in self.sections.keys():
        for key in self.sections:
            strng += str(self.sections[key])
            strng += "\n"
        strng += "end-input\n "
        return strng

    def __setitem__(self, key, item):
        """ Set a key-value-pair in parameters{} """
        self.sections[key] = item

    def __getitem__(self, key):
        """ Return value of key in parameters{} """
        return self.sections[key]

    def hasseckey(self, secname, seckey):
        """
        hasseckey(secname,seckey) -> bool
        Return True if section secname exists and contains key seckey.
        Return False otherwise
        """
        if secname in self.sections: #has_key not vaild
        #if self.sections.has_key(secname):
            #return self.sections[secname].parameters.has_key(seckey)
            return seckey in self.sections[secname].parameters
        else:
            return False


    def hassecflag(self, secname, flag):
        """
        hassecflag(secname,secflag) -> bool
        Return True if section secname exists and contains flag flag.
        Return False otherwise
        """
        #if self.sections.has_key(secname): #changed MAP as has_key removed and in fails
        try:
            self.sections[secname].flags.index(flag)
        except ValueError:
            return False
        except KeyError:
            return False
        return True

        #else:
        #return False


    def copy(self, other):
        "Copy other instance to self"
        self.clear()
        for name in other.sections.keys():
            self.sections[name] = MctdhSection()
            self.sections[name].copy(other.sections[name])


    def clear(self):
        "Delete all data"
        self.sections.clear()

    def addsection(self, name, sec):
        """
        addsection(secname,section)
        Copy section and add the copy with name secname
        to the sections dictionary
        """
        secy = MctdhSection()
        secy.copy(sec)
        self.sections[name] = secy

    def delsection(self, name):
        """
        delsection(secname)
        If exists: delete the section with name secname
        from the sections dictionary. Otherwise do nothing.
        """
        #if self.sections.has_key(name): return self.sections.pop(name)
        if name in self.sections:
            return self.sections.pop(name)


    def sectionnames(self):
        """Return a list of all section names"""
        return self.sections.keys()


    def importfile(self, filename):
        """ importfile(filename): Import input from file filename"""

        file_inp = open(filename,'r')
        for name, importfunc in self.secimportmap.items():
            sec = importfunc(file_inp)
            if sec:
                self[name] = sec


    def exportfile(self, filename, overwrite=True, mode='w'):
        """
        ExportFile(filename,owerwrite=True,mode='w'):
        Save input to ASCII file.
        """

        if os.path.exists(filename) and not overwrite:
            message = "\nNo permition to overwrite file: "+filename+'\n'
            message += "Try setting the overwrite flag."
            raise Exception(message)
        else:
            file_inp = open(filename, mode)
            file_inp.write(str(self))
            file_inp.close()
            #catch possible ecxeption in calling module

##############################################################################

class MctdhOper(MctdhInput):
    """ Wrapping of an MCTDH oper file. class mctdhoper
    contains a dictionaries holding the sections, Hamiltonians
    and functions of an operator file """

    #              name            --------------------arguments-------------------  function
    secimportmap = {"opdefine"    : ("OP_DEFINE-SECTION", "END-OP_DEFINE-SECTION",
                                   mctdheingabe.einsection),
                  "parameter"   : ("PARAMETER-SECTION", "END-PARAMETER-SECTION",
                                   mctdheingabe.einsection),
                  "dissipative" : ("DISSIPATIVE-SECTION", "END-DISSIPATIVE-SECTION",
                                   mctdheingabe.einsection),
                  "labels"      : ("LABELS-SECTION", "END-LABELS-SECTION",
                                   mctdheingabe.einsection),
                  }


    def __init__(self, filename = ''):
        self.sections = {}  # Sections
        self.operators = {} # hamiltonians
        self.functions = {} # functions as used sometimes for OCT-MCTDH
        if filename:
            self.importfile(filename)


    def __str__(self):
        " retuns a tring representing an MCTDH operator file "

        strng = "## MCTDH operator file:\n\n"
        #for key in self.sections.keys():
        for key in self.sections:
            strng += str(self.sections[key])+"\n"
            strng += "\n\n"

        # write system operator first
        syskey = "system"
        if syskey in self.operators.keys():
            strng += str(self.operators[syskey])+"\n"
            strng += "\n\n"
        #for key in self.operators.keys():
        for key in self.operators:
            if not key == syskey:
                strng += str(self.operators[key])+"\n"
                strng += "\n\n"

        #for key in self.functions.keys():
        for key in self.functions:
            strng += str(self.functions[key])+"\n"
            strng += "\n\n"

        strng += "end-operator\n "
        return strng


    def switchsign(self, opname='system'):
        """
        switchsign(opname='system') : multiply operator opname with -1
        Raise Exception of operator does not exist.
        """

        #if self.operators.has_key(opname):
        if opname in self.operators:

            def swsgn(line):

                if line[0:5] == '-----':
                    return line
                if re.search('^[ \t]*[mM][oO][dD][eE][sS]', line) is not None:
                    return line
                pat = r'^[ \t]*-[a-zA-Z0-9\.]+'
                if re.search(pat, line) is not None:
                    return re.sub('^[ \t]*-', '', line)
                pat = r'^[ \t]*\+[ \t]*[a-zA-Z0-9\.]+'
                if re.search(pat, line)is not None:
                    return re.sub(r'^[ \t]*\+', '-', line)
                pat = r'^[ \t]*[a-zA-Z0-9\.]+'
                if re.search(pat, line) is not None:
                    return re.sub('^[ \t]*', '-', line)

            self.operators[opname].data =  \
                [swsgn(line) for line in self.operators[opname].data]

        else:
            raise Exception("No operator with name: "+opname)


    def copy(self, other):
        "Copy from other to self"
        self.clear()
        for name in other.sections.keys():
            self.sections[name] = MctdhSection()
            self.sections[name].copy(other.sections[name])
        for name in other.operators.keys():
            self.operators[name] = MctdhSection()
            self.operators[name].copy(other.operators[name])
        for name in other.functions.keys():
            self.functions[name] = MctdhSection()
            self.functions[name].copy(other.functions[name])



    def clear(self):
        "Delete all data"
        self.sections.clear()
        self.operators.clear()
        self.functions.clear()



    def addoper(self, name, sec):
        """
        AddOper(name,sec): Add section object sec to operators dictionary
        with key name
        """
        secy = MctdhSection()
        secy.copy(sec)
        self.operators[name] = secy

    def deloper(self, name):
        """
        deloper(name):
        if self.operators.has_key(name): return self.operators.pop(name)
        """
        #if self.operators.has_key(name): return self.operators.pop(name)
        if name in self.operators:
            return self.operators.pop(name)



    def addfunction(self, name, sec):
        """
        addfunction(name,sec): Add section object sec to functionss dictionary
        with key name
        """
        secy = MctdhSection()
        secy.copy(sec)
        self.functions[name] = secy


    def delfunction(self, name):
        """
        delfunction(name):
        if self.functionss.has_key(name): return self.functions.pop(name)
        """
        #if self.functions.has_key(name): return self.functions.pop(name)
        if name in self.functions:
            return self.functions.pop(name)

    def delallfunctions(self):
        """
        delallfunctions(name):
        Clear the functions dictionary.
        """
        self.functions.clear()

    def importfile(self, filename):
        """importfile(filename): Import operator file filename where filename
        can be a relative or absolute path of the file"""

        file_inp = open(filename, 'r')
        #import MCTDH_.mctdheingabe as mctdheingabe
        # import all sections
        for name, (arg0, arg1, importfunc) in self.secimportmap.items():
            sec = importfunc(file_inp, arg0, arg1)
            if sec:
                self.sections[name] = sec


        #append system hamiltonian
        sstr = 'HAMILTONIAN-SECTION'
        estr = 'END-HAMILTONIAN-SECTION'
        delim = '_'
        sec = mctdheingabe.einsection(file_inp, sstr, estr)
        if sec:
            self.operators['system'] = sec



        #append other hamiltonians
        hamsecs = mctdheingabe.secnames(file_inp, sstr, delim)

        for name in hamsecs:
            self.operators[name] = mctdheingabe.einsection(file_inp,
                                                         sstr+str(delim)+str(name), estr)


        #append 1d functions

        sstr = 'FUNCTION-SECTION'
        estr = 'END-FUNCTION-SECTION'
        delim = '_'

        hamsecs = mctdheingabe.secnames(file_inp, sstr, delim)

        for name in hamsecs:
            self.functions[name] = mctdheingabe.einsection(file_inp,
                                                         sstr+str(delim)+str(name), estr)



    def exportfile(self, filename, overwrite=True, mode='w'):
        """
        exportfile(filename,overwrite=True,mode='w'):
        Save operator file as ASCII to file filename.
        Raise Exception if file exists and overwrite if False.
        """

        if os.path.exists(filename) and not overwrite:
            message = "\nNo permition to overwrite file: "+filename+'\n'
            message += "Try setting the overwrite flag."
            raise Exception(message)
        else:
            file_inp = open(filename, mode)
            file_inp.write(str(self))
            file_inp.close()
            #catch possible ecxeption in calling module
