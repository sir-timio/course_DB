import tkinter as tk
from tkinter import Button, Entry, OptionMenu, ttk, Label, messagebox, StringVar
from tkinter import font as tkfont

import psycopg2 as psql
from model import Entity, MedicalCart, Stuff, Job, Patient, Treatment, Price_list, Visit, Workdays

from tkcalendar import DateEntry
from datetime import date, time
import re
from config import config

FONT = 'Arial 16'

TIME_REGEX = '^([0-1]?[0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?$'
PHONE_REGEX = '^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
PERCENT_REGEX = '^(\d+(\.\d+)?%)$'
TK_SILENCE_DEPRECATION=1 
W, H = 1280, 720
W_BIAS = 2560
BG = "#79def7"
BTN_BG = "#3dffc2"
LBL_BG = "#79def7"
TITLE = "Clinic"
def init_db():
    conn = psql.connect(**config)
    try:
        with conn.cursor() as cur:
            cur.execute(open('init_db.sql', 'r').read())
            conn.commit()
    except Exception as ex:
        print(f'Error in init tables: {ex}')


    
##################################################
#                                                #
#               App                              # 
#                                                #
##################################################

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._frame = None
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.eval("tk::PlaceWindow . center")
        self.geometry(f"{W}x{H}-{W_BIAS}+0")
        self.configure(background=BG)
        self.title('MedOK')
        self.focus()
        self.switch_frame(MainPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack_propagate(0)
        self._frame.pack()
    
    
##################################################
#                                                #
#               Main Page                        # 
#                                                #
##################################################

class MainPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        label = tk.Label(self, text='Главная страница', bg=LBL_BG)
        label.grid(row=0, column=1, pady=30, padx=30)
        
        insert_stuff_button = tk.Button(
            self, text='внести сотрудника',
            bg=BG, background=BG,
            command=lambda: self.master.switch_frame(InsertStuffPage),
            highlightbackground=BTN_BG, height=3,
        )
        insert_stuff_button.grid(row=1, column=0, padx=30, pady=30)

        insert_patient_button = tk.Button(
            self, text='внести пациента',
            bg=BG, background=BG,
            command=lambda: self.master.switch_frame(InsertPatientPage),
            highlightbackground=BTN_BG, height=3,
        )
        insert_patient_button.grid(row=1, column=1, padx=30, pady=30)

        calc_button = tk.Button(
            self, text='калькулятор зарплат',
            bg=BG, background=BG,
            command=lambda: self.master.switch_frame(CalcPage),
            highlightbackground=BTN_BG, height=3,
        )
        calc_button.grid(row=2, column=1, padx=30, pady=30)

        insert_visit_button = tk.Button(
            self, text='внести визит',
            bg=BG, background=BG,
            command=lambda: self.master.switch_frame(InsertVisitPage),
            highlightbackground=BTN_BG, height=3,
        )
        insert_visit_button.grid(row=1, column=2, padx=30, pady=30)



    
##################################################
#                                                #
#               Visit Page                       # 
#                                                #
##################################################

class InsertVisitPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, width=W, height=H)
        label = tk.Label(self, text='Внести визит', font=FONT)
        label.grid(row=0, column=2, padx=20, pady=20)
        tk.Label(self, text='').grid(row=0, column=4,  padx=100, pady=10)
        self.pack()
        self.pack_propagate(0)
        self.master = master

        self.patient_id = None
        self.doctor_id = None
        self.visit_id = None
        self.date = str(date.today())

        self.treatment_list = []
        # self.treatment_list_label = tk.Label(self, text='список процедур: ', font=FONT)
        # self.treatment_list_label.grid(row=5, column=4)
        stuff = get_table(cls=Stuff)
        doctors = dict((k, v) for k, v in stuff.items() if v.is_doctor())
        doctor_names = [s.get_name() for s in doctors.values()]
        self.doctor_to_id = dict(zip(doctor_names, doctors.keys()))

        patient = get_table(cls=Patient)
        patients = dict((k, v) for k, v in patient.items())
        patient_names = [s.get_name() for s in patients.values()]
        self.patient_to_id =  dict(zip(patient_names, patients.keys()))
        self.set_drop_input(
            ['doctor_name', 'patient_name'],
            ['выберите врача', 'выберите пациента'],
            [doctor_names, patient_names],
            ['врач', 'пациент'],
            row=2, col=0
        )

        self.set_input(
            ['room', 'receipt', 'time'],
            ['кабинет', 'рецепт', 'время начала приема'],
            ['1', '', '12:00'],
            row=4,
            col=0,
        )
        self.set_date_input(1, 8, 'ввести прием', date(2022, 6, 1))


        self.set_input_treatment()
        self.insert_visit()
        self.set_go_menu()


    def set_input(self, fields, names, dummies=None, row=5, col=0):
        if dummies is None:
            dummies = [''] * len(names)
        for i, t in enumerate(zip(fields, names, dummies)):
            field, name, dummy = t

            self.__dict__[field] = StringVar()
            self.__dict__[field].set(dummy)
            Label(self, text=f'{name}:').grid(row=row+i, column=col, sticky='E')
            entry = Entry(self, textvariable=self.__dict__[field])
            entry.grid(row=row+i, column=col+1)

    def set_drop_input(self, fields, names, options, labels=None, row=5, col=2):
        if labels is None:
            labels = [''] * len(names)
        for i, t in enumerate(zip(fields, names, options, labels)):
            field, name, ops, label = t
            self.__dict__[field] = StringVar()
            drop = OptionMenu(self, self.__dict__[field], *ops)
            self.__dict__[field].set(name)
            Label(self, text=f'{label}:').grid(row=row+i, column=col, sticky='E')
            drop.grid(row=row+i, column=col+1)
            
    def set_go_menu(self):
            go_main_button = tk.Button(
                self, text='в главное меню',
                bg=BG,
                background=BG,
                command=lambda: self.master.switch_frame(MainPage),
                highlightbackground=BTN_BG,
                font=FONT,
                height=3,
            )
            go_main_button.grid(row=15, column=0, sticky='W', pady=20, padx=20)
    
    def set_date_input(self, col, row, prefix, default_date=date.today()):
        def set_date():
            self.date = str(cal.get_date())
            label.config(text=f'выбрано: {cal.get_date()}')

        label = ttk.Label(self, text=prefix)
        label.grid(row=row, column=col)
        cal = DateEntry(self, width=12, background='darkblue',
                        year=default_date.year,
                        month=default_date.month,
                        day=default_date.day,
                        foreground='white', borderwidth=2, )
        cal.grid(row=row+1, column=col)
        button = tk.Button(self, text='установить', command=lambda: set_date())
        button.grid(row=row+2, column=col, pady=20)
    
    def insert_visit(self):
        def _insert_visit():
            self.patient_id = self.patient_to_id.get(self.patient_name.get())
            self.doctor_id = self.doctor_to_id.get(self.doctor_name.get())
            if len(self.treatment_list) == 0:
                messagebox.showerror('Ошибка', 'Нет ни одной процедуры для визита')
                return
            if not self.patient_id:
                messagebox.showerror('Ошибка', 'Внесите пациента')
                return
            if not self.doctor_id:
                messagebox.showerror('Ошибка', 'Внесите врача')
                return
            if not re.fullmatch(TIME_REGEX, self.time.get()):
                messagebox.showerror('Ошибка', 'Введите корректно время в формате hh:mm:ss')
                return
            visit = Visit(
                patient_id=self.patient_id,
                doctor_id=self.doctor_id,
                date=self.date,
                time=self.time.get(),
                room=self.room.get(),
                receipt=self.receipt.get() or None
            )
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
            except Exception as ex:
                conn.rollback()
                print(f'Exception {ex} inserting visit')
                messagebox.showerror('ошибка', ex)
                return
            for i in range(len(self.treatment_list)):
                self.treatment_list[i].visit_id = self.visit_id
            
            for t in self.treatment_list:
                ex = insert(t)
                if ex:
                    return
            messagebox.showinfo('Визит внесен', 'успешно внесен визит')
  


        button = Button(self, text='внести визит', command=lambda: _insert_visit())
        button.grid(row=12, column=2)

    def set_input_treatment(self):
        
        price_list  = get_table(cls=Price_list)
        names = [p.name for p in price_list.values()]
        name_to_id = dict(zip(names, price_list.keys()))
        self.treatment_list_str = ''
        def on_select_treatment():
            text = clicked_treatment.get()
            name = text
            price_list_id = int(name_to_id.get(name))
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
                    Treatment(id=None, visit_id=self.visit_id, price_list_id=price_list_id, location=l, quantity=q)
                )
                text += '\n\n'
                self.treatment_list_str += f'{name} x {q}\n'
                text += 'список процедур:\n' + self.treatment_list_str
                label.config(text=text)
                
        clicked_treatment = StringVar(self)
        clicked_treatment.set('выбор процедуры')

        drop_treatment = OptionMenu(self, clicked_treatment, *names)
        drop_treatment.grid(row=1, column=3, columnspan=2)

        quantity = StringVar(self)
        quantity.set('1')
        quantity_entry = Entry(self, textvariable=quantity)
        quantity_entry.grid(row=2, column=4, padx=20)
        Label(self, text='количество:').grid(row=2, column=3, sticky='E')

        location = StringVar(self)
        location.set('1')
        location_entry = Entry(self, textvariable=location)
        location_entry.grid(row=3, column=4)
        Label(self, text='код зуба:').grid(row=3, column=3, sticky='E')
    
        button = Button(self, text='добавить', command=lambda: on_select_treatment())
        button.grid(row=4, column=4)
        label = Label(self, text=' ', anchor="e", justify=tk.LEFT)
        label.grid(row=5, column=4)

        

    
