"""
Eingabe routines for mctdhinp
"""

#########################################################################
#
# FUNCTIONS IN THIS MODULE
#
# - build_cire                Buird a case-independent regular expression
# - cleanline                 Remove unused parts from a string
# - concntrt                  Concentrate whitespaces
# - einfilter                 Read the FILTER-SECTION
# - eininitwf                 Read the INIT_WF-SECTION
# - einintegrator             Read the INTEGRATOR-SECTION
# - einoct                    Read the OCT-SECTION
# - einoper                   Read the OPER-SECTION
# - einpbasis                 Read the PBASIS-SECTION
# - einrun                    Read the RUN-SECTION
# - einsection                Read a general section
# - einspf                    Read the SBASIS-SECTION
# - eintarget                 Read the TARGET-SECTION
# - eindirdyn                 Read the DIRDYN-SECTION
# - eininitgeom               Read the INITIAL-GEOMETRY-SECTION
# - findparam                 Find a key=value pair
# - findsec                   Find a section
# - secnames                  Extract names (e.g. of Hamiltonians)
# - stripblkcmts              Remove comments
#
# To do additional parsing of sections modify the specialized
# functions. All, except einrun, are based on function einsection.
# einsection provides automatic key=value extraction and
# seaches for boolean flags. More complex structures remain inparsed.
#
# 04/2009 MS
# Altered MAP 2022, more robust and more 'pythonic'
#########################################################################


__all__ = ['build_cire', 'eininitwf', 'einintegrator', 'einoct',
         'einoper', 'einpbasis', 'einrun', 'einspf', 'einsection',
         'einfilter', 'eintarget', 'secnames', 'cleanline', 'concntrt',
         'findparam', 'findsec', 'stripblkcmts']

#high level imports
import re
from MCTDH_.mctdhinp import MctdhSection

##############################################################################
# Some tools first
##############################################################################
#a dictionary of what the sections might contain
# section_dic = {
#             "filename",
#             "startstr",
#             "closestr",
#             "keys",
#             "flags",
#             "readrest"
#             }

def build_cire(text):
    """
    build_cire(str) -> str1:
    Build a regular expression string str1 that finds str
    regardles of upper or lower case letters in str
    """
    pattern = [int(s.isalpha()) *('['+s+s.swapcase()+']')+ \
                    (1-int(s.isalpha()))*(s) for s in text]
    #evaluates * 0 or 1 ----^
    return ''.join(pattern)


##############################################################################



def stripblkcmts(line):
    """
    stripblkcmts(string) -> str
    - Remove comments of form '# commenttext' from end of str
    - Make str only containing whitespaces an empty string
    - remove all '\n' escape characters
    - remove leading whitespaces
    """
    #import re
    pat = ("#.*$", "^[ \t]*$", "[ \t]*\\n", '^[ \t]*', '[ \t]*$')
    # for i in range(len(pat)):
    #     line = re.subn(pat[i], '', line)[0]
    for pats in pat:
        line = re.subn(pats, '',line)[0]
    return line
##############################################################################

def concntrt(line):
    """
    concntrt(string) -> str
    - concentrate comma separated text
    (remove blanks, e.g.: "a, b , c" -> "a,b,c")
    - concentrate assignments
    (remove blanks, e.g.: "a  =  b" -> "a=b")
    - make multiple blanks a single space
    """
    #import re

    pat = ('[ \t]*,[ \t]*',
         '[ \t]*=[ \t]*',
         '[ \t][ \t]*',
        '^[ \t]*')

    rep = (',', '=', ' ', '')


    # for i in range(len(pat)):
    #     line = re.subn(pat[i], rep[i], line)[0]
    for index, pats in enumerate(pat):
        line = re.subn(pats, rep[index], line)[0]
    return line


##############################################################################


