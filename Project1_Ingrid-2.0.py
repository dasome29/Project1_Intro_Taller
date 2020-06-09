from tkinter import *
import tkinter as tk
from tkinter import messagebox
import random
import time
from threading import Thread
import functools
import os

global CB_EW, Freno, Proxi, cars, stopped, animation_time

CB_EW = True
Freno = True
Proxi = 100
cars = []
stopped = False
animation_time = 10

root = tk.Tk()



def read_txt():
    global CB_EW, Freno, Proxi
    w = open('backup.txt', 'r')
    CB_EW = w.readline()
    Freno = w.readline()
    Proxi = w.readline()

read_txt()




'''Simulador'''


def simu():
    listaY = [50, 260]

    global CB_EW, Proxi, Freno, cars, stopped

    print("El valor de CB_EW simu es:", CB_EW)
    print("El valor de Freno simu es:", Freno)
    print("El valor de Proxi simu es:", Proxi)

    def change_lane(i, canvas, truck):
        global cars

        truck_position = canvas.coords(truck)
        if i < len(cars):
            car = cars[i]
            car_position = car.canvas.coords(car.rect)
            if [car_position[0]] < [truck_position[2] + 200 + (Proxi / 2)] and car_position[1] != truck_position[1]:
                return False
            else:
                return change_lane(i + 1, canvas, truck)
        else:
            return True


    def cargar_img(name):
        path = os.path.join('Images', name)
        image = PhotoImage(file=path)
        return image

        
    #Funcion para borrar de la existencia a los carritos, deme un chance a mañana y la hago jajaja
    def delete_car():
        return

    class Car:
        def __init__(self, canvas, truck, main):
            self.canvas = canvas
            self.x = 900
            self.y = random.choice(listaY)
            self.speed = -random.randint(1, 3)
            #self.rect = canvas.create_rectangle(self.x, self.y, self.x + 200, self.y + 100, width=2, fill='red')
            self.distancia = Proxi
            self.truck = truck
            self.freno = Freno
            self.CB_EW = CB_EW
            self.frenado = False
            self.main = main
            
            littlecar = cargar_img("red_car.gif")
            self.canvas.create_image(self.x, self.y, image=littlecar, anchor=NW, state=NORMAL, tag="carrito")
            self.canvas.coords("carrito")
        
            car_thread = Thread(target=self.mover)
            car_thread.daemon = True
            car_thread.start()


            

        

        def __del__(self):
            print("Deleted car")

        def mover(self):
            global stopped, cars
            if not stopped:
                self.canvas.move(self.rect, self.speed, 0)
                self.canvas.after(25, self.mover)
                self.position = self.canvas.coords(self.rect)
                truck_position = self.canvas.coords(self.truck)
                if (self.position[0]+200) >= 0:
                    if self.freno and self.CB_EW:

                        if [self.position[0]] < [truck_position[0]+200 + (Proxi / 2)] and self.position[1] == \
                                truck_position[1]:

                            self.speed = 0

                            if not self.frenado:
                                self.frenado = True
                                print(self.frenado)
                                message = tk.messagebox.showinfo(title='Frenado',
                                                                 message='Se ejecuto el frenado de emergencia por proximidad')
                                self.canvas.destroy()
                                self.main.destroy()
                                

                    if self.freno == False and self.CB_EW:
                        if [self.position[0]] < [truck_position[0] + 200 + Proxi] and self.position[1] == \
                                truck_position[1]:
                            self.speed = 0
                            if change_lane(0, self.canvas, self.truck):
                                print('siiiii')
                                if not self.frenado:
                                    self.frenado = True
                                    print(self.frenado)
                                if truck_position[1]== 260:
                                    self.canvas.coords('destroyer_truck', 10, 50, 210, 150)
                                else:
                                    self.canvas.coords('destroyer_truck', 10, 260, 210, 360)
                                message = tk.messagebox.showinfo(title='Frenado',
                                                                 message='Se ejecuto el frenado de emergencia por proximidad')
                                self.canvas.destroy()
                                self.main.destroy()
                                

                                    
                            else:
                                print('noup')
                                message = tk.messagebox.showinfo(title='Frenado',
                                                                 message='Se ejecuto el frenado de emergencia por proximidad')
                                self.canvas.destroy()
                                self.main.destroy()
                                

                            stopped = True
                else:
                    # cars.remove(self)
                    # del self
                    # print(len(cars))
                    return
            else:
                return

    def main():
        global cars, stopped
        root.withdraw()

        root_main = Toplevel()
        root_main.geometry('1200x400')
        root_main.resizable(False, False)

        highway_canvas = Canvas(root_main, width=1200, height=400, bg='gray')
        highway_canvas.place(x=0, y=0)

        truck = cargar_img("blue_truck.gif")
        highway_canvas.create_image(10, 260, image=truck, anchor=NW, state=NORMAL, tag="super_truck")
        highway_canvas.coords("super_truck")
        
        #truck_rect = highway_canvas.create_rectangle(10, 260, 210, 360, width=2, fill='blue',
                                                     #tag='destroyer_truck')
        truckPosicion = highway_canvas.coords('super_truck')

        

        '''Como crear una imagen jiji, tqm
        littlecar = cargar_img("Car.gif")
        highway_canvas.create_image(50, 50, image=littlecar, anchor=NW, state=NORMAL, tag="carrito")
        highway_canvas.coords("carrito")
        print(highway_canvas.coords("carrito"))
        '''
        
        def back():
            highway_canvas.destroy()
            root_main.destroy()
            root.deiconify()

        def move_car(s):
            if s == "UP":
                highway_canvas.coords('destroyer_truck', 10, 50, 210, 150)
            else:
                highway_canvas.coords('destroyer_truck', 10, 260, 210, 360)

        def create_car():
            global cars, stopped
            if not stopped:
                cars.append(Car(highway_canvas, 'super_truck', root_main))

                time.sleep(10)
                create_car()
            else:
                return

        red_car_thread = Thread(target=create_car)
        red_car_thread.start()

        button_up = tk.Button(highway_canvas, text='Up', font=("fixedsys", "10"),
                              bg="#82B3FF", command=lambda: move_car("UP"))
        button_up.place(x=100, y=0)
        button_down = tk.Button(highway_canvas, text='Down', font=("fixedsys", "10"),
                                bg="#82B3FF",
                                command=lambda: move_car("DOWN"))
        button_down.place(x=200, y=0)

        button = tk.Button(highway_canvas, text='Press', font=("fixedsys", "10"),
                           bg="#82B3FF", command=create_car)
        button.place(x=0, y=0)

        Btn_back = Button(highway_canvas, text='BACK', command=back, fg='black', bg='white')
        Btn_back.place(x=250, y=1)

        root_main.mainloop()

    main()


