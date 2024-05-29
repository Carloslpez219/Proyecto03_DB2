def checkEnabled(data_table):
    return data_table.get("Is_enabled", False)

def checkColumn(data_table, column):
    return column in data_table.get("Column Families", [])

def checkRowId(data_table, row_id):
    return row_id in data_table.get("Rows", {})
