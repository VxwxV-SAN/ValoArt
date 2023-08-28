import tkinter as tk
from tkinter import ttk
import json
import pygame 
from tkinter import Text

class copys:
    def __init__(self, root):
        self.root = root
        self.root.title("ValoArt VxwxV")
        self.root.state("zoomed")
        self.cell_size = 70
        self.canvas_width = 26 * self.cell_size
        self.canvas_height = 13 * self.cell_size
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        self.current_char = "█"
        self.char_options = ["─", "█", "▓", "▒", "░","■","▌", "▐","▄","▀", "▖", "▗", "▘", "▝", "▙", "▟", "▛", "▜", "▞", "▚"]
        self.is_drawing = False
        self.selected_button = None
        self.root.bind("<Up>", self.shift_up) 
        self.root.bind("<Down>", self.shift_down)  
        self.root.bind("<Left>", self.shift_left)  
        self.root.bind("<Right>", self.shift_right)
        self.root.bind("<Control-c>", self.copy_text)
        self.root.bind("<Control-v>", self.insert_text)
        self.create_buttons()
        self.create_grid()
        self.load_saved_data()

    def create_buttons(self):
        style = ttk.Style()
        style.configure("Dark.TFrame", background="#333333")
        style.configure("Dark.TButton", background="black", foreground="black",font=("Fixedsys"))  
        style.configure("Selected.TButton", background="white", foreground="blue", font=("Fixedsys"))
        button_frame = ttk.Frame(root, style="Dark.TFrame")
        button_frame.pack()

        num_buttons = len(self.char_options)


        buttons_per_row = 1
        while num_buttons > buttons_per_row * 2:
            buttons_per_row += 1

        num_rows = (num_buttons + buttons_per_row - 1) // buttons_per_row

        self.button_dict = {}
        for i, char in enumerate(self.char_options):
            char_button = ttk.Button(button_frame, text=char, command=lambda c=char: self.select_char(c), style="Dark.TButton")
            self.button_dict[char] = char_button
            if i < len(self.char_options) // 2:  
                char_button.grid(row=0, column=i, padx=5, pady=10)
            else:
                char_button.grid(row=1, column=i - len(self.char_options) // 2, padx=5, pady=10)

        copy_button = ttk.Button(button_frame, text="Copiar", command=self.copy_text, style="Dark.TButton")
        copy_button.grid(row=0, column=len(self.char_options) + 1, padx=10, pady=10)

        reset_button = ttk.Button(button_frame, text="Rellenar", command=self.reset_grid, style="Dark.TButton")
        reset_button.grid(row=0, column=len(self.char_options) + 2, padx=10, pady=10)

        insert_button = ttk.Button(button_frame, text="Insertar", command=self.insert_text, style="Dark.TButton")
        insert_button.grid(row=0, column=len(self.char_options) + 3, padx=10, pady=10)

        self.invert_button = ttk.Button(button_frame, text="Volcar", command=self.show_replace_window, style="Dark.TButton")
        self.invert_button.grid(row=1, column=len(self.char_options) + 1, padx=10, pady=10)

        self.mirror_button = ttk.Button(button_frame, text="Espejo", command=self.mirror_text, style="Dark.TButton")
        self.mirror_button.grid(row=1, column=len(self.char_options) + 2, padx=5, pady=10)

        cuack_button = ttk.Button(button_frame, text="cuack", command=self.play_cuack_sound, style="Dark.TButton")
        cuack_button.grid(row=1, column=len(self.char_options) + 3, padx=5, pady=10)

    def create_grid(self):
        self.cells = []

        self.canvas.configure(bg="#101a23")

        for y in range(13):
            row = []
            for x in range(26):
                cell = self.canvas.create_text(
                    x * self.cell_size + self.cell_size / 2,
                    y * self.cell_size + self.cell_size / 2,
                    text=self.current_char,
                    font=("Fixedsys", int(-self.cell_size)), 
                    fill="white", 
                )
                row.append(cell)
            self.cells.append(row)

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)

    def select_char(self, char):
        self.current_char = char
        if self.selected_button:
            self.selected_button.configure(style="Dark.TButton")
        self.selected_button = self.button_dict[char]
        self.selected_button.configure(style="Selected.TButton")
    	
    def on_canvas_click(self, event):
        self.is_drawing = True
        self.update_cell(event)
        self.save_data()

    def on_canvas_drag(self, event):
        if self.is_drawing:
            self.update_cell(event)
            self.save_data()

    def mirror_text(self):
        mirrored_characters = {
            "▌": "▐",
            "▐": "▌",
            "▖": "▗",
            "▗": "▖",
            "▘": "▝",
            "▝": "▘",
            "▟":"▙",
            "▙":"▟",
            "▛": "▜",
            "▜": "▛",
            "▞": "▚",
            "▚": "▞"
        }

        for y, row in enumerate(self.cells):
            reversed_row = [mirrored_characters.get(self.canvas.itemcget(cell, "text"), self.canvas.itemcget(cell, "text")) for cell in reversed(row)]
            for x, cell in enumerate(row):
                self.canvas.itemconfig(cell, text=reversed_row[x])
        self.save_data()

    def play_cuack_sound(self):
        pygame.mixer.init()  
        pygame.mixer.music.load("cuack.mp3")  
        pygame.mixer.music.play()

    def update_cell(self, event):
        x, y = event.x // self.cell_size, event.y // self.cell_size
        self.canvas.itemconfig(self.cells[y][x], text=self.current_char)

    def copy_text(self, event=None):
        copied_text = "\n".join(["".join([self.canvas.itemcget(cell, "text") for cell in row]) for row in self.cells])
        root.clipboard_clear()
        root.clipboard_append(copied_text)

    def reset_grid(self):
        for row in self.cells:
            for cell in row:
                self.canvas.itemconfig(cell, text=self.current_char)
        self.save_data()

    def save_data(self):
        data = []
        for row in self.cells:
            data_row = [self.canvas.itemcget(cell, "text") for cell in row]
            data.append(data_row)
        with open("data.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

    def load_saved_data(self):
        try:
            with open("data.json", "r") as json_file:
                data = json.load(json_file)
                for y, row in enumerate(data):
                    for x, char in enumerate(row):
                        self.canvas.itemconfig(self.cells[y][x], text=char)
        except FileNotFoundError:
            pass

    def show_replace_window(self):
        replace_window = tk.Toplevel(self.root)
        replace_window.title("Volcado")

        char_frame = ttk.Frame(replace_window)
        char_frame.pack(side="left", padx=10, pady=10)

        replace_frame = ttk.Frame(replace_window)
        replace_frame.pack(side="right", padx=10, pady=10)

        label1 = ttk.Label(char_frame, text="Carácter a reemplazar:")
        label1.pack()

        selected_char = tk.StringVar()
        char_combobox = ttk.Combobox(char_frame, textvariable=selected_char, values=self.char_options)
        char_combobox.pack(padx=10, pady=5)

        label2 = ttk.Label(replace_frame, text="Por:")
        label2.pack()

        replace_selected = tk.StringVar()
        replace_combobox = ttk.Combobox(replace_frame, textvariable=replace_selected, values=self.char_options)
        replace_combobox.pack(padx=10, pady=5)

        accept_button = ttk.Button(replace_window, text="Aceptar", command=lambda: self.replace_char(selected_char.get(), replace_selected.get()))
        accept_button.pack(pady=10)
        replace_window.iconbitmap("logo.ico")
        
    def replace_char(self, char_to_replace, char_to_replace_with):
        if char_to_replace not in self.char_options or char_to_replace_with not in self.char_options:
            return

        for row in self.cells:
            for cell in row:
                if self.canvas.itemcget(cell, "text") == char_to_replace:
                    self.canvas.itemconfig(cell, text=char_to_replace_with)

        self.save_data()

    def insert_text(self, event=None):
        inserted_text = root.clipboard_get()


        inserted_text = inserted_text.replace("\n", "")

 
        inserted_text = inserted_text[:len(self.cells) * len(self.cells[0])]

        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                char_index = y * len(row) + x  

                if char_index < len(inserted_text):
                    self.canvas.itemconfig(cell, text=inserted_text[char_index])
                else:
                    self.canvas.itemconfig(cell, text='') 

        self.save_data()

    def stop_drawing(self, event):
        self.is_drawing = False

    def shift_up(self, event):
        self.shift_cells(0, -1)
        
    def shift_down(self, event):
        self.shift_cells(0, 1)
        
    def shift_left(self, event):
        self.shift_cells(-1, 0)
        
    def shift_right(self, event):
        self.shift_cells(1, 0)


    def shift_cells(self, dx, dy):
        new_cells = [[self.canvas.itemcget(cell, "text") for cell in row] for row in self.cells]

        for y in range(len(self.cells)):
            for x in range(len(self.cells[y])):
                new_x = (x + dx) % len(self.cells[y])
                new_y = (y + dy) % len(self.cells)

                new_cells[new_y][new_x] = self.canvas.itemcget(self.cells[y][x], "text")

        for y in range(len(self.cells)):
            for x in range(len(self.cells[y])):
                self.canvas.itemconfig(self.cells[y][x], text=new_cells[y][x])

        self.save_data()

root = tk.Tk()
root.iconbitmap("logo.ico")
root.configure(bg="#333333")
app = copys(root)
root.bind("<ButtonRelease-1>", app.stop_drawing)
root.mainloop()