def cleanline(line):
    """
    cleanline(string) -> str
    - Remove comments of form '# commenttext' from end of str
    - Make str only containing whitespaces an empty string
    - remove all '\\n' escape characters
    - concentrate comma separated text
      (remove blanks, e.g.: "a, b , c" -> "a,b,c")
    - concentrate assignments
      (remove blanks, e.g.: "a  =  b" -> "a=b")
    - make multiple blanks a single space
    """
    line = stripblkcmts(line)
    line = concntrt(line)

    return line

##############################################################################

def findsec(startstr, closestr, lines):
    """
    findsec(startstr,closestr,lines) -> list[]

    Returns a list of lines between startstr and closestr in lines
    list[] does not include the lines containing startstr and closestr
    """

    startstr = startstr.upper()
    closestr = closestr.upper()
    #import re

    startline = -1
    endline = -1
    # for j in range(len(lines)):
    #     if re.search("^"+startstr+'[ \t]*$', lines[j].upper()):
    #         startline = j+1
    #         break
    for index, line in enumerate(lines):
        if re.search("^"+startstr+'[ \t]*$', line.upper()):
            startline = index+1
            break

    for j in range(len(lines))[startline:]:
        if re.search("^"+closestr+'[ \t]*$', lines[j].upper()):
            endline = j
            break
    # for index, line in enumerate(lines[(startline-1):]):
    #     if re.search("^"+closestr+'[ \t]*$', line.upper()):
    #         endline = index
    #         break

    if startline > endline or startline == endline or startline < 0 or endline < 0:
        return None

    return lines[startline:endline] #return section

##############################################################################

def findparam(param, line):
    """ findparam(param, line) -> val,line
    return val,line if string "param=val" is contained in line
    remove param=val from line. If param is not in line, return None,line"""
    #import re

    pattern = build_cire(param)

    pattern += "=.*"
    findpat = re.compile(pattern)
    mat = findpat.match(line)
    if mat:
        parval = mat.group().split("=")[1]
        line = re.sub(pattern, '', line)
        return (parval, line)

    return (None, line)


#############################################################################
# Input routines for sections
##############################################################################

##############################################################################

# RUN-SECTION is sort of special - it gets its own routine:
# Except from the title, there are only flags and key=value
# pairs in a RUN-SECTION. So we go by formal patterns instead
# of keylists.
def einrun(file_inp):
    """ Read a run-section from file and return a section object"""
    #import re
    #from MCTDH_.mctdhinp import mctdhsection

    startstr = 'RUN-SECTION'
    closestr = 'END-RUN-SECTION'

    #create a section object
    sec = MctdhSection(startstr, closestr)


    file_inp.seek(0)

    #read lines and do some cleanup (remove comments etc)
    lines = map(cleanline, file_inp.readlines())
    # throw away empty lines
    lines = [line for line in lines if line]

    # see if we can find the section
    lines = findsec(startstr, closestr, lines)
    if lines is None:
        # Section not found
        return None

    #find title (given as rest of line)
    findttl = re.compile(build_cire('title')+"[ \t]*=")
    #for j in range(len(lines)):
    for index, line in enumerate(lines):
        mat = findttl.match(line)
        if mat:
            sec["title"] = lines[index][mat.end():]
            line = re.sub(build_cire('title')+'.*$', '', line)
            break
    #title is an entire line
    findttl = re.compile(build_cire('title'))
    #for j in range(len(lines)):
    for index, line in enumerate(lines):
        mat = findttl.match(line)
        if mat:
            sec['title'] = lines[index+1]
            line = re.sub(build_cire('title'), '', line)
            lines.pop(index+1)
            break

    #find parameters (structures like: a=b,c,d.... )
    findpar = re.compile(r"[\S]*=[\S\.\,]*")

    #for j in range(len(lines)):
    for line in lines:
        mat = findpar.findall(line)
        if mat:
            #for i in range(len(mat)):
            for maty in mat:
                lin = maty.split("=")
                sec[lin[0].lower()] = lin[1]
                line = re.sub(maty, '', line)
    del findpar, mat

    #everything else is flags
    text = " ".join(lines)
    text = cleanline(text)
    flags = text.split(' ')
    # for i in range(len(flags)):
    #     sec.setflag(flags[i].lower())
    for flag in flags:
        sec.setflag(flag.lower())
    return sec


