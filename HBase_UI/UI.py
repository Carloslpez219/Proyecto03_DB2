import tkinter as tk
from tkinter import ttk
from HBase_UI.commands import *
from Utils import *
from Data.data_definition import *
from PIL import Image, ImageTk
from Constants.constants import commands, themes


"""
Funcionalidades:

- pasar texto a la consola
- cambiar tema
- mandar comandos a la consola con enter o botón
- simulación visual de HBase Shell
- autocomplete

Keywords:

- clear = limpiar la consola
- exit = salir del programa
- help = mostrar comandos
- create
- list
- disable
- Is_enabled
- alter
- drop
- drop all
- describe

"""


class HBASEUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HBase")
        self.root.pack_propagate(0)
        self.root.geometry("800x700")
        self.root.minsize(1200, 1000)
        self.root.maxsize(1200, 1000)

        self.style = ttk.Style()
        self.style.configure(
            "TEntry", foreground="white", background="black", font=("Courier", 12)
        )

        self.root.configure(bg="black")
        self.text_box = tk.Text(self.root, wrap="word", font=("Courier", 12), fg="white", bg="black", insertbackground="white")
        self.text_box.pack(expand=True, fill="both", padx=20, pady=20)
        self.text_box.bind("<Return>", self.run_command)

        self.shell_started = False
        self.first_hbase_shell = True
        self.command_counter = 0
        self.prompt = "C:\\hbase\\shell> "

        self.text_box.insert("end", self.prompt)
        self.text_box.mark_set("insert", "end")
        self.text_box.focus()
        self.text_box.configure(state="normal")

        self.root.mainloop()

    def run_command(self, event):
        self.text_box.configure(state="normal")
        input_text = self.get_input().strip()
        self.text_box.insert("end", "\n")

        if not self.shell_started:
            if input_text.lower() == "init" and self.first_hbase_shell:
                self.shell_started = True
                self.first_hbase_shell = False
                self.init_message()
            else:
                self.text_box.insert("end", f"{self.prompt}use 'init' to start\n")
        else:
            if input_text.lower() == "help":
                self.Execute(self.show_help())
            elif input_text.lower() == "clear" or input_text.lower() == "cls":
                self.text_box.delete("1.0", "end")
            elif input_text.lower() == "exit":
                self.root.destroy()
            elif "create" in input_text.lower():
                self.Execute(create(input_text), input_text)
            elif "put" in input_text.lower():
                self.Execute(put(input_text), input_text)
            elif "get" in input_text.lower():
                self.Execute(get(input_text), input_text)
            elif "scan" in input_text.lower():
                self.Execute(scan(input_text), input_text)
            elif "enable" in input_text.lower():
                self.Execute(enable(input_text), input_text)
            elif "disable" in input_text.lower():
                self.Execute(disable(input_text), input_text)
            elif "count" in input_text.lower():
                self.Execute(count(input_text), input_text)
            elif "alter" in input_text.lower():
                self.Execute(alter(input_text), input_text)
            elif "list" == input_text.lower():
                self.Execute(listTables(), input_text)
            elif "describe" in input_text.lower():
                self.Execute(describe(input_text), input_text)
            elif "truncate" in input_text.lower():
                self.Execute(truncate(input_text), input_text)
            elif "delete " in input_text.lower():
                self.Execute(delete(input_text), input_text)
            elif "deleteall" in input_text.lower():
                self.Execute(deleteAll(input_text), input_text)
            elif "drop " in input_text.lower():
                self.Execute(drop(input_text), input_text)
            elif "dropall" in input_text.lower():
                self.Execute(dropall(input_text), input_text)
            else:
                self.text_box.insert("end", f"{self.prompt}Unknown command: {input_text}\n")
        
        self.text_box.insert("end", self.prompt)
        self.text_box.mark_set("insert", "end")
        self.text_box.see("end")
        self.text_box.configure(state="normal")
        self.text_box.focus()
        return "break"

    def get_input(self):
        input_text = self.text_box.get("insert linestart", "insert")
        return input_text[len(self.prompt):]

    def init_message(self):
        self.text_box.insert(
            "end",
            "'help' -> supported commands.\n"
            '"exit" -> to leave\n'
        )
        self.text_box.insert("end", f"\n{self.prompt}")
        self.text_box.mark_set("insert", "end")
        self.text_box.see("end")

    def show_help(self):
        help_text = ""
        for command in commands:
            help_text += f"{command}\n"
        return help_text

    def Execute(self, function, input_text=""):
        response = function
        formatted_counter = f"{self.command_counter:03}"
        self.text_box.insert(
            "end", f"hbase(command):{formatted_counter}:0> {input_text}\n{response}\n"
        )
        self.text_box.see("end")
        self.command_counter += 1