'''Ventana de configuracion'''


def config():
    global CB_EW, Freno, Proxi

    def change_txt():
        w = open('backup.txt','w')
        w.write(CB_EW)
        w.write('\n')
        w.write(Freno)
        w.write('\n')
        w.write(Proxi)
        w.close() #Cierras el archivo.
    change_txt()

    def cambiar():
        global CB_EW, Freno, Proxi

        distance = int(entry_distance.get())
        Proxi = distance

        print("El valor de CB_EW cambio es:", CB_EW)
        print("El valor de Freno cambio es:", Freno)
        print("El valor de Proxi cambio es:", Proxi)

        simu()

    def change_CB_EW(value):
        global CB_EW
        CB_EW = value

    def change_Freno(value):
        global Freno
        Freno = value

    root_config = tk.Tk()
    root_config.geometry('800x400')
    root_config.resizable(False, False)

    config_canvas = tk.Canvas(root_config, width=800, height=400, bg='gray')
    config_canvas.place(x=0, y=0)

    label1 = tk.Label(config_canvas, text="Parametro de proximidad", font=("fixedsys", 5),
                      bg='#606060', fg='#AED6F1')
    label1.place(x=75, y=99)

    label2 = tk.Label(config_canvas, text="Uso del CB-EW", font=("fixedsys", 5),
                      bg='#606060', fg='#AED6F1')
    label2.place(x=155, y=150)

    label3 = tk.Label(config_canvas, text="Metodo a utilizar", font=("fixedsys", 5),
                      bg='#606060', fg='#AED6F1')
    label3.place(x=122, y=240)

    label4 = tk.Label(config_canvas, text="Configuracion", font=("fixedsys", 20),
                      bg='#606060', fg='#AED6F1')
    label4.place(x=260, y=5)

    distance = IntVar()
    entry_distance = tk.Entry(root_config, textvariable=distance)
    entry_distance.place(x=277, y=100)

    CB_button_true = tk.Button(root_config, text="Activar",
                               command=lambda: change_CB_EW(True))
    CB_button_true.place(x=277, y=150)
    CB_button_false = tk.Button(root_config, text="Desactivar",
                                command=lambda: change_CB_EW(False))
    CB_button_false.place(x=277, y=180)

    Freno_button_true = tk.Button(root_config, text="Frenado de Emergencia",
                                  command=lambda: change_Freno(True))
    Freno_button_true.place(x=277, y=240)
    Freno_button_false = tk.Button(root_config, text="Cambio de Carril",
                                   command=lambda: change_Freno(False))
    Freno_button_false.place(x=277, y=270)

    # CBRadio1=tk.Radiobutton(root_config, text="Activado", variable=CB_EWr, value=True)
    # CBRadio1.place(x=277, y=150)

    # CBRadio2=tk.Radiobutton(root_config, text="Desactivado", variable=CB_EWr, value=False)
    # CBRadio2.place(x=277, y=180)

    # FrenoRadio1=tk.Radiobutton(root_config, text="Frenado de Emergencia", variable=Frenor, value=True)
    # FrenoRadio1.place(x=277, y=240)

    # FrenoRadio2=tk.Radiobutton(root_config, text="Cambio de Carril", variable=Frenor, value=False)
    # FrenoRadio2.place(x=277, y=270)

    SimuButton = tk.Button(config_canvas, text="Iniciar", font=("fixedsys", "15"), bg='#AED6F1',
                           command=cambiar)
    SimuButton.place(x=550, y=340)

    print("El valor de CB_EW config es:", CB_EW, ' ')
    print("El valor de Freno config es:", Freno, ' ')
    print("El valor de Proxi config es:", Proxi, ' ')

    root_config.mainloop()


