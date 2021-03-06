from tkinter import *             #Importar todo de la libreria de Tkinter para realizar la GUI
import tkinter as tk
from tkinter import messagebox    #Importar especificamente el Messagebox para realizar los mensajes al usuario
import random                     #Importar Random para la aparicion de los autos y la velocidad
import time                       #Importar Time para el Splash
from threading import Thread      #Importar threading para el uso de hilos
import os                         #Importar os para el uso de imagenes

#Variables globales
global CB_EW, Freno, Proxi, cars, stopped, animation_time

CB_EW = True
Freno = True
Proxi = 100
cars = []
stopped = False
animation_time = 10


#Inicio de la ventana principal
root = tk.Tk()


#Funcion para leer los datos almacenados en el txt
def read_txt():
    global CB_EW, Freno, Proxi
    w = open('backup.txt', 'r')
    CB_EW = w.readline()
    Freno = w.readline()
    Proxi = w.readline()
read_txt()

#Lista de las posiciones en Y
listaY = [50, 260]


#Funcion para cargar imagenes
#E: nombre del archivo a cargar
#S: variable con la imagen cargada
def cargar_img(name):
    path = os.path.join('Images', name)
    image = PhotoImage(file=path)
    return image


#Funcion para verificar si es posible realizar el cambio de carril
#E: Indice para la lista de carros,  el canvas donde se esta realizando la simulacion, el objeto truck
#S: Boolean se es posible el cambio de carril
def change_lane(i, canvas, truck):
    global cars

    truck_position = canvas.coords(truck)
    if i < len(cars):
        car = cars[i]
        car_position = car.canvas.coords(car.image)
        print(len(car_position))
        if car_position[0] < (truck_position[0] + 200 + (Proxi * 2)) and car_position[1] != truck_position[1]:
            return False
        else:
            return change_lane(i + 1, canvas, truck)
    else:
        return True


#Clase para la creacion de los automoviles
class Car:

    #Funcion para crear el objeto
    #E: el canvas donde se realiza la animacion, el objeto truck, la ventana donde se encuentra el canvas y el identificador del automovil
    def __init__(self, canvas, truck, main, id):
        self.id = id
        self.canvas = canvas
        self.x = 900
        self.y = random.choice(listaY)
        self.speed = -random.randint(1, 3)
        self.distancia = Proxi
        self.truck = truck
        self.freno = Freno
        self.out = False
        self.CB_EW = CB_EW
        self.frenado = False
        self.main = main

        self.image_cache = cargar_img("red_car.gif")
        self.image = self.canvas.create_image(self.x, self.y, image=self.image_cache, anchor=NW, state=NORMAL,
                                              tag="carrito")

        self.canvas.coords("carrito")

        car_thread = Thread(target=lambda: self.mover(self.image))
        car_thread.daemon = True
        car_thread.start()

    #Funcion para mostrar en shell cuando se elimina un automovil de la lista
    def __del__(self):
        print("Deleted car")

    #Funcion para eliminar los automoviles de la lista que los almacena
    def delete_car(self, i):
        global cars
        print("Deleting car")
        if i < len(cars):
            print(self.id)
            if cars[i].id == self.id:
                print("True")
                cars.remove(cars[i])
                return
            return self.delete_car(i + 1)
        else:
            return

    #Funcion para realizar el movimiento de los automoviles y para verificar cuando se realiza la proximacion
    def mover(self, image):
        global stopped, cars
        if not stopped and not self.out:
            self.canvas.move(image, self.speed, 0)
            self.canvas.after(25, lambda: self.mover(image))
            self.position = self.canvas.coords(image)
            truck_position = self.canvas.coords(self.truck)

            if (self.position[0] + 200) >= 0:

                if self.freno and self.CB_EW:
                    if [self.position[0]] < [truck_position[0] + 200 + (Proxi / 2)] and self.position[1] == \
                            truck_position[1]:
                        self.speed = 0
                        if not self.frenado:
                            self.frenado = True
                            stopped = True
                            message = tk.messagebox.showinfo(title='Frenado',
                                                             message='Se ejecuto el frenado de emergencia por proximidad')
                            self.canvas.destroy()
                            self.main.destroy()

                if self.freno == False and self.CB_EW:
                    if [self.position[0]] < [truck_position[0] + 200 + Proxi] and self.position[1] == truck_position[1]:
                        self.speed = 0
                        if change_lane(0, self.canvas, self.truck):
                            #print('siiiii')
                            if not self.frenado:
                                self.frenado = True
                                if truck_position[1] == 260:
                                    self.canvas.coords('super_truck', 10, 50)
                                else:
                                    self.canvas.coords('super_truck', 10, 260)
                                stopped = True
                                message = tk.messagebox.showinfo(title='Frenado',
                                                                message='Se realizo el cambio de carril')
                                self.canvas.destroy()
                                self.main.destroy()
                        else:
                            #print('noup')
                            stopped = True
                            message = tk.messagebox.showinfo(title='Frenado',
                                                             message='No se puede realizar el cambio de carril')
                            self.canvas.destroy()
                            self.main.destroy()
                if self.CB_EW == False:
                    if [self.position[0]] < [truck_position[0] + 200] and self.position[1] == \
                            truck_position[1]:
                        self.speed = 0
                        if not self.frenado:
                            self.frenado = True
                            stopped = True
                            message = tk.messagebox.showinfo(title='Frenado',
                                                             message='Se ha producido un accidente')
                            self.canvas.destroy()
                            self.main.destroy()


            else:
                self.out = True
                self.delete_car(0)
                print(len(cars))
                return
        else:
            return


