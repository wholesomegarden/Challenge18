import os

'''
    COLORS - MODULE - V.1.0
+------------------------+
This is a Python module to print
with colors.
Developed by qq8.

Usage:
colors.printc(text, color)
+------------------------+

'''

os.system('')

def printc(text, color):

    """
    Prints text with color.
    """

    if color == 'black':
        print('\033[30m' + text + '\033[0m')
        return

    if color == 'red':
        print('\033[31m' + text + '\033[0m')
        return

    if color == 'green':
        print('\033[32m' + text + '\033[0m')
        return

    if color == 'yellow':
        print('\033[33m' + text + '\033[0m')
        return

    if color == 'blue':
        print('\033[34m' + text + '\033[0m')
        return

    if color == 'magenta':
        print('\033[35m' + text + '\033[0m')
        return

    if color == 'cyan':
        print('\033[36m' + text + '\033[0m')
        return

    if color == 'white':
        print('\033[37m' + text + '\033[0m')
        return

    if color == 'underline':
        print('\033[4m' + text + '\033[0m')
        return