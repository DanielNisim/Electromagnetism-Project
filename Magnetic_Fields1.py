import numpy as np
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import tkinter as tk

#requeting objects
objects=[]

#python interface
'''
print("input 0 to stop \nformat:object,x,y,z,q/rho/lambda (optional) \nfor line z coordinate doesn't matter")
object=input("enter object and location:")
while object!='0':
    objects.append(object)
    object=input("enter object and location:")
'''

#####
def ob(window,listbox,text):
    s=str(text.get())
    objects.append(s)
    listbox.insert('active',s)
    text.delete(0,tk.END)

def gui(objects):
    b1=tk.Tk()

    b1.title("Fields of Objects")
    b1.configure(background='light blue')
    # Set window size and position
    w=1300
    h=700
    screen_width = b1.winfo_screenwidth()
    screen_height = b1.winfo_screenheight()
    x = int((screen_width / 2) - (w / 2))
    y = int((screen_height / 2) - (h / 2))
    b1.geometry(f"{w}x{h}+{x}+{y}")


    ourMessage ="format:object,x,y,z,q/rho/lambda (optional),w (optional) \nfor linez z coordinate doesn't matter etc\nobjects:sphere,linex,liney,linez"
    messageVar = tk.Message(b1, text = ourMessage,width=int(0.65*w),font=('arial',25))
    messageVar.config(bg='lightgreen')
    messageVar.grid(row=0)

    tk.Label(b1, text="enter object and location:",font=('arial',25)).grid(row=1)
    e1 = tk.Entry(b1,width=25,font=('arial',25))
    e1.grid(row=1, column=1)

    #List of added objects
    tk.Label(b1, text="List of added objects:", font=('arial', 25)).grid(row=3)
    Lb = tk.Listbox(b1,height=7,width=25,font=('arial',25))
    Lb.grid(row=3,column=1)

    button1 = tk.Button(b1, text='enter', width=25,font=('arial',25), command=lambda: ob(b1,Lb,e1))
    button1.grid(row=2,column=1)

    #Pressing the enter key adds the object
    e1.bind('<Return>', lambda event: ob(b1,Lb,e1))


    button2=tk.Button(b1, text='Finish', width=25,font=('arial',25), command=b1.destroy)
    button2.grid(row=4,column=1)

    b1.mainloop()

gui(objects)
####


#Grid
d=3
n=5 #controls amount of arrows
x=np.linspace(-d, d, n)
y=np.linspace(-d, d, n)
z=np.linspace(-d, d, n)
xx,yy,zz=np.meshgrid(x,y,z)
coords=np.c_[xx.ravel(), yy.ravel(),zz.ravel()]


fig = plt.figure()
ax = plt.axes(projection='3d')

# draw sphere
def sphere(center,r=1):
    #center
    xc,yc,zc=center[0],center[1],center[2]
    u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:50j]
    x = r*np.cos(u)*np.sin(v)+xc
    y = r*np.sin(u)*np.sin(v)+yc
    z = r*np.cos(v)+zc
    # alpha controls opacity
    ax.plot_surface(x, y, z, color="g", alpha=0.3,picker=True)
"""
def ringz(center,r=1):
    xc, yc, zc = center[0], center[1], center[2]
    u = np.mgrid[0:2 * np.pi:50j]
    x = r * np.cos(u) + xc
    y = r * np.sin(u) + yc
    z = zc+np.sin(u*0)
    ax.plot(x,y,z,picker=True)

def ringx(center,r=1):
    xc, yc, zc = center[0], center[1], center[2]
    u = np.mgrid[0:2 * np.pi:50j]
    x = xc+np.sin(u*0)
    y = r * np.sin(u) + yc
    z = r * np.cos(u) + zc
    ax.plot(x,y,z,picker=True)
"""

#draw line
def linez(loca):
    x=np.full(100,loca[0])
    y=np.full(100,loca[1])
    l=max(coords[:,2])+5
    z=np.linspace(-l,l,100)
    line1=ax.plot(x,y,z,picker=True)

def linex(loca):
    z=np.full(100,loca[2])
    y=np.full(100,loca[1])
    l=max(coords[:,2])+5
    x=np.linspace(-l,l,100)
    line2=ax.plot(x,y,z,picker=True)

