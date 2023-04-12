import numpy as np
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.backend_bases import FigureCanvasBase as fcb
from scipy.integrate import solve_ivp,odeint
import tkinter as tk

# Set maximum iteration
maxIter = 500

# Set Dimension and delta
#print("set boundaries:")
#lenR = float(input("max r (r>0):")) #lenR>0
#minR= float(input("min r (0<=r<maxR):"))
#lenP = float(input("max angle (0<phi<=2*pi):")) #0<lenP<2*pi

delta = 1
lenR=1
minR=0
lenP=0.79

def sb(root,e1,e2,e3):
    global lenR
    global minR
    global lenP
    lenR=float(e1.get())
    minR=float(e2.get())
    lenP=float(e3.get())
    root.destroy()

b2=tk.Tk()

b2.title("Cylindrical Potential Problems")
b2.configure(background='light blue')
#Set window size and position
w=1000
h=300
screen_width = b2.winfo_screenwidth()
screen_height = b2.winfo_screenheight()
x = int((screen_width / 2) - (w / 2))
y = int((screen_height / 2) - (h / 2))
b2.geometry(f"{w}x{h}+{x}+{y}")


ourMessage ="Set boundaries"
messageVar = tk.Message(b2, text = ourMessage,width=int(0.65*w),font=('arial',25))
messageVar.config(bg='lightgreen')
messageVar.grid(row=0)

tk.Label(b2, text="max r (r>0):",font=('arial',25)).grid(row=1)
e1 = tk.Entry(b2,width=25,font=('arial',25))
e1.grid(row=1, column=1)

tk.Label(b2, text="min r (0<=r<maxR):", font=('arial', 25)).grid(row=2)
e2 = tk.Entry(b2, width=25, font=('arial', 25))
e2.grid(row=2, column=1)

tk.Label(b2, text="max angle (0<phi<=2*pi):", font=('arial', 25)).grid(row=3)
e3 = tk.Entry(b2, width=25, font=('arial', 25))
e3.grid(row=3, column=1)

button2=tk.Button(b2, text='Finish', width=25,font=('arial',25), command=lambda:sb(b2,e1,e2,e3))
button2.grid(row=5)

b2.mainloop()

Vxmax=0
Vxmin=0
Vymax=0
Vymin=0
def bc(root,e1,e2,e3,e4):
    global Vxmax
    global Vxmin
    global Vymax
    global Vymin
    Vxmax=str(e1.get())
    Vxmin=str(e2.get())
    Vymax=str(e3.get())
    Vymin=str(e4.get())
    root.destroy()
#open window and set boundary conditions

b1=tk.Tk()

b1.title("Cylindrical Potential Problems")
b1.configure(background='light blue')
#Set window size and position
w=1000
h=300
screen_width = b1.winfo_screenwidth()
screen_height = b1.winfo_screenheight()
x = int((screen_width / 2) - (w / 2))
y = int((screen_height / 2) - (h / 2))
b1.geometry(f"{w}x{h}+{x}+{y}")


ourMessage ="Enter boundary conditions"
messageVar = tk.Message(b1, text = ourMessage,width=int(0.65*w),font=('arial',25))
messageVar.config(bg='lightgreen')
messageVar.grid(row=0)

tk.Label(b1, text=f'Voltage at r={lenR}:',font=('arial',25)).grid(row=1)
e1 = tk.Entry(b1,width=25,font=('arial',25))
e1.grid(row=1, column=1)
tk.Label(b1, text='Volt', font=('arial', 25)).grid(row=1,column=2)

tk.Label(b1, text=f'Voltage at r={minR}:', font=('arial', 25)).grid(row=2)
e2 = tk.Entry(b1, width=25, font=('arial', 25))
e2.grid(row=2, column=1)
tk.Label(b1, text='Volt', font=('arial', 25)).grid(row=2,column=2)

tk.Label(b1, text=f'Voltage at phi={lenP}:', font=('arial', 25)).grid(row=3)
e3 = tk.Entry(b1, width=25, font=('arial', 25))
e3.grid(row=3, column=1)
tk.Label(b1, text='Volt', font=('arial', 25)).grid(row=3,column=2)

tk.Label(b1, text=f'Voltage at phi=0:', font=('arial', 25)).grid(row=4)
e4 = tk.Entry(b1, width=25, font=('arial', 25))
e4.grid(row=4, column=1)
tk.Label(b1, text='Volt', font=('arial', 25)).grid(row=4,column=2)

button2=tk.Button(b1, text='Finish', width=25,font=('arial',25), command=lambda: bc(b1,e1,e2,e3,e4))
button2.grid(row=5)

messageVar = tk.Message(b1, text = "Calculation might take a few seconds",width=int(0.65*w),font=('arial',25))

b1.mainloop()


#Creating color map
#color resolution (max=999):
colorinterpolation = 500
colourMap = plt.cm.jet

#Grid
d=100 #resolution
x=np.linspace(minR, lenR, d)
y=np.linspace(0, lenP, d)
xx,yy=np.meshgrid(x,y)
coords=np.c_[xx.ravel(), yy.ravel()]


# Initial guess of interior grid
Vguess = float(Vxmax)

# Set array size and set the interior value with Tguess
T = np.empty((d, d))
T.fill(Vguess)

# Set Boundary condition
T[(d-1):, :] = Vymax
T[:1, :] = Vymin
T[:, (d-1):] = Vxmax
T[:, :1] = Vxmin


# Iteration (We assume that the iteration is convergence in maxIter = 500)
print("Please wait for a moment")
for iteration in range(0, maxIter):
    for i in range(1, d-1, delta):
        for j in range(1, d-1, delta):
            T[i, j] = 0.25 * (T[i+1][j] + T[i-1][j] + T[i][j+1] + T[i][j-1])

print("Iteration finished")

# Configure the contour
plt.title("Voltage")
plt.xlabel('x')
plt.ylabel('y')
plt.contourf(xx*np.cos(yy), xx*np.sin(yy), T, colorinterpolation, cmap=colourMap)

# Set Colorbar
cbar=plt.colorbar()
cbar.ax.set_title('Volt')

#draw the circle
u = np.mgrid[0:2 * np.pi:50j]
x = lenR * np.cos(u)
y = lenR * np.sin(u)
plt.plot(x,y,linewidth=2,color='black')

x2 = minR * np.cos(u)
y2 = minR * np.sin(u)
plt.plot(x2,y2,linewidth=2,color='black')

plt.text((lenR+0.5)*np.cos(lenP),(lenR+0.5)*np.sin(lenP),f'phi={np.round(lenP,2)}')
# Show the result in the plot window
plt.show()


#test
"""
plt.contourf(xx, yy, T, colorinterpolation, cmap=colourMap)
plt.colorbar()
plt.show()
"""
