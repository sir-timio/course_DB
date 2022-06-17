import tkinter as tk
TK_SILENCE_DEPRECATION=1 
H, W = 750, 750
W_BIAS = 2800
BG = "#02abe3"
BTN_BG = "#000000"
TITLE = "Clinic"

def make_root():
    root = tk.Tk()
    root.title(TITLE)
    root.eval("tk::PlaceWindow . center")
    root.geometry(f"{H}x{W}-{W_BIAS}+0")
    root.focus()
    return root

def load_add_frame():
    print('add menu')

def load_main_frame(root):
    frame1 = tk.Frame(root, width=W, height=W, bg=BG)
    frame1.grid(row=0, column=0)
    frame1.pack_propagate(False)

    tk.Button(
        frame1,
        text="add doctor",
        font=("TkGeadingFont", 20),
        bg=BTN_BG,
        fg="white",
        activebackground="black",
        command=lambda: load_add_frame()
    ).pack(pady=20)

if __name__ == '__main__':
    root = make_root()
    load_main_frame(root)
    root.mainloop()