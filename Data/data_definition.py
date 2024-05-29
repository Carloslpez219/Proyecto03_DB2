from Utils import *
from time import *
import os
from prettytable import PrettyTable
import re

def LimpiarInput(func):
    def wrapper(command):
        # Verifica si la cadena contiene comillas mezcladas o no balanceadas
        if ('"' in command and "'" in command) or (command.count('"') % 2 != 0) or (command.count("'") % 2 != 0):
            return "Invalid command. Cannot mix single and double quotes or unclosed quotes."
        
        # Llama a la función original y verifica su resultado
        result = func(command)
        if result is None:
            return "Invalid command."
        
        return result

    return wrapper
