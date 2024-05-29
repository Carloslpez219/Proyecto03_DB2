# Constantes globales
RUTA_TABLAS = "./HFiles/"

themes = [
    {
        "result_text_fg": "white",
        "result_text_bg": "blue",
        "text_box_fg": "black",
        "text_box_bg": "blue",
        "button_fg": "white",
        "button_bg": "black",
    },
    {
        "result_text_fg": "black",
        "result_text_bg": "white",
        "text_box_fg": "black",
        "text_box_bg": "white",
        "button_fg": "white",
        "button_bg": "black",
    },
    {
        "result_text_fg": "yellow",
        "result_text_bg": "purple",
        "text_box_fg": "black",
        "text_box_bg": "purple",
        "button_fg": "white",
        "button_bg": "black",
    },
    {
        "result_text_fg": "green",
        "result_text_bg": "black",
        "text_box_fg": "black",
        "text_box_bg": "black",
        "button_fg": "white",
        "button_bg": "black",
    },
]

commands = [
    "create",
    "put",
    "get",
    "scan",
    "enable",
    "disable",
    "count",
    "alter",
    "describe",
    "truncate",
    "drop",
    "dropall",
    "clear",
    "cls",
    "exit",
    "help",
]


#init
#list
# # Crear la tabla 'peliculas' con las familias de columnas 'informacion', 'estado', 'ubicacion'
# create 'peliculas','genero','estado','ubicacion'

# # Alterar la tabla 'peliculas' para actualizar la familia de columnas 'informacion' agregando 'genero'
# alter 'peliculas','update','genero','informacion'

# # Insertar datos en la tabla 'peliculas' para la fila 'P001' en la columna 'informacion:titulo'
# put 'peliculas','P001','informacion:titulo','Inception'
# put 'peliculas','P001','informacion:director','Christopher Nolan'
# put 'peliculas','P001','informacion:genero','Ciencia Ficción'
# put 'peliculas','P001','estado:disponibilidad','Disponible'
# put 'peliculas','P001','ubicacion:estante','A1'

# # Obtener todos los datos de la fila 'P001'
# get 'peliculas','P001'

# # Obtener los últimos 3 datos de la fila 'P001'
# get 'peliculas', 'P001', 3

# # Escanear toda la tabla 'peliculas'
# scan 'peliculas'

# # Escanear los primeros 3 registros de la tabla 'peliculas'
# scan 'peliculas',3

# # Alterar la tabla 'peliculas' para eliminar la familia de columnas 'genero'
# alter 'peliculas','delete','ubicacion'

# # Eliminar todos los datos de la fila 'P002'
# deleteall 'peliculas','P002'

# # Eliminar un dato específico de la fila 'P001' en la columna 'informacion:genero' en un timestamp dado
# delete 'peliculas','P001','informacion:genero','timestamp'

# # Contar el número de filas en la tabla 'peliculas'
# count 'peliculas'

# # Describir la estructura de la tabla 'peliculas'
# describe 'peliculas'

# # Deshabilitar la tabla 'peliculas'
# disable 'peliculas'

# # Habilitar la tabla 'peliculas'
# enable 'peliculas'

# # Truncar la tabla 'peliculas' (eliminar todos los datos)
# truncate 'peliculas'

# # Eliminar la tabla 'peliculas'
# drop 'peliculas'

# # Eliminar todas las tablas que comiencen con 'cine*'
# dropall 'libros*'