def liney(loca):
    x=np.full(100,loca[0])
    z=np.full(100,loca[2])
    l=max(coords[:,2])+5
    y=np.linspace(-l,l,100)
    line3=ax.plot(x,y,z,picker=True)


def draw(objects):
    global drawlist
    removelst=[]
    for item in objects:
        temp=item.split(',')
        try:
            eval(temp[0]+f'([{temp[1]},{temp[2]},{temp[3]}])')
        except Exception as e:
            print(f"object {item} didn't print beacuse: {str(e)}")
            removelst.append(item)
    for item in removelst:
        objects.remove(item)

#calculating strength
def field(objects):
    Ex=np.zeros(coords.shape[0])
    Ey=np.copy(Ex)
    Ez=np.copy(Ex)
    for item in objects:
        temp = item.split(',')
        try:

            if temp[0]=='sphere':
                r=1
                try:rho=int(temp[4])
                except IndexError:rho=1
                try:w=int(temp[5])
                except IndexError:w=1
                R = np.sqrt((int(temp[1]) - coords[:, 0]) ** 2 + (int(temp[2]) - coords[:, 1]) ** 2 + (int(temp[3]) - coords[:, 2]) ** 2)
                #R<r
                Ein=4*np.pi/3*r*w*rho
                Ez[R<=r]+=Ein

                #R>r
                Eout = w*rho*(4*np.pi*r**4)/3 / R**3
                theta = np.arctan2(np.sqrt((int(temp[1]) - coords[:, 0]) ** 2 + (int(temp[2]) - coords[:, 1]) ** 2),(int(temp[3]) - coords[:, 2]))
                phi = np.arctan2((int(temp[2]) - coords[:, 1]), (int(temp[1]) - coords[:, 0]))

                Ex[R>=r] += Eout[R>=r] *3/2* np.sin(2*theta[R>=r]) * np.cos(phi[R>=r])
                Ey[R>=r] += Eout[R>=r] *3/2* np.sin(2*theta[R>=r]) * np.sin(phi[R>=r])
                Ez[R>=r] += Eout[R>=r] *(2-3* np.sin(theta[R>=r])**2)

            if temp[0]=='linez':
                try:I=int(temp[4])
                except IndexError:I=1

                try:
                    E=I/np.sqrt((int(temp[1])-coords[:,0])**2+(int(temp[2])-coords[:,1])**2)
                except ZeroDivisionError:
                    E=0
                phi = np.arctan2((int(temp[2]) - coords[:, 1]), (int(temp[1]) - coords[:, 0]))
                Ex+=E*np.sin(phi)
                Ey+=-E*np.cos(phi)

            if temp[0]=='linex':
                try:I=int(temp[4])
                except IndexError:I=1

                try:
                    E=I/np.sqrt((int(temp[3])-coords[:,2])**2+(int(temp[2])-coords[:,1])**2)
                except ZeroDivisionError:
                    E=0
                phi = np.arctan2((int(temp[3]) - coords[:, 2]), (int(temp[2]) - coords[:, 1]))
                Ey+=E*np.sin(phi)
                Ez+=-E*np.cos(phi)

            if temp[0]=='liney':
                try:I=int(temp[4])
                except IndexError:I=1

                try:
                    E=I/np.sqrt((int(temp[1])-coords[:,0])**2+(int(temp[3])-coords[:,2])**2)
                except ZeroDivisionError:
                    E=0
                phi = np.arctan2((int(temp[1]) - coords[:, 0]), (int(temp[3]) - coords[:, 2]))
                Ez+=E*np.sin(phi)
                Ex+=-E*np.cos(phi)
        except ValueError: None


    vecs=np.array([Ex,Ey,Ez])
    ax.quiver(coords[:,0],coords[:,1],coords[:,2],vecs[0], vecs[1], vecs[2],length=1.0, normalize=True, color='blue', arrow_length_ratio=0.7)

draw(objects)
field(objects)
plt.xlim([np.min(coords[:,0])-1,np.max(coords[:,0])+1])
plt.ylim([np.min(coords[:,1])-1,np.max(coords[:,1])+1])
ax.set_zlim([np.min(coords[:,1])-1,np.max(coords[:,1])+1])
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')

items=[]
for i in range(len(objects)):
     items.append(objects[i].split(','))

plt.show()