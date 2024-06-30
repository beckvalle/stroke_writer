#!/usr/bin/python3

import csv
from tkinter import *
from tkinter import ttk
from os.path import exists


# create the main application window
root = Tk()
root.geometry("700x700")

choose_window = None

show_outline_var = BooleanVar()
show_arrows_var = BooleanVar()
stroke_number_var = IntVar()
current_letter_var = StringVar()

show_outline_var.set(True)
show_arrows_var.set(True)
stroke_number_var.set(0)
current_letter_var.set('')

content = ttk.Frame(root)
content.grid(column=0, row=0)

stroke_window = ttk.Frame(content)
stroke_window.grid(column=0, row=0)

stroke_canvas = ttk.Frame(stroke_window, padding=(2, 2, 2, 2))
stroke_canvas.grid(column=0, row=0)

stroke_options = ttk.Frame(stroke_window)
stroke_options.grid(column=0, row=1)

info_frame = ttk.Frame(content)

name_lbl = ttk.Label(info_frame, text="Prompt: ")
hint_lbl = ttk.Label(info_frame, font=("Arial", 50))
stroke_num_lbl = ttk.Label(info_frame, text="Stroke: ")

strokes_frame = ttk.Frame(content)
button_frame = ttk.Frame(content)

letter_frame = ttk.Frame(content)
letter_frame.grid(column=2, row=0)



###################################
###################################

def close_window(window):
    window.destroy()

def clear_all():
    clear_canvas()
    clear_hint()

def clear_canvas():
    sketch.delete('all')
    show_grid()
    stroke_number_var.set(0)
    stroke_num_lbl.config(text="Stroke: ")
    sketch.clear_stroke()

def show_grid():
    sketch.draw_hor_guides()
    sketch.draw_vert_guides()
    sketch.draw_diag_guides()

def clear_hint():
    hint_lbl['text'] = ''

