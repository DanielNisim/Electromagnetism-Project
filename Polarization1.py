from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import tkinter as tk
import sys
#initializing phase shift
dphi=0

# initializing a figure in
# which the graph will be plotted
fig = plt.figure()


# marking the x-axis and y-axis
axis = plt.axes(xlim=(0, 4),
                ylim=(-2, 2),zlim=(-2,2),projection='3d')

# initializing a line variable
line, = axis.plot([], [], [], lw=3)
line2, = axis.plot([], [], [], lw=3)
shape,=axis.plot([], [], [], lw=3)
dot,=axis.plot([],[],[],'o')

# data which the line will
# contain (x, y)
def init():
    line.set_data([], [])
    line.set_3d_properties([])
    line2.set_data([], [])
    line2.set_3d_properties([])
    shape.set_data([], [])
    shape.set_3d_properties([])
    dot.set_data([], [])
    dot.set_3d_properties([])
    return line,line2,shape,dot,

#Animation
def animate(i):
    x = np.linspace(0, 4, 1000)
    global dphi
    # plots a sine graph
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    y2=np.sin(2 * np.pi * (x - 0.01 * i)+dphi)
    z=np.zeros(len(x))
    line.set_data(x, y)
    line.set_3d_properties(z)
    line2.set_data(x, z)
    line2.set_3d_properties(y2)
    shape.set_data(x*0, y)
    shape.set_3d_properties(y2)
    dot.set_data([0], [y[0]])
    dot.set_3d_properties([y2[0]])

    return line,line2,shape,dot,


###
#Interface
def b1(r):
    global dphi
    dphi=0
    plt.suptitle('Linear Wave')
    r.destroy()

def b2(r):
    global dphi
    dphi=0.5*np.pi
    plt.suptitle('Circular Wave')
    r.destroy()

def b3(r):
    global dphi
    dphi=0.25*np.pi
    plt.suptitle('Elliptical Wave')
    r.destroy()

def gp(root,e1):
    global dphi
    dphi=float(e1.get())
    plt.suptitle(f'Electrical Wave with dphi={dphi}')
    root.destroy()


#window creation
r = tk.Tk()
r.title('Polarization')
r.configure(background='light blue')
#Set window size and position
w=1500
h=700
screen_width = r.winfo_screenwidth()
screen_height = r.winfo_screenheight()
x = int((screen_width/2) - (w/2))
y = int((screen_height/2) - (h/2))
r.geometry(f"{w}x{h}+{x}+{y}")

#text at the top
ourMessage ='Choose phase shift:'
messageVar = tk.Message(r, text = ourMessage,width=500)
messageVar.config(bg='lightgreen',font=('arial',25))
messageVar.grid(row=0,column=1)

bw=25 #width of buttons

button1 = tk.Button(r, text='Linear wave', width=bw,font=('arial',25), command=lambda: b1(r))
button1.grid(row=1,column=1)

button2 = tk.Button(r, text='Circular wave (dphi=0.5pi)', width=bw,font=('arial',25), command=lambda: b2(r))
button2.grid(row=2,column=1)

button3 = tk.Button(r, text='Elliptical wave (with dphi=0.25pi)', width=bw,font=('arial',25), command=lambda: b3(r))
button3.grid(row=3,column=1)

tk.Label(r, text=f"Another phase shift:",font=('arial',25)).grid(row=4)
e1 = tk.Entry(r,width=27,font=('arial',25))
e1.grid(row=4, column=1)
tk.Label(r, text='radians', font=('arial', 25)).grid(row=4,column=2)

button3 = tk.Button(r, text='Enter', width=bw,font=('arial',25), command=lambda: gp(r,e1))
button3.grid(row=5,column=1)

r.mainloop()
###


#activating the animation
anim = FuncAnimation(fig, animate, init_func=init,
                     frames=200, interval=20, blit=True)


axis.legend(['Ex','Ey','Shape'])
axis.set_xlabel('z')
axis.set_ylabel('x')
axis.set_zlabel('y')

###
#pause and resume animation
axis.set_title('Press space to pause and resume', fontsize=8)
anim_running=True
def on_press(event):
    global anim_running
    print('press', event.key)
    sys.stdout.flush()
    if event.key == ' ' and anim_running:
        anim.pause()
        anim_running=False
    elif event.key == ' ' and not anim_running:
        anim.resume()
        fig.canvas.draw() #stops paused graph from staying
        anim_running=True

fig.canvas.mpl_connect('key_press_event', on_press)
###

plt.show()