##############################################################################

# all sections wich are not RUN-SECTION are wrapped

def einoper(file_inp):
    """ Read a oper-section from file and return a section object"""

    sect_dict = {}
    sect_dict["file_inp"] = file_inp
    sect_dict["readrest"] = True

    sect_dict["startstr"] = 'OPERATOR-SECTION'
    sect_dict["closestr"] = 'END-OPERATOR-SECTION'

    sect_dict["keylist"]  = [
                            "opname",
                            "oppath",
                            "parfile",
                            "splinepath",
                            "cutoff",
                            "gwpintorder"]

    sect_dict["flaglist"] = [
                            "closed",
                            "open",
                            "projection",
                            "analytic_pes",
                            "print-npot",
                            "optcontract",
                            "gwp_renorma",
                            "nogwp_renorma"]

    sect_dict["subsect"] =[
                            {
                            "substart" : "alter-parameters",
                            "subclose" : "end-alter-parameters",
                            "subname" : "alter-parameters"},
                            {
                            "substart" : "alter-labels",
                            "subclose" : "end-alter-labels",
                            "subname" : "alter-labels"}
                            ]

    return ein_dict_section(sect_dict)


##############################################################################


def einspf(file_inp):
    """ Read a SPF-section from file and return a section object"""

    sect_dict = {}
    sect_dict["file_inp"] = file_inp
    sect_dict["readrest"] = True

    sect_dict["startstr"] = 'SPF-BASIS-SECTION'
    sect_dict["closestr"] = 'END-SPF-BASIS-SECTION'

    sect_dict["keylist"] = ['packets']
    sect_dict["flaglist"] = ['multi-set',
                            "single-set"
                            "no-redundancy-check"]

    sec = ein_dict_section(sect_dict)

    if sec is None:
        sect_dict["startstr"] = 'SBASIS-SECTION'
        sect_dict["closestr"] = 'END-SPF-BASIS-SECTION'

        sec = ein_dict_section(sect_dict)

    if sec is None:

        sect_dict["startstr"] = 'SPF-BASIS-SECTION'
        sect_dict["closestr"] = 'END-SBASIS-SECTION'

        sec = ein_dict_section(sect_dict)


    if sec is None:

        sect_dict["startstr"] = 'SBASIS-SECTION'
        sect_dict["closestr"] = 'END-SBASIS-SECTION'

        sec = ein_dict_section(sect_dict)


    if sec is not None:   #added MAP to deal with absence of this section
        if ('multi-set' in sec.flags) and ("single-set" in sec.flags):
            message = sect_dict["startstr"] + ": either 'multi-set' or 'single-set' "
            message += "may be used. Not both."
            raise RuntimeError(message)

    return sec

##############################################################################

def einpbasis(file_inp):
    """ Read a SPF-section from file and return a section object"""
    sect_dict = {}
    sect_dict["file_inp"] = file_inp
    sect_dict["readrest"] = True

    sect_dict["startstr"] = 'PBASIS-SECTION'
    sect_dict["closestr"] = 'END-PBASIS-SECTION'

    sec = ein_dict_section(sect_dict)

    if sec is None:
        sect_dict["startstr"] = 'PRIMITIVE-BASIS-SECTION'
        sect_dict["closestr"] = 'END-PBASIS-SECTION'

        sec = ein_dict_section(sect_dict)

    if sec is None:
        sect_dict["startstr"] = 'PBASIS-SECTION'
        sect_dict["closestr"] = 'END-PRIMITIVE-BASIS-SECTION'

        sec = ein_dict_section(sect_dict)

    if sec is None:
        sect_dict["startstr"] = 'PRIMITIVE-BASIS-SECTION'
        sect_dict["closestr"] = 'END-PRIMITIVE-BASIS-SECTION'

        sec = ein_dict_section(sect_dict)


    return sec



##############################################################################