def load_language_options():
    langs = []
    lang_abrs = []
    with open("sw_langs.csv", 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            lang_abrs.append(row["lid"])
            langs.append(row["lname"])
    return [lang_abrs, langs]

def store_language_options():
    fieldnames = ["lid", "lname", "char_set"]
    if not (exists("sw_langs.csv",)):
        with open("sw_langs.csv", 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
            writer.writeheader()

def setup_language_strokes(in_language_abr):
    fieldnames = ["symbol_name", "strokes"]
    fnm = in_language_abr+'_stk.csv'
    if not (exists(fnm)):
        with open(fnm, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
            writer.writeheader()

def load_strokes(in_frame, in_language_abr, in_canvas):
    show_load_options(in_frame, in_language_abr, in_canvas)

def show_load_options(in_frame, in_language, in_canvas):
    if in_language in langs_abr:
        fnm = in_language+'_stk.csv'
    else:
        fnm = langs_abr[langs.index(in_language)]+'_stk.csv'
    print(in_frame)
    print(fnm)
    col_ct = 0
    row_ct = 0
    button_ids = []
    chars = []

    with open("sw_langs.csv", 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["lid"] == in_language:
                raw_chars = row['char_set'].split(" ")
                for rc in raw_chars:
                    chars.append(rc)

    for char in chars:
        button_id = ttk.Button(in_frame, text=char, 
            command = lambda text=char:in_canvas.set_current_letter(text), state=DISABLED)
        button_ids.append(button_id)
    
    with open(fnm, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            button_letter = row['symbol_name']
            if button_letter in chars:
                for bid in button_ids:
                    if bid.cget('text') == button_letter:
                        bid.configure(state=NORMAL)

    sorted_button_ids = sorted(button_ids, key=lambda x: x.cget('text'))    
    for bid in sorted_button_ids:
        bid.grid(column=col_ct, row=row_ct)
        col_ct +=1
        if col_ct > 4:
            col_ct = 0
            row_ct += 1

class Stroke_canvas(Canvas):

    def __init__(self, parent, language, **kwargs):
        super().__init__(parent, **kwargs)
        self.language = language
        self.csvfile_name = self.language+'_stk.csv'
        self.fieldnames = ["symbol_name", "strokes"]
        self.letter_loaded = False
        self.point_color = "blue"
        self.stroke_end_id_holder = []
        self.stroke_line_id_holder = []
        self.coords_holder = []
        self.single_stroke_holder = []
        self.loaded_stroke_id_holder = []

        setup_language_strokes(self.language)

        # test bounds
        # self.create_rectangle(0,0,5,5, outline="magenta")
        # self.create_rectangle(400,400,405,405, outline="red")
        # self.create_rectangle(3,3,402,402, outline="blue")
        # self.create_rectangle(2,2,403,403, outline="black")

        self.draw_vert_guides()
        self.draw_diag_guides()
        self.draw_hor_guides()

        # bind mouse movement to draw functions within canvas
        self.bind("<Button-1>", self.save_posn)
        self.bind("<Button-1>", self.change_pt_color_to_red, add='+')
        self.bind("<Button-1>", self.add_circle, add='+')
        self.bind("<B1-Motion>", self.add_line)
        self.bind("<B1-ButtonRelease>", self.change_pt_color_to_red)
        self.bind("<B1-ButtonRelease>", self.add_circle, add='+')
        self.bind("<B1-ButtonRelease>", self.increment_stroke, add='+')

    def save_posn(self, event):
        self.lastx, self.lasty = event.x, event.y
        self.single_stroke_holder.append(str(event.x))
        self.single_stroke_holder.append(str(event.y))

    def add_line(self, event):
        self.stroke_line_id_holder.append(
            self.create_line((self.lastx, self.lasty, event.x, event.y), 
                width=10, fill="red"))
        self.save_posn(event)

    def add_circle(self, event):
        self.stroke_end_id_holder.append(
            self.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, 
                fill=self.point_color, outline=""))

    def increment_stroke(self, event):
        stroke_number_var.set(stroke_number_var.get()+1)
        stroke_num_lbl.config(text="Stroke: "+str(stroke_number_var.get()))
        self.coords_holder.append((';').join(self.single_stroke_holder))
        self.single_stroke_holder = []
        
    def clear_stroke(self):
        self.stroke_end_id_holder = []
        self.stroke_line_id_holder = []
        self.coords_holder = []
        stroke_number_var.set(0)
        stroke_num_lbl.config(text="Stroke: ")

    def clear_last_stroke(self):

        # print(len(stroke_end_id_holder), len(stroke_line_id_holder), len(coords_holder))
        id = self.stroke_end_id_holder.pop()
        self.delete(id)
        id = self.stroke_end_id_holder.pop()
        self.delete(id)
        id = self.stroke_line_id_holder.pop()

        id = self.coords_holder.pop()
        self.delete(id)
        stroke_number_var.set(int(stroke_number_var.get())-1)
        stroke_num_lbl.config(text="Stroke: "+str(stroke_number_var.get()))

    def clear_written_strokes(self):
        for id in self.stroke_line_id_holder:
            self.delete(id)
        for id in self.stroke_end_id_holder:
            self.delete(id)
        self.clear_stroke()

    def handle_stroke_storage(self):
        def store_stroke():
            ret_val = return_val.get()
            with open(self.csvfile_name, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=self.fieldnames)
                writer.writerow({"symbol_name":ret_val, "strokes":('-').join(self.coords_holder)})
            close_window(message_window)
            self.clear_written_strokes()

        message_window = Toplevel(root)
        message_window.grab_set()
        Label(message_window, text= "Enter the letter/symbol name!").grid(row=0, column=0)
        return_val = Entry(message_window)
        return_val.grid(row=1, column=0)
        submit_bttn = ttk.Button(message_window, text="Submit", command=store_stroke).grid(row=2, column=0)
        cancel_bttn = ttk.Button(message_window, text="Cancel", command=lambda: close_window(message_window)).grid(row=2, column=1)

    def set_current_letter(self, in_letter):
        current_letter_var.set(in_letter)
        self.letter_loaded = True
        self.show_outline()

                
    def show_outline(self):
        if self.letter_loaded:
            clear_canvas()
            if show_outline_var.get():
                with open(self.csvfile_name, 'r', newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        if row['symbol_name'] == current_letter_var.get():
                            hint_lbl['text'] = current_letter_var.get()
                            for stroke in row['strokes'].split('-'):
                                if show_arrows_var.get():
                                    self.create_line(*stroke.split(';'), 
                                        width=3, fill="grey", arrow=LAST, arrowshape=(10, 20, 10))
                                else:
                                    self.create_line(*stroke.split(';'), 
                                        width=3, fill="grey")
                    
    def change_pt_color_to_red(self, event):
        self.point_color = 'red'

    def change_pt_color_to_blue(self, event):
        self.point_color = 'blue'

    def draw_hor_guides(self):
        self.create_line((0, 100, 400, 100), width=3, fill='grey')
        self.create_line((0, 200, 400, 200), width=3, fill='grey', dash=(10,5))
        self.create_line((0, 300, 400, 300), width=3, fill='grey')

        self.create_line((0, 50, 400, 50), width=3, fill='light grey',  dash=(10,5))
        self.create_line((0, 350, 400, 350), width=3, fill='light grey',  dash=(10,5))
    
    def draw_vert_guides(self):
        self.create_line((100, 0, 100, 400), width=3, fill='light grey',  dash=(10,5))
        self.create_line((200, 0, 200, 400), width=3, fill='light grey',  dash=(10,5))
        self.create_line((300, 0, 300, 400), width=3, fill='light grey',  dash=(10,5))

    def draw_diag_guides(self):
        self.create_line((0, 0, 400, 400), width=3, fill='light grey',  dash=(10,5))
        self.create_line((400, 0, 0, 400), width=3, fill='light grey',  dash=(10,5))

###################################
###################################

langs_abr, langs = load_language_options()
langs_var = StringVar()

sketch = Stroke_canvas(stroke_canvas, width=400, height=400, language=langs_abr[0])
sketch.grid()

show_load_options(strokes_frame, langs_abr[0], sketch)

show_outline_bttn = ttk.Checkbutton(stroke_options, text="Outline", 
    variable=show_outline_var, onvalue=True, command=sketch.show_outline)
show_arrows_bttn = ttk.Checkbutton(stroke_options, text="Arrows", 
    variable=show_arrows_var, onvalue=True, command=sketch.show_outline)
clear_stroke_bttn = ttk.Button(stroke_options, text="Clear Stroke", command=sketch.clear_written_strokes)
clear_lst_stroke_bttn = ttk.Button(stroke_options, text="Clear Last", command=sketch.clear_last_stroke)
clear_bttn = ttk.Button(stroke_options, text="Clear All", command=clear_all)

show_outline_bttn.grid(column=0, row=1)
show_arrows_bttn.grid(column=1, row=1)
clear_stroke_bttn.grid(column=2, row=1)
clear_lst_stroke_bttn.grid(column=3, row=1)
clear_bttn.grid(column=4, row=1)

lang_dropown = ttk.OptionMenu(button_frame, langs_var, langs[0], *langs, command=lambda var=langs_var: show_load_options(letter_frame, var, sketch))
load_bttn = ttk.Button(button_frame, text="Load", command=lambda: load_strokes(button_frame, langs_var, sketch))
store_bttn = ttk.Button(button_frame, text="Store", command=sketch.handle_stroke_storage)
exit_bttn = ttk.Button(button_frame, text="Exit", command=lambda: close_window(root))

info_frame.grid(column=1, row=0)
strokes_frame.grid(column=2, row=0)
button_frame.grid(column=0, row=1)

name_lbl.grid(column=0, row=0)
hint_lbl.grid(column=0, row=1)
stroke_num_lbl.grid(column=0, row=2)

lang_dropown.grid(column=2, row=1)
load_bttn.grid(column=3, row=1)
store_bttn.grid(column=4, row=1)
exit_bttn.grid(column=5, row=1)

root.mainloop()
