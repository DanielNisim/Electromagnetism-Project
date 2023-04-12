import sys
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import tkinter as tk
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection


#initializing original phase shift and change in phase shift
odphi=0
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

line3, = axis.plot([], [], [], lw=3)
line4, = axis.plot([], [], [], lw=3)
shape2,=axis.plot([], [], [], lw=3)
dot2,=axis.plot([],[],[],'o')

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

    line3.set_data([], [])
    line3.set_3d_properties([])
    line4.set_data([], [])
    line4.set_3d_properties([])
    shape2.set_data([], [])
    shape2.set_3d_properties([])
    dot2.set_data([], [])
    dot2.set_3d_properties([])

    return line,line2,shape,dot,line3,line4,shape2,dot2,

#Animation
def animate(i):
    x = np.linspace(0, 2, 1000)
    x2= np.linspace(2, 4, 1000)
    global dphi
    # before
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    y1= np.sin(2 * np.pi * (x - 0.01 * i)+odphi)
    y2=np.sin(2 * np.pi * (x - 0.01 * i)+odphi+dphi)
    z=np.zeros(len(x))
    line.set_data(x, y)
    line.set_3d_properties(z)
    line2.set_data(x, z)
    line2.set_3d_properties(y1)
    shape.set_data(x*0, y)
    shape.set_3d_properties(y1)
    dot.set_data([0], [y[0]])
    dot.set_3d_properties([y1[0]])

    #after
    line3.set_data(x2, y)
    line3.set_3d_properties(z)
    line4.set_data(x2, z)
    line4.set_3d_properties(y2)
    shape2.set_data(x2 /x2 * 4, y)
    shape2.set_3d_properties(y2)
    dot2.set_data([4], [y[0]])
    dot2.set_3d_properties([y2[0]])

    return line,line2,shape,dot,line3,line4,shape2,dot2,


###
#Interface
def b1(r,e2):
    global odphi
    global dphi
    try:
        odphi = float(e2.get())
    except ValueError:
        odphi=0
    dphi=0
    axis.set_title('Full Wave Plate')
    r.destroy()

def b2(r,e2):
    global odphi
    global dphi
    try:
        odphi = float(e2.get())
    except ValueError:
        odphi = 0
    dphi=np.pi
    plt.suptitle('Half Wave Plate')
    r.destroy()

def b3(r,e2):
    global odphi
    global dphi
    try:
        odphi = float(e2.get())
    except ValueError:
        odphi = 0
    dphi=0.5*np.pi
    plt.suptitle('Quarter Wave Plate')
    r.destroy()

def gp(root,e1,e2):
    global odphi
    global dphi
    try:
        odphi = float(e2.get())
    except ValueError:
        odphi = 0
    dphi=float(e1.get())
    plt.suptitle(f'Plate with dphi={dphi}')
    root.destroy()

def set_text(text):
    e2.delete(0,tk.END)
    e2.insert(0,text)


#window creation
r = tk.Tk()
r.title('Polarization')
r.configure(background='light blue')
#Set window size and position
w=2000
h=700
screen_width = r.winfo_screenwidth()
screen_height = r.winfo_screenheight()
x = int((screen_width/2) - (w/2))
y = int((screen_height/2) - (h/2))
r.geometry(f"{w}x{h}+{x}+{y}")

#text at the top
ourMessage ='Enter original phase shift ,and than choose a plate or enter custom phase change'
messageVar = tk.Message(r, text = ourMessage,width=1000)
messageVar.config(bg='lightgreen',font=('arial',25))
messageVar.grid(row=0,column=1)

bw=33 #width of buttons
tk.Label(r, text=f"Original phase shift:",font=('arial',25)).grid(row=1)
e2 = tk.Entry(r,width=35,font=('arial',25))
e2.grid(row=1, column=1)
tk.Label(r, text='radians', font=('arial', 25)).grid(row=1,column=2)


bpi1=tk.Button(r, text='0.5pi', width=5,font=('arial',25), command=lambda: set_text("1.57080"))
bpi1.grid(row=1,column=3)

bpi2=tk.Button(r, text='pi', width=5,font=('arial',25), command=lambda: set_text("3.14159"))
bpi2.grid(row=1,column=4)


button1 = tk.Button(r, text='No phase shift', width=bw,font=('arial',25), command=lambda: b1(r,e2))
button1.grid(row=2,column=1)

button2 = tk.Button(r, text='Half Wave shift (dphi=pi)', width=bw,font=('arial',25), command=lambda: b2(r,e2))
button2.grid(row=3,column=1)

button3 = tk.Button(r, text='Quarter Wave shift (dphi=0.5pi)', width=bw,font=('arial',25), command=lambda: b3(r,e2))
button3.grid(row=4,column=1)

tk.Label(r, text=f"Change phase shift:",font=('arial',25)).grid(row=5)
e1 = tk.Entry(r,width=35,font=('arial',25))
e1.grid(row=5, column=1)
tk.Label(r, text='radians', font=('arial', 25)).grid(row=5,column=2)

button3 = tk.Button(r, text='Enter', width=bw,font=('arial',25), command=lambda: gp(r,e1,e2))
button3.grid(row=6,column=1)

r.mainloop()
###


#activating the animation
anim = FuncAnimation(fig, animate, init_func=init,
                     frames=200, interval=20, blit=True)

#plotting filter
l=2
x1=np.linspace(-l,l,100)
x2=np.full(len(x1),2)
x3=np.full(len(x1),-l)
x4=np.full(len(x1),l)
f,=axis.plot(x2,x1,x3,'blue')
axis.plot(x2,x1,x4,'blue')
axis.plot(x2,x3,x1,'blue')
axis.plot(x2,x4,x1,'blue')

#plotting optic axis
optic,=axis.plot(x2,np.zeros(len(x1)),x1)

#creating the legend
pos = axis.get_position()
axis.set_position([pos.x0, pos.y0+0.15, pos.width, pos.height * 0.85])
axis.legend([line,line2,shape,line3,line4,shape2,f,optic],['Ex,i','Ey,i','Shape','Ex,f','Ey,f','Shape after','Filter','Optic axis'], loc='lower center',bbox_to_anchor=(0.5, -0.35),ncol=3,)

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