def einoct(file_inp):
    """ Read a oct-section from file and return a section object"""
    sect_dict = {}
    sect_dict["file_inp"] = file_inp
    sect_dict["readrest"] = True

    sect_dict["startstr"] = 'OCT-SECTION'
    sect_dict["closestr"] = 'END-OCT-SECTION'

    sect_dict["keylist"] = [
                            "algorithm",
                            'functype',
                            "iterations",
                            "operator",
                            "guess",
                            "penalty-function",
                            "penalty-factor",
                            "reference",
                            "write",
                            "save",
                            "filter"]

    sect_dict["flaglist"] = [
                            'tdoverlap',
                            'alignphs',
                            'no-reffilter',
                            'filter']

    return ein_dict_section(sect_dict)




##############################################################################

def einintegrator(file_inp):
    """ Read a integrator-section from file and return a section object"""

    sect_dict = {}
    sect_dict["file_inp"] = file_inp
    sect_dict["readrest"] = True

    sect_dict["startstr"] = 'INTEGRATOR-SECTION'
    sect_dict["closestr"] = 'END-INTEGRATOR-SECTION'

    sect_dict["keylist"] = [
                            "CMF",
                            "CMF/fix",
                            "CMF/var",
                            "CMF/var2",
                            "CMF/varphi",
                            "CMF/vara",
                            "ML-CMF",
                            "ABM/S",
                            "BS/S",
                            "RK5/S",
                            "RK8/S",
                            "SIL/S",
                            "CSIL/S",
                            "DAV",
                            "rDAV",
                            "rrDAV",
                            "cDAV",
                            "LSODA",
                            "ZVODE/S"]

    sect_dict["flaglist"] = [

                            "VMF"]

    return ein_dict_section(sect_dict)


##############################################################################

def eintarget(file_inp):
    """ Read a target-section from file and return a section object"""
    sect_dict = {}
    sect_dict["file_inp"] = file_inp
    sect_dict["readrest"] = True

    sect_dict["startstr"] = 'TARGET-SECTION'
    sect_dict["closestr"] = 'END-TARGET-SECTION'

    sect_dict["keylist"] = ["operator",]

    return ein_dict_section(sect_dict)


##############################################################################
def eininitwf(file_inp):
    """ Read a init_wf-section from file and return a section object"""
    sect_dict = {}
    sect_dict["file_inp"] = file_inp
    sect_dict["readrest"] = True

    sect_dict["startstr"] = 'INIT_WF-SECTION'
    sect_dict["closestr"] = 'END-INIT_WF-SECTION'

    sect_dict["keylist"] = [
                            "file",
                            "block-SPF",
                            "block-A"
                                    ]
    sect_dict["flaglist"] = [
                            "realpsi"
                            ]
    sect_dict["subsect"] =[
                            {
                            "substart" : "build",
                            "subclose" : "end-build",
                            "subname" : "build"},
                            {
                            "substart" : "read-inwf",
                            "subclose" : "end-read-inwf",
                            "subname" : "read-inwf"}
                            ]

    return ein_dict_section(sect_dict)

##############################################################################
def einfilter(file_inp):
    """ Read a init_wf-section from file and return a section object"""
    sect_dict = {}
    sect_dict["file_inp"] = file_inp
    sect_dict["readrest"] = True

    sect_dict["startstr"] = 'FILTER-SECTION'
    sect_dict["closestr"] = 'END-FILTER-SECTION'

    return ein_dict_section(sect_dict)


##############################################################################

##############################################################################

def eindirdyn(file_inp):
    """ Read a DIRDYN-SECTION from file and return a section object"""
    sect_dict = {}
    sect_dict["file_inp"] = file_inp
    sect_dict["readrest"] = True

    sect_dict["startstr"] = 'DIRDYN-SECTION'
    sect_dict["closestr"] = 'END-DIRDYN-SECTION'

    sect_dict["keylist"] = [
                            "qcprogram",
                            "subcmd",
                            "method",
                            "ener0",
                            "nroot",
                            "data",
                            "db",
                            "update",
                            "dbmin",
                            "dbpoint",
                            "dbweight",
                            "mindv",
                            "dd_diab",
                            "ddtrans",
                            "transfile",
                            "coinfile",
                            "dreffile",
                            "nbasis" ]

    sect_dict["flaglist"] = ["simulate",
                            "fchk",
                            "ascii_db",
                            "dd_adiab",
                            "dipole",
                            "dbsave",
                            "ddlog",
                            "hess_upd",
                            "rediabatise"]

    return ein_dict_section(sect_dict)


