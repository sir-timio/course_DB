import tkinter as tk
from tkinter import Button, OptionMenu, ttk, Label
from tkinter import font as tkfont
import psycopg2 as psql

from tkinter import StringVar

from config import ICON_PATH
from PIL import ImageTk, Image
from model import Entity, Stuff

from tkcalendar import Calendar, DateEntry
from datetime import date

font = 'Arial 16'


from config import config

TK_SILENCE_DEPRECATION=1 
W, H = 1280, 720
W_BIAS = 2560
BG = "#79def7"
BTN_BG = "#3dffc2"
LBL_BG = "#79def7"
TITLE = "Clinic"

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # tk.Tk.__init__(self, *args, **kwargs)
        self._frame = None
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.eval("tk::PlaceWindow . center")
        self.geometry(f"{W}x{H}-{W_BIAS}+0")
        self.configure(background=BG)
        self.focus()
        # self.switch_frame(MainPage)
        self.switch_frame(CalcPage)


    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack_propagate(0)
        self._frame.pack()
    


class MainPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        label = tk.Label(self, text='Главная страница', bg=LBL_BG)
        label.grid(row=0, column=2, pady=30, padx=30)
        
        go_calc_button = tk.Button(
            self, text='калькулятор зарплат',
            bg=BG,
            background=BG,
            command=lambda: self.master.switch_frame(CalcPage),
            highlightbackground=BTN_BG,
            # font=font,
            height=3,
        )
        go_calc_button.grid(row=1, column=2, padx=30, pady=30)

class CalcPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, width=W, height=H)
        label = tk.Label(self, text='Рассчет зарплаты сотрудника', font=font)
        label.grid(row=0, column=1, sticky='W', padx=20, pady=20)
        tk.Label(self, text='').grid(row=0, column=4,  padx=100, pady=30)
        self.pack()
        self.pack_propagate(0)
        self.master = master

        self.stuff_id = None
        self.start_date = date(2022, 6, 1)
        self.end_date = date.today()

        self.set_drop_menu()
        
        self.set_date_input(1, 'начальная дата', self.start_date, is_start=1)
        self.set_date_input(2, 'конечная дата', self.end_date)

        self.set_go_menu()

        self.set_calc_button()


    def set_go_menu(self):
        go_main_button = tk.Button(
            self, text='в главное меню',
            bg=BG,
            background=BG,
            command=lambda: self.master.switch_frame(MainPage),
            highlightbackground=BTN_BG,
            font=font,
            height=3,
        )
        go_main_button.grid(row=10, column=0, sticky='W', pady=20, padx=30)

    def set_drop_menu(self):
        stuff = get_table(cls=Stuff)
        names = [s.get_name() for s in stuff]
        clicked = StringVar()
        clicked.set(names[0])
        self.stuff_id = int(names[0].split()[0])

        def on_click():
            text = clicked.get()
            label.config(text=text)
            self.stuff_id = int(text.split()[0])
            st = get_row(Stuff, self.stuff_id)
            print(st.get_data())

        drop = OptionMenu(self, clicked, *names)
        drop.grid(row=1, column=1, padx=5, pady=20)
        label = Label(self, text=' ')
        button = Button(self, text='выбрать сотрудника', command=lambda: on_click())
        button.grid(row=1, column=2)
        label.grid(row=2, column=1, padx=5, pady=20)
    
    def set_calc_button(self):
        
        def calc():
            if self.stuff_id and self.start_date and self.end_date:
                pass
            else:
                pass
            label.config(text='итого: ')
        label = Label(self, text=' ')
        button = Button(self, text='рассчет', command=lambda: calc())
        button.grid(row=6, column=2)
        label.grid(row=6, column=1, pady=10, padx=20)


    def set_date_input(self, col, prefix, default_date, is_start=0):
        def print_date():
            label.config(text=f'{prefix}: {cal.get_date()}')
            if is_start:
                self.start_date = cal.get_date()
            else:
                self.end_date = cal.get_date()

        label = ttk.Label(self, text=prefix)
        label.grid(row=3, column=col)
        cal = DateEntry(self, width=12, background='darkblue',
                        year=default_date.year,
                        month=default_date.month,
                        day=default_date.day,
                        foreground='white', borderwidth=2, )
        cal.grid(row=4, column=col)
        button = tk.Button(self, text='установить', command=lambda: print_date())
        button.grid(row=5, column=col, pady=5)

def get_connection(config=config):
    try:
        conn = psql.connect(**config)
        return conn
    except Exception as ex:
        print(f'Cannot connect: {ex}')
        return None

def get_table(cls, conn=get_connection()):
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


def get_row(cls, id, id_col_name='id', conn=get_connection()):
    table_name = cls.__name__.lower()
    query = f'select * from {table_name} where {id_col_name} = {id}'
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
            rows = cur.fetchall()
            entity = cls(*rows[0])
            return entity
    except Exception as ex:
        conn.rollback()
        print(f"Exeption get row: {ex} for table {table_name} id: {id}")
        return None

            

if __name__ == '__main__':
    app = App()
    app.mainloop()