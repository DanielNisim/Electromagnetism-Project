import numpy as np
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import tkinter as tk
from tkinter import ttk


scale=False
def b1(r,var1):
    global scale
    scale=var1.get()
    r.destroy()

#window creation
r = tk.Tk()
r.title('A moving charge')
r.configure(background='light blue')
#Set window size and position
w=700
h=300
screen_width = r.winfo_screenwidth()
screen_height = r.winfo_screenheight()
x = int((screen_width/2) - (w/2))
y = int((screen_height/2) - (h/2))
r.geometry(f"{w}x{h}+{x}+{y}")


#text at the top
ourMessage ='A moving charge'
messageVar = tk.Message(r, text = ourMessage,width=500)
messageVar.config(bg='lightgreen',font=('arial',40))
messageVar.pack()

bw=10 #width of buttons

tk.Label(r, text=f"Scaled by strength?",font=('arial',25)).pack()
var1 = tk.IntVar()
e1 = tk.Checkbutton(r,variable=var1,onvalue=0,offvalue=1,width=27,height=3,bg='light blue',foreground='green')
e1.pack()

#clear checkbutton
e1.toggle()

button3 = tk.Button(r, text='Enter', width=bw,font=('arial',25), command=lambda: b1(r,var1))
button3.pack()

ourMessage1 ='*When in scaled mode the magnetic fields are multiplied by 100,000'
messageVar1 = tk.Message(r, text = ourMessage1,width=500)
messageVar1.config(bg='lightgreen',font=('arial',15))
messageVar1.pack()

r.mainloop()
###



# initializing a figure in
# which the graph will be plotted
fig = plt.figure()

#Grid
d=4
n=5 #controls amount of arrows
x=np.linspace(-d, d, n)
y=np.linspace(-d, d, n)
z=np.linspace(-d, d, n)
xx,yy,zz=np.meshgrid(x,y,z)
coords=np.c_[xx.ravel(), yy.ravel(),zz.ravel()]

c=299792.458#km/s

# marking the x-axis and y-axis
axis = plt.axes(xlim=(-d, d),
                ylim=(-d, d),zlim=(-d,d),projection='3d')

axis.plot(0,0,0,'o')


# The parametrized function to be plotted
def f(q, v):
    gamma=1/np.sqrt(1-v**2/c**2)

    E = q / np.abs(
        (0 - coords[:, 0]) ** 2 + (0 - coords[:, 1]) ** 2 + (0 - coords[:, 2]) ** 2)
    theta = np.arctan2(np.sqrt((0 - coords[:, 0]) ** 2 + (0 - coords[:, 1]) ** 2),
                       (0 - coords[:, 2]))
    phi = np.arctan2((0 - coords[:, 1]), (0 - coords[:, 0]))
    Ex = -E * np.sin(theta) * np.cos(phi)
    Ey = -E * np.sin(theta) * np.sin(phi) * gamma
    Ez = -E * np.cos(theta) * gamma

    Bx=0*coords[:,0]
    By=Ez*v/c**2 * gamma
    Bz=-Ey*v/c**2 * gamma

    return Ex,Ey,Ez,Bx,By,Bz


# Define initial parameters
init_q = 1
init_v = 0

# Create the figure and the line that we will manipulate

vecs=np.array(f(init_q,init_v)[0:3])
size=vecs[0]**2+vecs[1]**2+vecs[2]**2
axis.quiver(coords[:,0],coords[:,1],coords[:,2],vecs[0], vecs[1], vecs[2], normalize=scale, color='blue', arrow_length_ratio=0.7)

vecs1=np.array(f(init_q,init_v)[3:6])
axis.quiver(coords[:,0],coords[:,1],coords[:,2],vecs1[0], vecs1[1], vecs1[2], normalize=scale, color='green', arrow_length_ratio=0.7)


# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.15, bottom=0.25)

# Make a horizontal slider to control the frequency.
axq = fig.add_axes([0.25, 0.1, 0.65, 0.03])
q_slider = Slider(
    ax=axq,
    label='q',
    valmin=-3,
    valmax=3,
    valinit=init_q,
)

# Make a vertically oriented slider to control the amplitude
axv = fig.add_axes([0.25, 0.15, 0.65, 0.03])
v_slider = Slider(
    ax=axv,
    label="v[km/s]",
    valmin=-297000,
    valmax=297000,
    valinit=init_v,
)


# The function to be called anytime a slider's value changes
def update(val):
    axis.cla()

    axis.set_title('Fields from the frame of a stationary viewer')
    axis.set_xlabel('X-axis')
    axis.set_ylabel('Y-axis')
    axis.set_zlabel('Z-axis')
    axis.annotate(f'Charge at {np.round(np.abs(100*v_slider.val/c),2)}% the speed of light', (0, 0), (10, -10), xycoords='axes fraction',textcoords='offset points', va='top')
    axis.plot(0, 0, 0, 'o')

    #Velocity arrow
    axis.quiver(0,0,0,4*v_slider.val/c,0,0,color='Purple')

    vecs = np.array(f(q_slider.val, v_slider.val)[0:3])
    size = vecs[0] ** 2 + vecs[1] ** 2 + vecs[2] ** 2
    axis.quiver(coords[:, 0], coords[:, 1], coords[:, 2], vecs[0], vecs[1], vecs[2], normalize=scale,
                    color='blue', arrow_length_ratio=0.7)

    vecs1 = np.array(f(q_slider.val, v_slider.val)[3:6])
    axis.quiver(coords[:, 0], coords[:, 1], coords[:, 2], 100000*vecs1[0], 100000*vecs1[1], 100000*vecs1[2], normalize=scale,
                    color='green', arrow_length_ratio=0.7)

    fig.canvas.draw_idle()


# register the update function with each slider
q_slider.on_changed(update)
v_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')

def reset(event):
    q_slider.reset()
    v_slider.reset()
button.on_clicked(reset)

#Change view point

#xy
def bu1(event):
    axis.view_init(elev=90, azim=90)
b1ax= fig.add_axes([0.6, 0.025, 0.1, 0.04])
button1 = Button(b1ax, 'XY', hovercolor='0.975')
button1.on_clicked(bu1)

#xz
def bu2(event):
    axis.view_init(elev=0, azim=90)
b2ax= fig.add_axes([0.4, 0.025, 0.1, 0.04])
button2 = Button(b2ax, 'XZ', hovercolor='0.975')
button2.on_clicked(bu2)

#yz
def bu3(event):
    axis.view_init(elev=0, azim=0)
b3ax= fig.add_axes([0.2, 0.025, 0.1, 0.04])
button3 = Button(b3ax, 'YZ', hovercolor='0.975')
button3.on_clicked(bu3)


axis.set_title('Fields from the frame of a stationary viewer')
axis.set_xlabel('X-axis')
axis.set_ylabel('Y-axis')
axis.set_zlabel('Z-axis')
axis.annotate(f'Charge at 0% the speed of light',(0,0),(10, -10), xycoords='axes fraction', textcoords='offset points', va='top')
fig.legend(['The charge','Electric field', 'Magnetic field'],loc='center left')
plt.show()
