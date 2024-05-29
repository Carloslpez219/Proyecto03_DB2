from Data.data_definition import *
from prettytable import PrettyTable
import json
from Utils.file_utils import *
from Utils.validation_utils import *


# Función para el comando create
@LimpiarInput
def create(command):
    if "create " in command:
        command = command.replace("create ", "")
        command_split = command.split(",")
        if len(command_split) >= 2:
            table_name = scanWord(command_split[0])
            column_families = []
            for i in range(1, len(command_split)):
                column_families.append(scanWord(command_split[i]))
            if "ERROR" not in table_name:
                if not checkFile(table_name):
                    createFile(table_name, column_families)
                    if checkFile(table_name):
                        response = f"Table {table_name} already exists\n"
                    else:
                        response = f"Table {table_name} created\n"
                else:
                    response = f"Table {table_name} already exists\n"
            else:
                response = f"{table_name}: command not found\n"
        else:
            response = "Invalid command."
    else:
        response = "Invalid command."

    return response

# Función para el comando put
@LimpiarInput
def put(command):
    if "put " in command:
        command = command.replace("put ", "")
        command_split = command.split(",")
        if len(command_split) >= 4:
            table_name = scanWord(command_split[0])
            row_id = scanWord(command_split[1])
            column = scanWord(command_split[2])
            value = scanWord(command_split[3])
            timestamp = int(time())
            if checkFile(table_name):
                with open(f"./HFiles/{table_name}.json") as file:
                    data_table = json.load(file)
                if checkEnabled(data_table):
                    column_family, qualifier = column.split(":")
                    if checkColumn(data_table, column_family):
                        if not checkRowId(data_table, row_id):
                            data_table["Rows"][row_id] = {}
                        if column not in data_table["Rows"][row_id]:
                            data_table["Rows"][row_id][column] = []
                        # Añadir nuevo valor y timestamp
                        data_table["Rows"][row_id][column].append({
                            "value": value,
                            "timestamp": timestamp,
                        })
                        # Mantener solo los últimos tres timestamps
                        if len(data_table["Rows"][row_id][column]) > 3:
                            data_table["Rows"][row_id][column] = data_table["Rows"][row_id][column][-3:]
                        data_table["Rows"][row_id] = dict(sorted(data_table["Rows"][row_id].items()))
                        data_table["Rows"] = dict(sorted(data_table["Rows"].items()))
                        with open(f"./HFiles/{table_name}.json", "w") as file:
                            json.dump(data_table, file, indent=4)
                        return "0 row(s) in 0.0000 seconds"
                    else:
                        return f"Unknown column family {column_family}"
                else:
                    return "Table not enabled."
            else:
                return f"Table {table_name} does not exist."
        else:
            return "Invalid command."

# Función para el comando get
@LimpiarInput
def get(command):
    if "get " in command:
        command = command.replace("get ", "")
        command_split = command.split(",")
        table_name = scanWord(command_split[0])
        row_id = scanWord(command_split[1])
        versions = 1  # Por defecto, recuperar una sola versión

        # Verifica si se proporcionó un parámetro adicional para el número de versiones
        if len(command_split) > 2:
            try:
                versions = int(scanWord(command_split[2]))
            except ValueError:
                return "Invalid number of versions specified."

        if checkFile(table_name):
            with open(f"./HFiles/{table_name}.json") as file:
                data_table = json.load(file)
            if checkEnabled(data_table):
                if checkRowId(data_table, row_id):
                    row_info = data_table["Rows"][row_id]
                    table = PrettyTable()
                    table.field_names = ["COLUMN", "CELL"]
                    for column_key in row_info:
                        # Recuperar las versiones en orden descendente de timestamp
                        column_data_list = sorted(row_info[column_key], key=lambda x: x['timestamp'], reverse=True)
                        # Tomar solo las 'versions' más recientes
                        column_data_list = column_data_list[:versions]
                        for column_data in column_data_list:
                            table.add_row([column_key, f"timestamp={column_data['timestamp']}, value={column_data['value']}"])
                    return str(table)
                else:
                    return f"Row {row_id} does not exist in table {table_name}."
            else:
                return "Table not enabled."
        else:
            return f"Table {table_name} does not exist."
    else:
        return "Invalid command."


