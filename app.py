import tkinter as tk
from tkinter import Button, Entry, OptionMenu, ttk, Label
from tkinter import font as tkfont
from tkinter import messagebox
from attr import field
from click import command
import psycopg2 as psql

from tkinter import StringVar

from config import ICON_PATH
from PIL import ImageTk, Image
from model import Entity, Stuff, Job, Patient, Treatment, Price_list, Visit

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
        self.switch_frame(InsertVisitPage)


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
        
        calc_button = tk.Button(
            self, text='калькулятор зарплат',
            bg=BG,
            background=BG,
            command=lambda: self.master.switch_frame(CalcPage),
            highlightbackground=BTN_BG,
            # font=font,
            height=3,
        )
        calc_button.grid(row=1, column=1, padx=30, pady=30)


        insert_visit_button = tk.Button(
            self, text='внести визит',
            bg=BG,
            background=BG,
            command=lambda: self.master.switch_frame(InsertVisitPage),
            highlightbackground=BTN_BG,
            # font=font,
            height=3,
        )
        insert_visit_button.grid(row=1, column=3, padx=30, pady=30)


class InsertVisitPage(tk.Frame):
    def __init__(self, master):
            tk.Frame.__init__(self, master, width=W, height=H)
            label = tk.Label(self, text='Внести визит', font=font)
            label.grid(row=0, column=2, padx=20, pady=20)
            tk.Label(self, text='').grid(row=0, column=4,  padx=100, pady=10)
            self.pack()
            self.pack_propagate(0)
            self.master = master

            self.patient_id = None
            self.doctor_id = None
            self.visit_id = None
            self.room = StringVar()
            self.room.set('1')
            self.receipt = StringVar()
            self.receipt.set('')
            self.date = str(date.today())
            self.time = None    
            self.treatment_list = []

            self.set_go_menu()
            self.set_date_input(1, 'ввести прием', date(2022, 6, 1))
            self.set_receipt_room_input()
            self.set_drop_menu_doctor()
            self.set_drop_menu_patient()
            self.set_input_treatment()

            self.insert_visit()


    def set_receipt_room_input(self):

        receipt_entry = Entry(self, textvariable=self.receipt)
        receipt_entry.grid(row=5, column=1)
        Label(self, text='рецепт:').grid(row=5, column=0, sticky='E')

        room_entry = Entry(self, textvariable=self.room)
        room_entry.grid(row=6, column=1)
        Label(self, text='кабинет:').grid(row=6, column=0, sticky='E', pady=15)

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
            go_main_button.grid(row=15, column=0, sticky='W', pady=20, padx=20)
    
    def set_date_input(self, col, prefix, default_date):
        def set_date():
            self.date = str(cal.get_date())
            label.config(text=f'выбрано: {cal.get_date()}')

        label = ttk.Label(self, text=prefix)
        label.grid(row=7, column=col)
        cal = DateEntry(self, width=12, background='darkblue',
                        year=default_date.year,
                        month=default_date.month,
                        day=default_date.day,
                        foreground='white', borderwidth=2, )
        cal.grid(row=8, column=col)
        button = tk.Button(self, text='установить', command=lambda: set_date())
        button.grid(row=9, column=col, pady=20)
    
    def set_drop_menu_doctor(self):
        doctors = get_table(cls=Stuff)
        job = get_table(cls=Job)
        job_name = dict()
        job_salary = dict()
        for j in job:
            job_name[j.id] = j.name
        
        names = [s.get_name(job_name) for s in doctors if s.job == 3]

        clicked = StringVar()
        clicked.set('выбор мед. сотрудника')

        def on_select(choice):
            text = clicked.get()
            doctor_id, name = text.split(' ', 1)
            self.doctor_id = int(doctor_id)
            text = f'сотрудник: {name}'
            label.config(text=text)


        drop = OptionMenu(self, clicked, *names, command=on_select)
        drop.grid(row=1, column=1, padx=5, pady=5)
        label = Label(self, text=' ')
        label.grid(row=2, column=1, padx=5, pady=5)
    
    def set_drop_menu_patient(self):
        patients = get_table(cls=Patient)

        names = [p.get_name() for p in patients]

        
        clicked = StringVar()
        clicked.set('выбор пациента')

        def on_select(choice):
            text = clicked.get()
            patient_id, name = text.split(' ', 1)
            self.patient_id = int(patient_id)
            text = f'пациент: {name}'
            label.config(text=text)


        drop = OptionMenu(self, clicked, *names, command=on_select)
        drop.grid(row=3, column=1, padx=5, pady=5)
        label = Label(self, text=' ')
        label.grid(row=4, column=1, padx=5, pady=5)
    
    def insert_visit(self):
        def _insert_visit():
            visit = Visit(
                patient_id=self.patient_id,
                doctor_id=self.doctor_id,
                date=self.date,
                time=self.time,
                room=self.room.get(),
                receipt=self.receipt.get() or None
            )
            if len(self.treatment_list) == 0:
                ok = False
                err = 'Нет ни одной процедуры для визита'
                messagebox.showerror('Ошибка', err)
                return
            query = 'insert into visit'
            d = visit.get_data()
            fields = d.keys()
            values = list(d.values())
            query += ' (' + ', '.join(fields) + ')'
            query += ' values (' + ', '.join(['%s'] * len(values)) + ')'
            query += ' returning id;'
            conn = get_connection()
            try:
                with conn.cursor() as cur:
                    cur.execute(query, values)
                    conn.commit()
                    res = cur.fetchall()
                    self.visit_id = int(res[0][0])
                    print(self.visit_id)
            except Exception as ex:
                conn.rollback()
                print(f'Exception {ex} inserting visit')
                messagebox.showerror('ошибка', ex)
            for i in range(len(self.treatment_list)):
                self.treatment_list[i].visit_id = self.visit_id
            
            for t in self.treatment_list:
                insert(t)
  


        button = Button(self, text='внести визит', command=lambda: _insert_visit())
        button.grid(row=12, column=2)
