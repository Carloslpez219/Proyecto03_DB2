import json
import os
from time import *


def scanWord(word: str):
    # Verifica y elimina las comillas, si están balanceadas
    if word.startswith("'") and word.endswith("'"):
        return word.strip("'")
    elif word.startswith('"') and word.endswith('"'):
        return word.strip('"')
    return word


def createFile(table_name, column_families):
    hfile_content = {
        "Table Name": table_name,
        "Column Families": column_families,
        "Is_enabled": True,
        "Rows": {},
    }
    with open(f"./HFiles/{table_name}.json", "w") as hfile:
        json.dump(hfile_content, hfile, indent=4)


def checkFile(table_name):
    path = f"./HFiles/{table_name}.json"
    if os.path.exists(path):
        creation_time = os.path.getctime(path)
        current_time = time()
        # Verifica si el archivo fue creado hace menos de 0.5 segundos
        if (current_time - creation_time) < 0.5:
            return False
        return True
    return False