# Función para el comando scan
@LimpiarInput
def scan(command):
    if "scan " in command:
        command = command.replace("scan ", "")
        command_split = command.split(",")
        table_name = scanWord(command_split[0])
        versions = 1  # Por defecto, recuperar una sola versión

        # Verifica si se proporcionó un parámetro adicional para el número de versiones
        if len(command_split) > 1:
            try:
                versions = int(scanWord(command_split[1]))
            except ValueError:
                return "Invalid number of versions specified."

        if checkFile(table_name):
            with open(f"./HFiles/{table_name}.json") as file:
                data_table = json.load(file)
            if checkEnabled(data_table):
                table = PrettyTable()
                table.field_names = ["ROW", "COLUMN+CELL"]
                for row in data_table["Rows"]:
                    for column in data_table["Rows"][row]:
                        # Recuperar las versiones en orden descendente de timestamp
                        column_data_list = sorted(data_table["Rows"][row][column], key=lambda x: x['timestamp'], reverse=True)
                        # Tomar solo las 'versions' más recientes
                        column_data_list = column_data_list[:versions]
                        for column_data in column_data_list:
                            cell = f"{column}, timestamp={column_data['timestamp']}, value={column_data['value']}"
                            table.add_row([row, cell])
                return str(table)
            else:
                return "Table not enabled"
        else:
            return f"Table {table_name} does not exist."
    else:
        return "Invalid command"


# Función para el comando enable
@LimpiarInput
def enable(command):
    if "enable " in command:
        command = command.replace("enable ", "")
        table_name = scanWord(command)
        if checkFile(table_name):
            with open(f"./HFiles/{table_name}.json") as file:
                data_table = json.load(file)
            if not checkEnabled(data_table):
                data_table["Is_enabled"] = True
                with open(f"./HFiles/{table_name}.json", "w") as file:
                    json.dump(data_table, file, indent=4)
                return f"Table {table_name} was enabled."
            else:
                return f"Table {table_name} is already enabled."
        else:
            return f"Table {table_name} does not exist."
    else:
        return "Invalid command."

# Función para el comando disable
@LimpiarInput
def disable(command):
    if "disable " in command:
        command = command.replace("disable ", "")
        table_name = scanWord(command)
        if checkFile(table_name):
            with open(f"./HFiles/{table_name}.json") as file:
                data_table = json.load(file)
            if checkEnabled(data_table):
                data_table["Is_enabled"] = False
                with open(f"./HFiles/{table_name}.json", "w") as file:
                    json.dump(data_table, file, indent=4)
            else:
                return "Table not enabled"
            return f"Table {table_name} disabled."
        else:
            return "Table not found"
    return "ERROR: Wrong number of arguments: disable <table name>"

# Función para el comando count
@LimpiarInput
def count(command):
    if "count " in command:
        command = command.replace("count ", "")
        table_name = scanWord(command)
        if checkFile(table_name):
            with open(f"./HFiles/{table_name}.json") as file:
                data_table = json.load(file)
            if checkEnabled(data_table):
                return "0 row(s)\n" if len(data_table["Rows"]) == 0 else f"{len(data_table['Rows'])} row(s)\n"
            else:
                return f"ERROR: Table {table_name} is disabled\n"
        else:
            return f"ERROR: Table {table_name} not found\n"
    else:
        return "Invalid command."

# Función para el comando alter
@LimpiarInput
def alter(command):
    if "alter " in command:
        command = command.replace("alter ", "")
        command_split = command.split(",")
        if len(command_split) >= 3:
            table_name = scanWord(command_split[0])
            action = scanWord(command_split[1])
            column_family = scanWord(command_split[2])
            if checkFile(table_name):
                with open(f"./HFiles/{table_name}.json") as file:
                    data_table = json.load(file)
                if checkEnabled(data_table):
                    if action == "delete":
                        if checkColumn(data_table, column_family):
                            data_table["Column Families"].remove(column_family)
                            empty_rowid = []
                            for row_id in data_table["Rows"]:
                                key_list = list(data_table["Rows"][row_id].keys())
                                for i in key_list:
                                    if column_family in i:
                                        del data_table["Rows"][row_id][i]
                                if data_table["Rows"][row_id] == {}:
                                    empty_rowid.append(row_id)
                            for row_id in empty_rowid:
                                del data_table["Rows"][row_id]
                            with open(f"./HFiles/{table_name}.json", "w") as file:
                                json.dump(data_table, file, indent=4)
                            return f"Column family '{column_family}' deleted from table '{table_name}'."
                        else:
                            return f"Column family '{column_family}' does not exist in table '{table_name}'."
                    elif action == "update":
                        new_column_family = scanWord(command_split[3])
                        if checkColumn(data_table, column_family):
                            if not checkColumn(data_table, new_column_family):
                                data_table["Column Families"][data_table["Column Families"].index(column_family)] = new_column_family
                                for row_id in data_table["Rows"]:
                                    key_list = list(data_table["Rows"][row_id].keys())
                                    for i in key_list:
                                        if column_family in i:
                                            value = data_table["Rows"][row_id][i]
                                            del data_table["Rows"][row_id][i]
                                            column, qualifier = i.split(":")
                                            new_column = new_column_family + ":" + qualifier
                                            data_table["Rows"][row_id][new_column] = value
                                    if data_table["Rows"] != {}:
                                        data_table["Rows"][row_id] = dict(sorted(data_table["Rows"][row_id].items()))
                                with open(f"./HFiles/{table_name}.json", "w") as file:
                                    json.dump(data_table, file, indent=4)
                                return f"Column family '{column_family}' updated to '{new_column_family}' in table '{table_name}'."
                            else:
                                return f"New column family '{new_column_family}' already exists in table '{table_name}'."
                        else:
                            return f"Column family '{column_family}' does not exist in table '{table_name}'."
                    else:
                        return f"Invalid action '{action}' for command 'alter'."
                else:
                    return f"Table '{table_name}' is not enabled."
            else:
                return f"Table '{table_name}' does not exist."
        else:
            return "Invalid command format for 'alter' command."
    else:
        return "Invalid command. 'alter' keyword not found."