'''Splash'''


def anim():
    # root.withdraw()
    global animation_time
    
    print(animation_time)

    animation_time = int(entry_time.get())
    print(animation_time)
    #animation_time = 10
    balls = []
    animation_active = True

    start_time = 0
    root_anim = tk.Tk()
    root_anim.geometry('800x400')
    root_anim.resizable(False, False)

    anim_canvas = tk.Canvas(root_anim, width=800, height=400, bg='#E8F8F5')
    anim_canvas.place(x=0, y=0)

    class Ball:
        def __init__(self, canvas):
            self.canvas = canvas
            self.x = random.randint(0, 400)
            self.y = random.randint(0, 400)
            self.r = random.randint(5, 12)
            self.speed = random.randint(2, 5)
            self.speed2 = random.randint(2, 5)
            self.oval = canvas.create_oval(self.x, self.y, self.x + 2 * self.r, self.y + 2 * self.r, fill='red')

            ball_thread = Thread(target=self.rebote)
            ball_thread.daemon = True
            ball_thread.start()

        def __del__(self):
            print("Deleted")

        def rebote(self):
            self.canvas.move(self.oval, self.speed, self.speed2)
            self.canvas.after(25, self.rebote)
            self.posicion = self.canvas.coords(self.oval)

            if self.posicion[0] > 800:
                self.speed = -self.speed
            if self.posicion[1] > 400:
                self.speed2 = -self.speed2

    def delete_balls(i):
        if i < len(balls):
            del balls[i]
            return delete_balls(i + 1)
        else:
            return

    def create_ball():
        global start_time
        print(animation_active)
        if (time.time() - start_time) < animation_time:
            ball = Ball(anim_canvas)
            balls.append(ball)
            time.sleep(0.5)
            create_ball()
        else:
            delete_balls(0)
            return

    def start_animation_thread():
        global animation_active, start_time
        start_time = time.time()
        create_ball_thread = Thread(target=create_ball)
        create_ball_thread.start()
        # time.sleep(animation_time)

    label1 = tk.Label(anim_canvas, text="Informacion de la Programadora", font=("fixedsys", 20),
                      bg="#606060", fg="#E8F8F5")
    label2 = tk.Label(anim_canvas, text="Nombre: Ingrid Vargas", font=("Haettenschweiler", 15),
                      fg="#606060")
    label3 = tk.Label(anim_canvas, text="Carnet: 2020129621", font=("Haettenschweiler", 15),
                      fg="#606060")

    
    label1.place(x=150, y=2)
    label2.place(x=20, y=70)
    label3.place(x=20, y=150)

    button = tk.Button(anim_canvas, text="Continuar", font=("fixedsys", "15"), bg='gray', fg = '#F5B7B1', 
                       command=lambda: [anim_canvas.destroy(), root_anim.destroy(), root.deiconify()])
    button.place(x=650, y=350)

    start_animation_thread()

    root_anim.mainloop()


'''Ventana de Inicio'''

root.geometry('800x400')
root.resizable(False, False)

root_canvas = tk.Canvas(root, width=800, height=400, bg='#5499C7')
root_canvas.place(x=0, y=0)

labelInicio = tk.Label(root_canvas, text="SIMULADOR CB-EW", font=("fixedsys", 20),
                       bg='#D5DBDB', fg='#1F618D')
labelInicio.place(x=260, y=50)

label_anim = tk.Label(root_canvas, text="Animacion", font=("fixedsys", 15),
                      fg='#34495E')
label_anim.place(x=150, y=150)

label_time = tk.Label(root_canvas, text="Tiempo en segundos:", font=("fixedsys", 1),
                      fg='#34495E')
label_time.place(x=120, y=180)

entry_time = tk.Entry(root, textvariable=animation_time)
entry_time.place(x=140, y=210)
      

button_anim = tk.Button(root_canvas, text='Inicio', font=('fixedsys', 14), bg='#D5DBDB', fg='#34495E',
                        command=lambda: [root.withdraw(), anim()])
button_anim.place(x=160, y=250)

label_config = tk.Label(root_canvas, text="Inicio CB-EW", font=("fixedsys", 15),
                        fg='#34495E')
label_config.place(x=490, y=150)

button_config = tk.Button(root_canvas, text="Continuar", font=("fixedsys", 14), bg='#D5DBDB', fg='#34495E',
                          command=lambda: [root.withdraw(), config()])
button_config.place(x=500, y=250)

root.mainloop()
