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


#Hbase shell
#list
#create 'universidad','facultades','cursos'
#alter 'universidad','update','facultades','carreras'
#put 'universidad','UVG','carreras:ingenieria','ciencias de la computacion'
#get 'universidad','UVG'
#get 'universidad','UVG',3

#scan 'universidad'
#scan 'universidad', 3