
import json
import pygame 
import customtkinter as ctk
import tkinter as tk
import json
import pygame

color_botones="#6C3483"
color_seleccionado = "#3498DB"
ancho_boton = 102

class copys:
    def __init__(self, root):
        self.root = root
        self.root.title("ValoArt")
        self.root.state("zoomed")
        self.cell_size = 61
        self.canvas_width = 26 * self.cell_size
        self.canvas_height = 13 * self.cell_size
        self.current_char = "█"
        self.char_options = ["─", "█", "▓", "▒", "░", "■", "▌", "▐", "▄", "▀", "▖", "▗", "▘", "▝", "▙", "▟", "▛", "▜", "▞", "▚"]
        self.is_drawing = False
        self.selected_button = None
        self.root.bind("<Up>", self.shift_up)
        self.root.bind("<Down>", self.shift_down)
        self.root.bind("<Left>", self.shift_left)
        self.root.bind("<Right>", self.shift_right)
        self.root.bind("<Control-c>", self.copy_text)
        self.root.bind("<Control-v>", self.insert_text)
        self.canvas = ctk.CTkCanvas(root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(pady=40)
        self.create_buttons()
        self.create_grid()
        self.load_saved_data()
        self.fade_in()

    def fade_in(self):

        for opacity in range(0, 11):
            self.root.attributes('-alpha', opacity / 10)
            self.root.update()
            self.root.after(50)

    def create_buttons(self):
        button_frame = ctk.CTkFrame(self.root, fg_color="#333333") 
        button_frame.pack()
        num_buttons = len(self.char_options)
        buttons_per_row = 1
        while num_buttons > buttons_per_row * 2:
            buttons_per_row += 1

        num_rows = (num_buttons + buttons_per_row - 1) // buttons_per_row

        self.button_dict = {}
        for i, char in enumerate(self.char_options):
            char_button = ctk.CTkButton(button_frame, text=char, command=lambda c=char: self.select_char(c),
                                        fg_color="#4A235A", text_color="white",width=ancho_boton)  
            self.button_dict[char] = char_button
            if i < len(self.char_options) // 2:
                char_button.grid(row=0, column=i, padx=10, pady=10)
            else:
                char_button.grid(row=1, column=i - len(self.char_options) // 2, padx=5, pady=10)

        copy_button = ctk.CTkButton(button_frame, text="Copiar", command=self.copy_text, fg_color=color_botones, text_color="white",width=ancho_boton)
        copy_button.grid(row=0, column=len(self.char_options) + 1, padx=10, pady=10)

        reset_button = ctk.CTkButton(button_frame, text="Rellenar", command=self.reset_grid, fg_color=color_botones, text_color="white",width=ancho_boton)
        reset_button.grid(row=0, column=len(self.char_options) + 2, padx=10, pady=10)

        insert_button = ctk.CTkButton(button_frame, text="Insertar", command=self.insert_text, fg_color=color_botones, text_color="white",width=ancho_boton)
        insert_button.grid(row=0, column=len(self.char_options) + 3, padx=10, pady=10)

        self.invert_button = ctk.CTkButton(button_frame, text="Volcar", command=self.show_replace_window, fg_color=color_botones, text_color="white",width=ancho_boton)
        self.invert_button.grid(row=1, column=len(self.char_options) + 1, padx=10, pady=10)

        self.mirror_button = ctk.CTkButton(button_frame, text="Espejo", command=self.mirror_text, fg_color=color_botones, text_color="white",width=ancho_boton)
        self.mirror_button.grid(row=1, column=len(self.char_options) + 2, padx=10, pady=10)

        cuack_button = ctk.CTkButton(button_frame, text="cuack", command=self.play_cuack_sound, fg_color=color_botones, text_color="white",width=ancho_boton)
        cuack_button.grid(row=1, column=len(self.char_options) + 3, padx=10, pady=10)

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
        if self.selected_button:
            self.selected_button.configure(fg_color="#4A235A")  
        self.current_char = char
        self.selected_button = self.button_dict[char]
        self.selected_button.configure(fg_color=color_seleccionado)
    	
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
        replace_window = ctk.CTkToplevel(self.root)
        replace_window.title("Volcado")
        replace_window.geometry("450x100") 
        window_width = replace_window.winfo_reqwidth()
        window_height = replace_window.winfo_reqheight()
        position_right = int(replace_window.winfo_screenwidth()/2 - window_width/2)
        position_down = int(replace_window.winfo_screenheight()/2 - window_height/2)
        replace_window.geometry("+{}+{}".format(position_right, position_down))
        replace_window.lift()
        replace_window.attributes('-topmost',True)
        replace_window.after_idle(replace_window.attributes,'-topmost',False)

        char_frame = ctk.CTkFrame(replace_window)
        char_frame.pack(side="left", padx=10, pady=10)

        replace_frame = ctk.CTkFrame(replace_window)
        replace_frame.pack(side="right", padx=10, pady=10)

        label1 = ctk.CTkLabel(char_frame, text="Carácter a reemplazar:")
        label1.pack()

        char_combobox = ctk.CTkComboBox(char_frame, values=self.char_options,fg_color=color_botones)
        char_combobox.pack(padx=10, pady=5)

        label2 = ctk.CTkLabel(replace_frame, text="Por:")
        label2.pack()

        replace_combobox = ctk.CTkComboBox(replace_frame, values=self.char_options, fg_color=color_botones)
        replace_combobox.pack(padx=10, pady=5)

        accept_button = ctk.CTkButton(replace_window, text="Aceptar", fg_color=color_botones, command=lambda: self.replace_char(char_combobox.get(), replace_combobox.get()))
        accept_button.pack(pady=10)

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

root = ctk.CTk()
root.iconbitmap("logo.ico")  
root.configure(bg="#333333")
app = copys(root)
root.bind("<ButtonRelease-1>", app.stop_drawing)
root.mainloop()