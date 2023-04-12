import numpy as np
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import tkinter as tk

#there is code for ringz,ringx and fline but they aren't
#mentioned in the interface

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
    w=1200
    h=700
    screen_width = b1.winfo_screenwidth()
    screen_height = b1.winfo_screenheight()
    x = int((screen_width / 2) - (w / 2))
    y = int((screen_height / 2) - (h / 2))
    b1.geometry(f"{w}x{h}+{x}+{y}")


    ourMessage ="format:object,x,y,z,q/rho/lambda (optional) \nfor line z coordinate doesn't matter\nobjects:charge,sphere,line,fline,ringz,ringx"
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
d=4
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

#draw a ring
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


#draw dot
def charge(loca):
    d=ax.plot(loca[0],loca[1],loca[2],'o',picker=True)

#draw line
def line(loca):
    x=np.full(100,loca[0])
    y=np.full(100,loca[1])
    l=max(coords[:,2])+5
    z=np.linspace(-l,l,100)
    line=ax.plot(x,y,z,picker=True)

#draw finite line
def fline(loca):
    x=np.full(100,loca[0])
    y=np.full(100,loca[1])
    l=3
    z=np.linspace(-l,l,100)
    fline=ax.plot(x,y,z,picker=True)



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
            if temp[0]=='charge':
                try:q=int(temp[4])
                except IndexError:q=1

                E=q/np.abs((int(temp[1])-coords[:,0])**2+(int(temp[2])-coords[:,1])**2+(int(temp[3])-coords[:,2])**2)
                theta=np.arctan2(np.sqrt((int(temp[1])-coords[:,0])**2+(int(temp[2])-coords[:,1])**2),(int(temp[3])-coords[:,2]))
                phi=np.arctan2((int(temp[2])-coords[:,1]),(int(temp[1])-coords[:,0]))
                Ex+=-E*np.sin(theta)*np.cos(phi)
                Ey+=-E*np.sin(theta)*np.sin(phi)
                Ez+=-E*np.cos(theta)

            if temp[0]=='sphere':
                r=1
                try:rho=int(temp[4])
                except IndexError:rho=1

                E = rho*(4*np.pi*r**2) / np.abs((int(temp[1]) - coords[:, 0]) ** 2 + (int(temp[2]) - coords[:, 1]) ** 2 + (int(temp[3]) - coords[:, 2]) ** 2)
                theta = np.arctan2(np.sqrt((int(temp[1]) - coords[:, 0]) ** 2 + (int(temp[2]) - coords[:, 1]) ** 2),(int(temp[3]) - coords[:, 2]))
                phi = np.arctan2((int(temp[2]) - coords[:, 1]), (int(temp[1]) - coords[:, 0]))
                R=np.sqrt((int(temp[1]) - coords[:, 0]) ** 2 + (int(temp[2]) - coords[:, 1]) ** 2 + (int(temp[3]) - coords[:, 2]) ** 2)
                Ex[R>=r] += -E[R>=r] * np.sin(theta[R>=r]) * np.cos(phi[R>=r])
                Ey[R>=r] += -E[R>=r] * np.sin(theta[R>=r]) * np.sin(phi[R>=r])
                Ez[R>=r] += -E[R>=r] * np.cos(theta[R>=r])

            if temp[0]=='line':
                try:lambd=int(temp[4])
                except IndexError:lambd=1

                try:
                    E=lambd/np.sqrt((int(temp[1])-coords[:,0])**2+(int(temp[2])-coords[:,1])**2)
                except ZeroDivisionError:
                    E=0
                phi = np.arctan2((int(temp[2]) - coords[:, 1]), (int(temp[1]) - coords[:, 0]))
                Ex+=-E*np.cos(phi)
                Ey+=-E*np.sin(phi)

            if temp[0]=='ringz':
                r=1
                try:lambd=int(temp[4])
                except IndexError:lambd=1

                rres=100
                u = np.mgrid[0:2 * np.pi:rres*1j]

                for angle in u:
                    x1 = r * np.cos(angle)
                    y1 = r * np.sin(angle)
                    E = (2*np.pi*r/rres)*lambd / np.abs((int(temp[1]) - coords[:, 0]-x1) ** 2 + (int(temp[2]) - coords[:, 1]-y1) ** 2 + (
                                int(temp[3]) - coords[:, 2]) ** 2)
                    theta = np.arctan2(np.sqrt((int(temp[1]) - coords[:, 0]-x1) ** 2 + (int(temp[2]) - coords[:, 1]-y1) ** 2),
                                       (int(temp[3]) - coords[:, 2]))
                    phi = np.arctan2((int(temp[2]) - coords[:, 1]-y1), (int(temp[1]) - coords[:, 0]-x1))
                    Ex += -E * np.sin(theta) * np.cos(phi)
                    Ey += -E * np.sin(theta) * np.sin(phi)
                    Ez += -E * np.cos(theta)

            if temp[0]=='ringx':
                r=1
                try:lambd=int(temp[4])
                except IndexError:lambd=1

                rres = 100
                u1 = np.mgrid[0:2 * np.pi:rres * 1j]

                for angle in u1:
                    z2 = r * np.cos(angle)
                    y2 = r * np.sin(angle)
                    E = (2*np.pi*r/rres)*lambd / np.abs((int(temp[1]) - coords[:, 0]) ** 2 + (int(temp[2]) - coords[:, 1]-y2) ** 2 + (
                                int(temp[3]) - coords[:, 2]-z2) ** 2)
                    theta = np.arctan2(np.sqrt((int(temp[1]) - coords[:, 0]) ** 2 + (int(temp[2]) - coords[:, 1]-y2) ** 2),
                                       (int(temp[3]) - coords[:, 2]-z2))
                    phi = np.arctan2((int(temp[2]) - coords[:, 1]-y2), (int(temp[1]) - coords[:, 0]))
                    Ex += -E * np.sin(theta) * np.cos(phi)
                    Ey += -E * np.sin(theta) * np.sin(phi)
                    Ez += -E * np.cos(theta)

            if temp[0]=='fline':
                l=3
                try:lambd=int(temp[4])
                except IndexError:lambd=1

                rres=1000
                z3=np.linspace(-l,l,rres)

                for z in z3:
                    E = (2*l/rres)*lambd / np.abs((int(temp[1]) - coords[:, 0]) ** 2 + (int(temp[2]) - coords[:, 1]) ** 2 + (
                                int(temp[3]) - coords[:, 2]-z) ** 2)
                    theta = np.arctan2(np.sqrt((int(temp[1]) - coords[:, 0]) ** 2 + (int(temp[2]) - coords[:, 1]) ** 2),
                                       (int(temp[3]) - coords[:, 2]-z))
                    phi = np.arctan2((int(temp[2]) - coords[:, 1]), (int(temp[1]) - coords[:, 0]))
                    Ex += -E * np.sin(theta) * np.cos(phi)
                    Ey += -E * np.sin(theta) * np.sin(phi)
                    Ez += -E * np.cos(theta)

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