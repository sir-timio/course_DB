import tkinter as tk
from tkinter import Button, OptionMenu, ttk, Label
from tkinter import font as tkfont
import psycopg2 as psql

from tkinter import StringVar

from config import ICON_PATH
from PIL import ImageTk, Image
from model import Entity, Stuff

from tkcalendar import Calendar, DateEntry


from config import config

TK_SILENCE_DEPRECATION=1 
H, W = 750, 750
W_BIAS = 2800
BG = "#02abe3"
BTN_BG = "#000000"
TITLE = "Clinic"

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # tk.Tk.__init__(self, *args, **kwargs)
        self.config = config
        self._frame = None
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.eval("tk::PlaceWindow . center")
        self.geometry(f"{H}x{W}-{W_BIAS}+0")
        self.configure(background=BG)
        self.focus()
        self.switch_frame(MainPage)

    def switch_frame(self, frame_class):
        
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
    


class MainPage(tk.Frame):
    def __init__(self, master):
        global img
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text='Главная страница')
        label.pack(side='top', fill='x', pady=10)
        
        go_calc_button = tk.Button(
            self, text='Перейти к калькулятору зарплат',
            bg=BG, fg='green',
            command=lambda: master.switch_frame(CalcPage),
            highlightbackground='#3E4149'
        )
        go_calc_button.place(width=100, height=20)
        go_calc_button.pack(pady=10)





class CalcPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text='Рассчет зарплаты сотрудника')
        label.pack(side='top', fill='x', pady=10)
        self.master = master
        
        self.set_go_menu()

        self.set_drop_menu()

        self.set_date_input()
    
    def set_drop_menu(self):
        stuff = get_table(conn=get_connection(), cls=Stuff)
        names = [s.get_name() for s in stuff]
        clicked = StringVar() 
        clicked.set(names[0])

        drop = OptionMenu(self, clicked, *names)
        drop.pack()
        label = Label(self, text=' ')
        button = Button(self, text='Выбрать сотрудника', command=lambda: label.config(text=clicked.get())).pack()
        label.pack()
    
    def set_go_menu(self):
        go_main_button = tk.Button(
            self, text='в главное меню',
            bg=BG,
            command=lambda: self.master.switch_frame(MainPage)
        )
        go_main_button.pack(pady=10)

    def set_date_input(self):
        cal = Calendar(self, selectmode='day', year=2022, month=6, day=1)
        cal.pack(pady=50)

        def get_date():
            label.config(text=cal.get_date())
    
        button = Button(self, text='начало', command=get_date)
        button.pack(pady=50)

        label = Label(self, text='')
        label.pack(pady=50)

def get_connection(config=config):
    try:
        conn = psql.connect(**config)
        return conn
    except Exception as ex:
        print(f'Cannot connect: {ex}')
        return None

def get_table(conn, cls):
    conn = get_connection()
    table_name = cls.__name__.lower()
    query = f'select * from {table_name}'
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
            rows = cur.fetchall()
            entities = [cls(*r) for r in rows]
            return entities
    except Exception as ex:
        conn.rollback()
        print(f"Exeption select: {ex} for table {table_name}")
        return None



            

if __name__ == '__main__':
    app = App()
    app.mainloop()