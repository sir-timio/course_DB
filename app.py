import tkinter as tk
from tkinter import font as tkfont
from model import Entity
TK_SILENCE_DEPRECATION=1 
H, W = 750, 750
W_BIAS = 2800
BG = "#02abe3"
BTN_BG = "#121212"
TITLE = "Clinic"

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self._frame = None
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.eval("tk::PlaceWindow . center")
        self.geometry(f"{H}x{W}-{W_BIAS}+0")
        self.focus()
        self.switch_frame(MainPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class CalcPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text='Рассчет зарплаты сотрудника')
        label.pack(side='top', fill='x', pady=10)

        go_main_button = tk.Button(
            self, text='в главное меню',
            command=lambda: master.switch_frame(MainPage)
        )
        go_main_button.pack(pady=20)


class MainPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text='Главная страница')
        label.pack(side='top', fill='x', pady=10)
        
        go_calc_button = tk.Button(
            self, text='Перейти к калькулятору зарплат',
            command=lambda: master.switch_frame(CalcPage)
        )
        go_calc_button.pack(pady=20)

            

if __name__ == '__main__':
    app = App()
    app.mainloop()