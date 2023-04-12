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
lenX = lenY = 20
delta = 1


#Creating color map
#resolution (max=999):
colorinterpolation = 500
colourMap = plt.cm.jet

#Grid
d=lenX
x=np.linspace(-d, d, d)
y=np.linspace(-d, d, d)
xx,yy=np.meshgrid(x,y)
coords=np.c_[xx.ravel(), yy.ravel()]

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

b1.title("Cartesian Potential Problems")
b1.configure(background='light blue')
#Set window size and position
w=1000
h=500
screen_width = b1.winfo_screenwidth()
screen_height = b1.winfo_screenheight()
x1 = int((screen_width / 2) - (w / 2))
y1 = int((screen_height / 2) - (h / 2))
b1.geometry(f"{w}x{h}+{x1}+{y1}")


ourMessage ="Enter boundary conditions"
messageVar = tk.Message(b1, text = ourMessage,width=int(0.65*w),font=('arial',25))
messageVar.config(bg='lightgreen')
messageVar.grid(row=0)

tk.Label(b1, text=f"Voltage at x={d}",font=('arial',25)).grid(row=1)
e1 = tk.Entry(b1,width=25,font=('arial',25))
e1.grid(row=1, column=1)
tk.Label(b1, text='Volt', font=('arial', 25)).grid(row=1,column=2)

tk.Label(b1, text=f"Voltage at x={-d}", font=('arial', 25)).grid(row=2)
e2 = tk.Entry(b1, width=25, font=('arial', 25))
e2.grid(row=2, column=1)
tk.Label(b1, text='Volt', font=('arial', 25)).grid(row=2,column=2)


tk.Label(b1, text=f"Voltage at y={d}", font=('arial', 25)).grid(row=3)
e3 = tk.Entry(b1, width=25, font=('arial', 25))
e3.grid(row=3, column=1)
tk.Label(b1, text='Volt', font=('arial', 25)).grid(row=3,column=2)

tk.Label(b1, text=f"Voltage at y={-d}", font=('arial', 25)).grid(row=4)
e4 = tk.Entry(b1, width=25, font=('arial', 25))
e4.grid(row=4, column=1)
tk.Label(b1, text='Volt', font=('arial', 25)).grid(row=4,column=2)

button2=tk.Button(b1, text='Finish', width=25,font=('arial',25), command=lambda: bc(b1,e1,e2,e3,e4))
button2.grid(row=5)

b1.mainloop()




# Initial guess of interior grid
Vguess = float(Vxmax)

# Set array size and set the interior value with Tguess
T = np.empty((lenX, lenY))
T.fill(Vguess)

# Set Boundary condition
T[(lenY-1):, :] = Vxmax
T[:1, :] = Vxmin
T[:, (lenX-1):] = Vymax
T[:, :1] = Vymin

# Iteration (We assume that the iteration is convergence in maxIter = 500)
print("Please wait for a moment")
for iteration in range(0, maxIter):
    for i in range(1, lenX-1, delta):
        for j in range(1, lenY-1, delta):
            T[i, j] = 0.25 * (T[i+1][j] + T[i-1][j] + T[i][j+1] + T[i][j-1])

print("Iteration finished")

# Configure the contour
plt.title("Voltage")
plt.xlabel('x')
plt.ylabel('y')
plt.contourf( yy,xx, T, colorinterpolation, cmap=colourMap)

# Set Colorbar
cbar=plt.colorbar()
cbar.ax.set_title('Volt')

# Show the result in the plot window
plt.show()


fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_title("Voltage-3D graph")
ax.contour3D(x,y,T.T,colorinterpolation)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('V')
plt.show()