# Función para el comando describe
@LimpiarInput
def describe(command):
    if "describe " in command:
        table_name = scanWord(command.replace("describe ", ""))
        if checkFile(table_name):
            with open(f"./HFiles/{table_name}.json") as file:
                data_table = json.load(file)
            if checkEnabled(data_table):
                result = [
                    f"Table Name: {data_table['Table Name']}",
                    "Column Families:",
                    *[f" - {cf}" for cf in data_table["Column Families"]],
                    f"Is_enabled: {data_table['Is_enabled']}",
                ]
                return "\n".join(result)
            else:
                return "Table not enabled"
        else:
            return f"Table {table_name} does not exist."
    else:
        return "Invalid command"

# Otras funciones

def truncate(command):
    if "truncate " in command:
        command = command.replace("truncate ", "")
        table_name = scanWord(command)
        result = ""
        if checkFile(table_name):
            with open(f"./HFiles/{table_name}.json") as file:
                data_table = json.load(file)
            columns = data_table["Column Families"]
            result += disable(f"disable '{table_name}'")
            result += "\n"
            result += drop(f"drop '{table_name}'")
            result += "\n"
            column_families = ",".join([f"'{cf}'" for cf in columns])
            result += create(f"create '{table_name}',{column_families}")
            return result
        else:
            return f"Table {table_name} does not exist."

def delete(command):
    if "delete " in command:
        command = command.replace("delete ", "")
        command_split = command.split(",")
        if len(command_split) == 4:
            table_name = scanWord(command_split[0])
            row_id = scanWord(command_split[1])
            column = scanWord(command_split[2])
            timestamp = int(scanWord(command_split[3]))
            if checkFile(table_name):
                with open(f"./HFiles/{table_name}.json") as file:
                    data_table = json.load(file)
                if checkRowId(data_table, row_id):
                    if column in data_table["Rows"][row_id]:
                        if timestamp == data_table["Rows"][row_id][column]["timestamp"]:
                            del data_table["Rows"][row_id][column]
                            if data_table["Rows"][row_id] == {}:
                                del data_table["Rows"][row_id]
                with open(f"./HFiles/{table_name}.json", "w") as file:
                    json.dump(data_table, file, indent=4)
                return f"Row '{row_id}' deleted from table '{table_name}'."
    return "Invalid command"

def deleteAll(command):
    if "deleteall " in command:
        command = command.replace("deleteall ", "")
        command_split = command.split(",")
        if len(command_split) == 2:
            table_name = scanWord(command_split[0])
            row_id = scanWord(command_split[1])
            if checkFile(table_name):
                with open(f"./HFiles/{table_name}.json") as file:
                    data_table = json.load(file)
                if checkRowId(data_table, row_id):
                    del data_table["Rows"][row_id]
                with open(f"./HFiles/{table_name}.json", "w") as file:
                    json.dump(data_table, file, indent=4)
                return f"Row ID '{row_id}' deleted from table '{table_name}'."
    return "Invalid command"

def drop(command):
    if "drop " in command:
        command = command.replace("drop ", "")
        table_name = scanWord(command)
        if checkFile(table_name):
            os.remove(f"./HFiles/{table_name}.json")
            return f"Table {table_name} dropped successfully."
        else:
            return f"Table {table_name} does not exist."
    return "Invalid command"

def dropall(command):
    if "dropall" in command:
        result = ""
        command = command.replace("dropall ", "")
        command = scanWord(command)
        tables = os.listdir("./HFiles")
        for table in tables:
            table = table.replace('.json','')
            matched = re.search(command, table)
            if matched:
                os.remove(f"./HFiles/{table}.json")
                result += f"Table {table} dropped successfully."
        return result

# Función para listar tablas
def listTables():
    result = "TABLE \n"
    tables = os.listdir("./HFiles")
    for table in tables:
        table = table.replace('.json','')
        result = result + table + "\n"
    return result