# class Visit(Entity):
#     def __init__(
#         self,
#         patient_id: int,
#         doctor_id: int,
#         date: str = None,
#         time: str = None,
#         room: int = None,
#         receipt: str = None,


    def set_input_treatment(self):
        
        price_list  = get_table(cls=Price_list)
        names = [f'{p.code} {p.name}' for p in price_list]

        def on_select_treatment():
            text = clicked_treatment.get()
            code, name = text.split(' ', 1)
            code = int(code)
            text = f'добавлено!\nпроцедура: {name}'
            ok = True
            if quantity.get() != '':
                try:
                    q = int(quantity.get())
                    if q < 1:
                        text += '\nнекорректное количество, введите число'
                        q = None
                        ok = False
                    else:
                        text += f'\nколичество: {q}'
                except:
                    ok = False
                    text += '\nнекорректное количество'
            if location.get() != '':
                try:
                    l = int(location.get())
                    if 0 < l < 32:
                        text += f'\nкод зуба: {l}'
                    else:
                        l = None
                        ok = False
                        text += '\nнекорретный код зуба'
                except:
                    l = None
                    ok = False
                    text += '\nнекорретный код зуба, введите число'
            if ok:
                self.treatment_list.append(
                    Treatment(id=None, visit_id=self.visit_id, code=code, location=l, quantity=q)
                )
                label.config(text=text)
        clicked_treatment = StringVar()
        clicked_treatment.set('выбор процедуры')

        drop_treatment = OptionMenu(self, clicked_treatment, *names)
        drop_treatment.grid(row=1, column=3, columnspan=2)

        quantity = StringVar()
        quantity.set('1')
        quantity_entry = Entry(self, textvariable=quantity)
        quantity_entry.grid(row=2, column=4, padx=20)
        Label(self, text='количество:').grid(row=2, column=3, sticky='E')

        location = StringVar()
        location.set('1')
        location_entry = Entry(self, textvariable=location)
        location_entry.grid(row=3, column=4)
        Label(self, text='код зуба:').grid(row=3, column=3, sticky='E')
    
        button = Button(self, text='добавить', command=lambda: on_select_treatment())
        button.grid(row=4, column=4)
        label = Label(self, text=' ')
        label.grid(row=5, column=4)

class CalcPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, width=W, height=H)
        label = tk.Label(self, text='Рассчет зарплаты сотрудника', font=font)
        label.grid(row=0, column=1, padx=20, pady=20)
        # tk.Label(self, text='').grid(row=1, column=4,  padx=100, pady=30)
        self.pack()
        self.pack_propagate(0)
        self.master = master

        self.stuff_id = None
        self.salary = None
        self.interest_rate = 0
        self.start_date = None
        self.end_date = None

        self.set_drop_menu()

        self.set_date_input(0, 'начальная дата', date(2022, 6, 1), is_start=1)
        self.set_date_input(2, 'конечная дата', date.today())

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
        go_main_button.grid(row=10, column=0, pady=20, padx=30)

    def set_drop_menu(self):
        stuff = get_table(cls=Stuff)
        job = get_table(cls=Job)
        job_name = dict()
        job_salary = dict()
        for j in job:
            job_name[j.id] = j.name
            job_salary[j.id] = j.daily_salary
        

        names = [s.get_name(job_name) for s in stuff]
        for s in stuff:
            pass
        clicked = StringVar()
        clicked.set('выбор сотрудника')

        def on_select(choice):
            text = clicked.get()
            stuff_id, name = text.split(' ', 1)
            self.stuff_id = int(stuff_id)
            st = get_row(Stuff, self.stuff_id)
            self.salary = job_salary[st.job]
            text = f'сотрудник: {name}\nсмена: {self.salary}'
            if st.interest_rate != 0:
                self.interest_rate = st.interest_rate
                text += f', {round(self.interest_rate*100, 2)}%'
            
            label.config(text=text)


        drop = OptionMenu(self, clicked, *names, command=on_select)
        drop.grid(row=1, column=1, padx=10, pady=40)
        label = Label(self, text=' ')
        label.grid(row=2, column=1, padx=10, pady=40)
    
    def set_calc_button(self):
        def calc():
            if (self.stuff_id is None or
                self.start_date is None or
                self.end_date is None or
                self.salary is None):
                    label.config(text='недостаточно данных для рассчета')
                    return

            query_workdays = f'''select stuff_id, date from stuff_workdays where
                        stuff_id = {self.stuff_id} and
                        date between '{self.start_date}' and '{self.end_date}';'''
            try:
                conn = get_connection()
                with conn.cursor() as cur:
                    cur.execute(query_workdays)
                    conn.commit()
                    days = len(cur.fetchall())
            except Exception as ex:
                print(f'Cannot select workddays: {ex}')
                conn.rollback()
                return
            
            total_salary = days * self.salary

            if self.interest_rate != 0:
                query_visits = f'''
                select name, price, quantity from visit v
                    inner join treatment tr on tr.visit_id = v.id
                    inner join price_list p on p.code = tr.code
                where v.doctor_id = {self.stuff_id} and
                    v.date between '{self.start_date}' and '{self.end_date}';
                '''
                try:
                    conn = get_connection()
                    with conn.cursor() as cur:
                        cur.execute(query_visits)
                        conn.commit()
                        rows = cur.fetchall()
                        for row in rows:
                            _, price, quantity = str(row[0]), float(row[1]), int(row[2])
                            total_salary += price * quantity * self.interest_rate
                            
                except Exception as ex:
                    print(f'Cannot select visits: {ex}')
                    conn.rollback()
                    return
            
            label.config(text=f'итого: {round(total_salary)}')

        label = Label(self, text=' ')
        button = Button(self, text='рассчет', command=lambda: calc())
        button.grid(row=6, column=1)
        label.grid(row=7, column=1, pady=10, padx=10)

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

def insert(entity: Entity, conn=get_connection()):
    table_name = entity.__class__.__name__.lower()
    query = f'insert into {table_name}'
    d = entity.get_data()
    fields = d.keys()
    values = list(d.values())
    query += ' (' + ','.join(fields) + ')'
    query += ' values (' + ','.join(['%s'] * len(values)) + ');'
    try:
        with conn.cursor() as cur:
            cur.execute(query, values)
            conn.commit()
        return 1, ''
    except Exception as ex:
        conn.rollback()
        print(f"Exeption in insert: {ex} for table {table_name} with entity {entity}")
        return 0, ex


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

def get_workdays_amount(stuff_id, start_date, end_date, conn=get_connection()):
    query = f'''select stuff_id, date from stuff_workdays where
                 stuff_id = {stuff_id} and
                 date between {start_date} and {end_date}'''
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit();
            rows = cur.fetchall()
            return len(rows)
    except:
        conn.rollback()

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