##################################################
#                                                #
#               Patient Page                     # 
#                                                #
##################################################

class InsertPatientPage(tk.Frame):
    def __init__(self, master):
            tk.Frame.__init__(self, master, width=W, height=H)
            label = tk.Label(self, text='Внести пациента', font=FONT)
            label.grid(row=0, column=1, padx=20, pady=20)
            self.pack()
            self.pack_propagate(0)
            self.master = master

            self.set_go_menu()
            self.set_input(
                ['name', 'surname', 'phone'],
                ['имя', 'фамилия', 'номер телефона'],
                ['Иван', 'Иванов', '+7(963)610-20-30'],
                row=2,
                col=0
            )
            self.set_input(
                ['allergy', 'diseases', 'medicines'],
                ['аллергия', 'хронические заболевания',
                    'принимаемые препараты'],
                col=2,
                row=2
            )
            self.set_drop_input(
                ['sex', 'blood_type'],
                ['пол', 'группа крови'],
                [
                    ['M', 'F'],
                    ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
                ],

                col=3,
                row=5
            )
            self.insert_patient()
            self.set_bdate_input(col=1, row=5, prefix='дата рождения: ')


    def set_drop_input(self, fields, names, options, row=5, col=2):
        for i, t in enumerate(zip(fields, names, options)):
            field, name, ops = t
            self.__dict__[field] = StringVar()
            drop = OptionMenu(self, self.__dict__[field], *ops)
            self.__dict__[field].set(name)
            drop.grid(row=row+i, column=col)

    def set_input(self, fields, names, dummies=None, row=5, col=0):
        if dummies is None:
            dummies = [''] * len(names)
        for i, t in enumerate(zip(fields, names, dummies)):
            field, name, dummy = t

            self.__dict__[field] = StringVar()
            self.__dict__[field].set(dummy)
            Label(self, text=f'{name}:').grid(row=row+i, column=col, sticky='E')
            entry = Entry(self, textvariable=self.__dict__[field])
            entry.grid(row=row+i, column=col+1)

    def set_go_menu(self):
            go_main_button = tk.Button(
                self, text='в главное меню',
                bg=BG,
                background=BG,
                command=lambda: self.master.switch_frame(MainPage),
                highlightbackground=BTN_BG,
                font=FONT,
                height=3,
            )
            go_main_button.grid(row=15, column=0, sticky='W')
    
    def set_bdate_input(self, col, row, prefix, default_date=date.today()):
        def set_date():
            self.birth_date = str(cal.get_date())
            label.config(text=f'выбрано: {cal.get_date()}')

        label = ttk.Label(self, text=prefix)
        label.grid(row=row, column=col)
        cal = DateEntry(self, width=12, background='white',
                        year=default_date.year,
                        month=default_date.month,
                        day=default_date.day,
                        foreground='white', borderwidth=2, )
        cal.grid(row=row+1, column=col)
        button = tk.Button(self, text='установить', command=lambda: set_date())
        button.grid(row=row+2, column=col)
    
    def insert_patient(self):
        def _insert():
            patient = Patient(
                id=None,
                name=self.name.get(),
                surname=self.surname.get(),
                phone=self.phone.get(),
            )

            if not re.fullmatch(PHONE_REGEX, self.phone.get()):
                messagebox.showerror('Ошибка', 'Введите корректный номер телефона')
                return

            medical_cart = MedicalCart(
                id=None,
                sex=self.sex.get(),
                blood_type=self.blood_type.get(),
                birth_date=self.birth_date,
                allergy=self.allergy.get(),
                diseases=self.diseases.get(),
                medicines=self.medicines.get(),
            )
            
            query = 'insert into patient'
            d = patient.get_data()
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
                    self.id = int(res[0][0])

                    medical_cart.id = self.id
                    query = 'insert into medical_card'
                    d = medical_cart.get_data()
                    fields = d.keys()
                    values = list(d.values())
                    query += ' (' + ', '.join(fields) + ')'
                    query += ' values (' + ', '.join(['%s'] * len(values)) + ')'

                    print(query)
                    print(values)
                    cur.execute(query, values)
                    conn.commit()
            except Exception as ex:
                conn.rollback()
                print(f'Exception {ex} inserting patient')
                messagebox.showerror('ошибка', ex)
                return
 
            messagebox.showinfo('Пациент внесен', 'успешно внесен пациент')

        button = Button(self, text='внести пациента', command=lambda: _insert())
        button.grid(row=12, column=2)

