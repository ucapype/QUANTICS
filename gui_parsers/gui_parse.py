'''
Module with parser for cli to the guis
'''
import argparse #import for parsing of command line options
import os   #for file stuff

def parsing():
    '''
    Function create the cmd line argument parsing
    returns the parsing function
    would make sense to go in its own library separate to gui things
    '''

    #the - means optional argument, no dash means must be given and error is raised if not
    parse = argparse.ArgumentParser(description='Purpose: \
                                    Create inputs for Quantics calculations')
    parse.add_argument('-f',
                        metavar='FILE',
                        type=str,
                        default ='',
                        help='quantics input file to read in \
                            The string FILE may be a relative or a full path-name ')
    return parse