##############################################################################

##############################################################################

def eininitgeom(file_inp):
    """ Read a INITIAL-GEOMETRY-section from file and return a section object"""
    sect_dict = {}
    sect_dict["file_inp"] = file_inp
    sect_dict["readrest"] = True

    sect_dict["startstr"] = 'INITIAL-GEOMETRY-SECTION'
    sect_dict["closestr"] = 'END-INITIAL-GEOMETRY-SECTION'

    sect_dict["keylist"] = [
                "nstates",
                "init_state",
                "init_basis_dist"
                            ]
    sect_dict["flaglist"] = [
                "mom_distrib",
                "coo_distrib"
                            ]
    sect_dict["subsect"] =[
                            {
                            "substart" : "cartesian",
                            "subclose" : "end-cartesian",
                            "subequals" : True,
                            "subname" : "cartesian",
                            "subkeys" : ["cartesian"]},
                            {
                            "substart" : "nmode",
                            "subclose" : "end-nmode",
                            "subname" : "nmode"}
                            ]

    return ein_dict_section(sect_dict)


##############################################################################

##############################################################################

def einsection(file_inp, startstr, closestr, keys=None, flags=None, readrest=True):
    """
    einsection(file_inp,startstr,closestr,keys=[],flags=[],readrest=True) -> section

    - Create section object with startstr,closestr
    - reads file f, searches for textblock between lines startstr
      and closestr.
    - If textblock not found, return None
      Otherwise:
    - Extracts parameters of form key=value if
      key is in keys and sets section[key]=value.
    - Removes key=value from textblock.
    - Looks if the textblock contains the word
      flags[i], and calls section.setflag[flags[i]] if the word is
      in the text
    - removes flags[i] from textblock.
    - Reads the textblock into section.data if readrest is True
    - Returns section
    """
    #import re
    #from MCTDH_.mctdhinp import mctdhsection

    sec = MctdhSection(startstr, closestr)

    file_inp.seek(0)
    lines = file_inp.readlines()

    #if we need to process, do the basic string conversions
    #if len(keys) > 0:
    if keys is not None:
        lines = map(cleanline, lines)
    else:
        #otherwise remove only comments and whitespaces
        #(data goes into 'data')
        lines = map(stripblkcmts, lines)

    #remove empty lines
    lines = [line for line in lines if line]

    # see if we can find our section
    lines = findsec(startstr, closestr, lines)
    if lines is None:
        return None


    #read parameters list
    for line in lines:
        for key in keys:
            val, line = findparam(key, line)
            if val:
                sec[key.lower()] = val
                break

    #read flags ist
    for line in lines:
        for flag in flags:
            words = line.lower().split(' ')
            c_words = line.split(' ')
            if flag.lower() in words:
                sec.setflag(flag.lower())
                c_words.pop(words.index(flag.lower()))
                line = ' '.join(c_words)

    # cleaning up
    lines = [line.lstrip() for line in lines if line.lstrip()]
    #del line
    #everything else is 'data'
    if readrest:
        map(sec.adddataitem, lines) #this doesn't append correctly
        #map(sec.adddataitem(lines), lines)
        #this does append but doesn't deal with strings correctly
    # done! section is ready
    return sec