'''Simulador'''

#Funcion donde se realiza toda la simulacion
def simu():
    global CB_EW, Proxi, Freno, cars, stopped

    print("El valor de CB_EW simu es:", CB_EW)
    print("El valor de Freno simu es:", Freno)
    print("El valor de Proxi simu es:", Proxi)

    #Funcion donde se crea la ventana y el canvas de la simulacion
    def main():

        global cars, stopped

        root.withdraw()

        root_main = Toplevel()
        root_main.geometry('1200x400')
        root_main.resizable(False, False)
        root_main.title('Simulador')
        highway_canvas = Canvas(root_main, width=1200, height=400, bg='gray')
        highway_canvas.pack(expand=1, fill=BOTH)
        highway_canvas.place(x=0, y=0)

        truck = cargar_img("blue_truck.gif")
        highway_canvas.create_image(10, 260, image=truck, anchor=NW, state=NORMAL, tag="super_truck")

        truckPosicion = highway_canvas.coords('super_truck')

        #Funcion para el boton Back
        def back():
            highway_canvas.destroy()
            root_main.destroy()
            root.deiconify()

        #Funcion para cambiar la ubicacion del truck a disposicion del usuario
        def move_car(s):
            if s == "UP":
                highway_canvas.coords('super_truck', 10, 50)
            else:
                highway_canvas.coords('super_truck', 10, 260)

        button_up = tk.Button(highway_canvas, text='Up', font=("fixedsys", "10"),
                              bg="#82B3FF", command=lambda: move_car("UP"))
        #button_up.place(x=100, y=0)
        button_down = tk.Button(highway_canvas, text='Down', font=("fixedsys", "10"),
                                bg="#82B3FF",
                                command=lambda: move_car("DOWN"))
        #button_down.place(x=200, y=0)


        Btn_back = Button(highway_canvas, text='BACK', command=back, fg='black', bg='white')
        Btn_back.place(x=2, y=1)

        #Funcion para la creacion de los automoviles
        #E: el canvas donde se ejecuta la simulacion y el id del automovil
        def create_car(canvas, id):
            global cars, stopped
            if not stopped:
                car = Car(canvas, 'super_truck', root_main, id)
                cars.append(car)

                time.sleep(10)
                create_car(canvas, id + 1)
            else:
                return

        # Car(highway_canvas, 'super_truck', root_main)
        red_car_thread = Thread(target=create_car, args=[highway_canvas, 0])
        red_car_thread.start()

        root_main.mainloop()

    main()