##################################################
#                                                #
#               Stuff Page                       # 
#                                                #
##################################################  

class InsertStuffPage(tk.Frame):
    def __init__(self, master):
    
        tk.Frame.__init__(self, master, width=W, height=H)
        label = tk.Label(self, text='Внести сотрудника', font=FONT)
        label.grid(row=0, column=1, padx=20, pady=20)
        self.pack()
        self.pack_propagate(0)
        self.master = master
        self.interest_rate = 0
        self.set_go_menu()
        self.set_input(
            ['name', 'surname', 'phone'],
            ['имя', 'фамилия', 'номер телефона'],
            ['Иван', 'Иванов', '+7(963)610-20-30'],
            row=2,
            col=0
        )
        self.set_input(
            ['license', 'workdays', 'interest_rate'],
            ['лицензия', 'рабочие дни', 'проц. ставка'],
            ['UNI123-412-423', 'пн, вт, ср, чт, пт', '0%'],
            col=2,
            row=2
        )
        job = get_table(cls=Job)
        job_names = [s.get_name() for s in job.values()]
        self.job_to_id =  dict(zip(job_names, job.keys()))

        self.set_drop_input(
            ['job_name'],
            ['должность'],
            [
                ['врач', 'медсестра', 'администратор'],
            ],

            col=3,
            row=5
        )
        self.insert_stuff()
        self.set_bdate_input(col=1, row=5, prefix='дата рождения: ')


    def set_drop_input(self, fields, names, options, row=5, col=2):
        for i, t in enumerate(zip(fields, names, options)):
            field, name, ops = t
            self.__dict__[field] = StringVar()
            drop = OptionMenu(self, self.__dict__[field], *ops)
            self.__dict__[field].set(name)
            drop.grid(row=row+i, column=col)

    def set_input(self, fields, names, dummies=None, row=5, col=0):
        if dummies is None:
            dummies = [''] * len(names)
        for i, t in enumerate(zip(fields, names, dummies)):
            field, name, dummy = t

            self.__dict__[field] = StringVar()
            self.__dict__[field].set(dummy)
            Label(self, text=f'{name}:').grid(row=row+i, column=col, sticky='E')
            entry = Entry(self, textvariable=self.__dict__[field])
            entry.grid(row=row+i, column=col+1)

    def set_go_menu(self):
            go_main_button = tk.Button(
                self, text='в главное меню',
                bg=BG,
                background=BG,
                command=lambda: self.master.switch_frame(MainPage),
                highlightbackground=BTN_BG,
                font=FONT,
                height=3,
            )
            go_main_button.grid(row=15, column=0, sticky='W')
    
    def set_bdate_input(self, col, row, prefix, default_date=date.today()):
        def set_date():
            self.birth_date = str(cal.get_date())
            label.config(text=f'выбрано: {cal.get_date()}')

        label = ttk.Label(self, text=prefix)
        label.grid(row=row, column=col)
        cal = DateEntry(self, width=12, background='white',
                        year=default_date.year,
                        month=default_date.month,
                        day=default_date.day,
                        foreground='white', borderwidth=2, )
        cal.grid(row=row+1, column=col)
        button = tk.Button(self, text='установить', command=lambda: set_date())
        button.grid(row=row+2, column=col)
    
    def insert_stuff(self):
        def _insert():
            if not re.fullmatch(PHONE_REGEX, self.phone.get()):
                messagebox.showerror('Ошибка', 'Введите корректный номер телефона')
                return
            
            if not re.fullmatch(PERCENT_REGEX, self.interest_rate.get()) or\
                    0 > float(self.interest_rate.get()[:-1]) > 100:
                messagebox.showerror('Ошибка', 'Введите корректную процентную ставку')
                return

                
            stuff = Stuff(
                id=None,
                name=self.name.get(),
                surname=self.surname.get(),
                phone=self.phone.get(),
                job_id=self.job_to_id.get(self.job_name.get()),
                interest_rate=float(self.interest_rate.get()[:-1])/100,
            )

            query = 'insert into stuff'
            d = stuff.get_data()
            fields = d.keys()
            values = list(d.values())
            query += ' (' + ', '.join(fields) + ')'
            query += ' values (' + ', '.join(['%s'] * len(values)) + ')'
            query += ' returning id;'
            conn = get_connection()

            workday = Workdays(
                stuff_id=None,
                date=None,
                id=None
            )
            day_codes = [workday.get_day_code(s.strip()) for s in self.workdays.get().split(',')]
            try:
                with conn.cursor() as cur:
                    cur.execute(query, values)
                    conn.commit()
                    res = cur.fetchall()
                    stuff_id = str(res[0][0])
                    workday_interval = '(' + ','.join(day_codes) + ')'
                    query = 'insert into stuff_workdays(stuff_id, date)'
                    query += f'''
                    with days as
                    (
                        select dd, extract(DOW from dd) dw
                        from generate_series('{date.today()}'::date, '2050-05-02'::date, '1 day'::interval) dd
                    )
                    select {stuff_id}, dd
                    from   days
                    where  dw in {workday_interval};
                    '''
                    cur.execute(query)
                    conn.commit()
            except Exception as ex:
                conn.rollback()
                print(f'Exception {ex} inserting stuff')
                messagebox.showerror('ошибка', ex)
                return
 
            messagebox.showinfo('Сотдруник внесен', 'успешно внесен сотрудник')

        button = Button(self, text='внести сотрудника', command=lambda: _insert())
        button.grid(row=12, column=2)