##############################################################################
def ein_dict_section(sec_dict):
    """
    altered form of einsection that accepts a dictionary which contains what is needed
    Can be altered more easily for new options
    einsection(file_inp,startstr,closestr,keys=[],flags=[],readrest=True) -> section
    sect_dict = {} -dict of parameters to search in section
        sect_dict["file_inp"] = input file to search through
        sect_dict["readrest"] = whether to read textblock in section.data
        sect_dict["startstr"] = string that marks start of section
        sect_dict["closestr"] = string that marks end of section
        sect_dict["keylist"]  = list of keys of form key = X
        sect_dict["flaglist"] = list of flags (i.e true or false options)

        sect_dict["subsect"] = list of dictionary of subsection info
    - Create section object with startstr,closestr
    - reads file f, searches for textblock between lines startstr
      and closestr.
    - If textblock not found, return None
      Otherwise:
    - Extracts parameters of form key=value if
      key is in keys and sets section[key]=value.
    - Removes key=value from textblock.
    - Looks if the textblock contains the word
      flags[i], and calls section.setflag[flags[i]] if the word is
      in the text
    - removes flags[i] from textblock.
    - Reads the textblock into section.data if readrest is True
    - Returns section
    """
    #import re
    #from MCTDH_.mctdhinp import mctdhsection

    sec = MctdhSection(sec_dict["startstr"], sec_dict["closestr"])

    sec_dict["file_inp"].seek(0)
    lines = sec_dict["file_inp"].readlines()

    #if we need to process, do the basic string conversions
    #if len(keys) > 0:
    if "keylist" in sec_dict:
        lines = map(cleanline, lines)
    else:
        #otherwise remove only comments and whitespaces
        #(data goes into 'data')
        lines = map(stripblkcmts, lines)

    #remove empty lines
    lines = [line for line in lines if line]

    # see if we can find our section
    lines = findsec(sec_dict["startstr"], sec_dict["closestr"], lines)
    if lines is None:
        return None


    #read parameters list
    #check again if present
    if "keylist" in sec_dict:
        for line in lines:
            for key in sec_dict["keylist"]:
                val, line = findparam(key, line)
                if val:
                    sec[key.lower()] = val
                    #del line
                    break

    #read flags ist
    if "flaglist" in sec_dict:
        for line in lines:
            for flag in sec_dict["flaglist"]:
                words = line.lower().split(' ')
                c_words = line.split(' ')
                if flag.lower() in words:
                    sec.setflag(flag.lower())
                    c_words.pop(words.index(flag.lower()))
                    line = ' '.join(c_words)
                    #del line

    #see if there are sub-sections
    if "subsect" in sec_dict:
        #look for each sub section in turn
        for sub in sec_dict["subsect"]:
            if "subequals" in sub:
                #sub section title includes an equals, need to find, save and use as new key
                for line in lines:
                    if (sub["substart"] in line) and ("=" in line):
                        #remove white space and use as key
                        sub["substart"] = line
                        break
            sublines = findsec(sub["substart"], sub["subclose"], lines)
            if "subequals" in sub:
                sublines.insert(0,sub["substart"])
            sec.subsect[sub["subname"]] = sublines
            #remove sublines from lines
            #lines = lines.replace(sublines, "")

    # cleaning up
    lines = [line.lstrip() for line in lines if line.lstrip()]
    #del line
    #everything else is 'data'
    #if sec_dict["readrest"]:
        #map(sec.adddataitem, lines) #this doesn't append correctly
        #map(sec.adddataitem(lines), lines)
        #this does append but str functions doesn't deal with it correctly
    # done! section is ready
    return sec

##############################################################################


def secnames(file_inp, secname, delim='_'):
    """
    secname(file_inp,secname,delim) -> list
    Returns a list of names of sections in file f where sections are labeled
    "section_name", e.g, the line "HAMILTONIAN-SECTION_dipole" will result in
    ['dipole'] if secname is "HAMILTONIAN-SECTION" and delim is "_"
    """
    if file_inp.closed:
        file_inp.open()
    file_inp.seek(0)
    lines = map(cleanline, file_inp.readlines())

    #import re
    pat = "^[ \t]*"+build_cire(secname)+delim+"[a-zA-Z0-9]+[ \t]*$"


    newlines = [line.split(delim)[1] for line in lines if re.match(pat, line)]

    return newlines






##############################################################################