'''Ventana de configuracion'''

#Funcion donde se almacena la ventana de configuracion del CB-EW
def config():
    global CB_EW, Freno, Proxi

    #Funcion para cambiar los valores globales de CB-EW, Freno y Proxi
    def cambiar():
        global CB_EW, Freno, Proxi, stopped

        stopped = False
        distance = int(entry_distance.get())
        Proxi = distance

        print("El valor de CB_EW cambio es:", CB_EW)
        print("El valor de Freno cambio es:", Freno)
        print("El valor de Proxi cambio es:", Proxi)

        #Funcion para cambiar los valores del txt
        def change_txt():
            w = open('backup.txt', 'w')
            w.writelines(str(CB_EW) + '\n' + str(Freno) + '\n' + str(Proxi))
            w.close()  # Cierras el archivo.
        change_txt()

        simu()

    #Funcion para cambiar el valor de la variable CB-EW
    def change_CB_EW(value):
        global CB_EW
        CB_EW = value

    #Funcion para cambiar el valor de la variable Freno
    def change_Freno(value):
        global Freno
        Freno = value


    root_config = tk.Tk()
    root_config.geometry('800x400')
    root_config.resizable(False, False)
    root_config.title('Configuracion del CB-EW')
    config_canvas = tk.Canvas(root_config, width=800, height=400, bg='gray')
    config_canvas.place(x=0, y=0)

    label1 = tk.Label(config_canvas, text="Parametro de proximidad (cm)", font=("fixedsys", 5),
                      bg='#606060', fg='#AED6F1')
    label1.place(x=35, y=99)

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


    SimuButton = tk.Button(config_canvas, text="Iniciar", font=("fixedsys", "15"), bg='#AED6F1',
                           command=cambiar)
    SimuButton.place(x=550, y=340)

    print("El valor de CB_EW config es:", CB_EW, ' ')
    print("El valor de Freno config es:", Freno, ' ')
    print("El valor de Proxi config es:", Proxi, ' ')

    root_config.mainloop()


'''Splash'''

#Funcion donde se ejecuta el splash animado
def anim():

    global animation_time

    print(animation_time)

    animation_time = int(entry_time.get())
    print(animation_time)
    balls = []
    animation_active = True

    start_time = 0
    root_anim = tk.Tk()
    root_anim.geometry('800x400')
    root_anim.resizable(False, False)
    root_anim.title('Splash')

    anim_canvas = tk.Canvas(root_anim, width=800, height=400, bg='#E8F8F5')
    anim_canvas.place(x=0, y=0)

    #Clase donde se generan las bolas
    class Ball:

        #Creacion de las bolas
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

        #Funcion que mueve ls bolas
        def rebote(self):
            self.canvas.move(self.oval, self.speed, self.speed2)
            self.canvas.after(25, self.rebote)
            self.posicion = self.canvas.coords(self.oval)

            if self.posicion[0] > 800:
                self.speed = -self.speed
            if self.posicion[1] > 400:
                self.speed2 = -self.speed2

    #Funcion para borrar las bolas de la lista
    def delete_balls(i):
        if i < len(balls):
            del balls[i]
            return delete_balls(i + 1)
        else:
            return

    #Funcion para crear las bolas en el rango de tiempo brindado
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

    #Funcion para el inico del hilo de la creacion de bolas
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

    button = tk.Button(anim_canvas, text="Continuar", font=("fixedsys", "15"), bg='gray', fg='#F5B7B1',
                       command=lambda: [anim_canvas.destroy(), root_anim.destroy(), root.deiconify()])
    button.place(x=650, y=350)

    start_animation_thread()

    root_anim.mainloop()


'''Ventana de Inicio'''

#Creacion de la ventana de inicio del programa

root.geometry('800x400')
root.resizable(False, False)
root.title('Inicio')
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
