import tkinter as tk
import sys
import os


def main():
    # Functions for opening scripts
    def b1(root, m):
        # hide root window (turns black if left open)
        m.destroy()
        root.withdraw()
        # run other script
        os.system('python Fields_of_objects1.py')
        # make root window visible again
        root.deiconify()

    def b2(root):
        # hide root window (turns black if left open)
        root.withdraw()
        # run other script
        os.system('python Cartesian_potential_problem1.py')
        # make root window visible again
        root.deiconify()

    def b3(root):
        # hide root window (turns black if left open)
        root.withdraw()
        # run other script
        os.system('python Cylindrical_potential_problem1.py')
        # make root window visible again
        root.deiconify()

    def b4(root):
        # hide root window (turns black if left open)
        root.withdraw()
        # run other script
        os.system('python CPP_Ronly1.py')
        # make root window visible again
        root.deiconify()

    def b5(root, m):
        # hide root window (turns black if left open)
        m.destroy()
        root.withdraw()
        # run other script
        os.system('python Polarization1.py')
        # make root window visible again
        root.deiconify()

    def b6(root, m):
        # hide root window (turns black if left open)
        m.destroy()
        root.withdraw()
        # run other script
        os.system('python Magnetic_Fields1.py')
        # make root window visible again
        root.deiconify()

    def b7(root, m):
        # hide root window (turns black if left open)
        m.destroy()
        root.withdraw()
        # run other script
        os.system('python Polarization_plates1.py')
        # make root window visible again
        root.deiconify()

    def b8(root):
        # hide root window (turns black if left open)
        root.withdraw()
        # run other script
        os.system('python relativeEM.py')
        # make root window visible again
        root.deiconify()

    # Main window creation
    r = tk.Tk()
    r.title('Electromagnetic simulations')
    r.configure(background='light blue')
    # Set window size and position
    w = 1000
    h = 500
    screen_width = r.winfo_screenwidth()
    screen_height = r.winfo_screenheight()
    x = int((screen_width / 2) - (w / 2))
    y = int((screen_height / 2) - (h / 2))
    r.geometry(f"{w}x{h}+{x}+{y}")

    # text at the top
    ourMessage = 'Choose a simulation:'
    messageVar = tk.Message(r, text=ourMessage, width=500)
    messageVar.config(bg='lightgreen', font=('arial', 40))
    messageVar.pack()

    bw = 30  # width of buttons

    # Functions for opening subwindows
    def open1(root):
        m = tk.Toplevel(r)

        # Set window position
        screen_width = m.winfo_screenwidth()
        screen_height = m.winfo_screenheight()
        x = int((screen_width / 2) - (w / 2))
        y = int((screen_height / 2) - (h / 2))
        m.geometry(f"+{x}+{y}")

        message = tk.Message(m, text="Choose type of field:", width=500)
        message.config(bg='lightgreen', font=('arial', 25))
        message.pack()

        button1 = tk.Button(m, text='Electric Field', width=bw, font=('arial', 25), command=lambda: b1(root, m))
        button1.pack()

        button2 = tk.Button(m, text='Magnetic Field', width=bw, font=('arial', 25), command=lambda: b6(root, m))
        button2.pack()

        message2 = tk.Message(m, text="*Fields are Normalized", width=500, font=('arial', 15))
        message2.pack()
        m.mainloop()

    def open2(root):
        m = tk.Toplevel(r)

        # Set window position
        screen_width = m.winfo_screenwidth()
        screen_height = m.winfo_screenheight()
        x = int((screen_width / 2) - (w / 2))
        y = int((screen_height / 2) - (h / 2))
        m.geometry(f"+{x}+{y}")

        message = tk.Message(m, text="Polarization", width=500)
        message.config(bg='lightgreen', font=('arial', 25))
        message.pack()

        button1 = tk.Button(m, text='Kinds of polarizations', width=bw, font=('arial', 25), command=lambda: b5(root, m))
        button1.pack()

        button2 = tk.Button(m, text='Wave plates', width=bw, font=('arial', 25), command=lambda: b7(root, m))
        button2.pack()

        m.mainloop()

    # Buttons for choosing script
    button1 = tk.Button(r, text='Fields of objects', width=bw, font=('arial', 25), command=lambda: open1(r))
    button1.pack()

    button2 = tk.Button(r, text='Cartesian potential problem', width=bw, font=('arial', 25), command=lambda: b2(r))
    button2.pack()

    button3 = tk.Button(r, text='Cylindrical potential problem', width=bw, font=('arial', 25), command=lambda: b3(r))
    button3.pack()

    button4 = tk.Button(r, text='Cylindrical potential problem (R only)', width=bw, font=('arial', 25),
                        command=lambda: b4(r))
    button4.pack()

    button5 = tk.Button(r, text='Polarization', width=bw, font=('arial', 25), command=lambda: open2(r))
    button5.pack()

    button6 = tk.Button(r, text='A moving charge', width=bw, font=('arial', 25), command=lambda: b8(r))
    button6.pack()

    r.mainloop()


if __name__ == "__main__":
    main()