##################################################
#                                                #
#               Calculator Page                  # 
#                                                #
##################################################

class CalcPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, width=W, height=H)
        label = tk.Label(self, text='Рассчет зарплаты сотрудника', font=FONT)
        label.grid(row=0, column=1, padx=20, pady=20)
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
            font=FONT,
            height=3,
        )
        go_main_button.grid(row=10, column=0, pady=20, padx=30)

    def set_drop_menu(self):
        stuff = get_table(cls=Stuff)
        job = get_table(cls=Job)
        names = [s.get_name(job) for s in stuff.values()]
        name_to_id = dict(zip(names, stuff.keys()))
        clicked = StringVar(self)
        clicked.set('выбор сотрудника')

        def on_select(choice):
            text = clicked.get()
            name = text
            self.stuff_id = int(name_to_id.get(name))
            st = stuff.get(self.stuff_id)
            self.salary = job[st.job_id].daily_salary
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
                    label.config(text='недостаточно данных для расчета')
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
            
            base_salary = days * self.salary
            from_visits = 0

            if self.interest_rate != 0:
                query_visits = f'''
                select name, price, quantity from visit v
                    inner join treatment tr on tr.visit_id = v.id
                    inner join price_list p on p.id = tr.id
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
                            from_visits += price * quantity * self.interest_rate                            
                except Exception as ex:
                    print(f'Cannot select visits: {ex}')
                    conn.rollback()
                    return
            text = f'итого за смены: {round(base_salary)}'
            if from_visits:
                text += f'\nитого за визиты: {round(from_visits)}'
                text += f'\nитого: {round(base_salary + from_visits)}'
            label.config(text=text)

        label = Label(self, text=' ')
        button = Button(self, text='расчет', command=lambda: calc())
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
        label.grid(row=3, column=col, padx=10)
        cal = DateEntry(self, width=12, background=BG,
                        year=default_date.year,
                        month=default_date.month,
                        day=default_date.day,
                        foreground='black', borderwidth=2)
        cal.grid(row=4, column=col)
        button = tk.Button(self, text='установить', command=lambda: print_date())
        button.grid(row=5, column=col, pady=5, padx=10)

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
        return 0
    except Exception as ex:
        conn.rollback()
        print(f"Exeption in insert: {ex} for table {table_name} with entity {entity}")
        return ex


def get_table(cls, conn=get_connection()):
    table_name = cls.__name__.lower()
    query = f'select * from {table_name}'
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
            rows = cur.fetchall()
            entities = [cls(*r) for r in rows]
            table = dict()
            for e in entities:
                table[e.id] = e
            return table
    except Exception as ex:
        conn.rollback()
        print(f"Exeption select: {ex} for table {table_name}")
        return None



            

if __name__ == '__main__':
    app = App()
    init_db()
    app.mainloop()