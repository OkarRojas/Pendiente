import tkinter

class MyWindow:
    def __init__(self, master):
        self.master = master
        master.title("Mi Ventana con Rectángulo")
        master.geometry("400x300")
        master.resizable(False, False)

        ## Velocidades
        self.xvelociti = 10
        self.yvelociti = 200
        self.lvelociti = -10

        ## Altura del suelo
        self.suelo = 250


        # Variables de estado para el movimiento
        self.moving_left = False
        self.moving_right = False
        self.on_ground = True

        self.canvas = tkinter.Canvas(master, width=400, height=300, bg="lightblue")
        self.canvas.pack()

        # Dibujar un rectángulo que ocupe toda la parte inferior
        # Las coordenadas son (x1, y1, x2, y2)
        # x1=0, y1=altura_ventana - altura_rectangulo, x2=ancho_ventana, y2=altura_ventana
        self.canvas.create_rectangle(0, 250, 400, 300, fill="brown", outline="black")
        self.m = self.canvas.create_rectangle(300, 200, 350, 250, fill="black", outline="black")
        self.p =self.canvas.create_rectangle(0, 200, 50, 250, fill="brown", outline="black")

        # Iniciar el bucle de gravedad
        self.update_game()

        # Binds para presionar y soltar teclas
        self.master.bind("<KeyPress-d>", self.start_moving_right)
        self.master.bind("<KeyRelease-d>", self.stop_moving_right)
        self.master.bind("<KeyPress-a>", self.start_moving_left)
        self.master.bind("<KeyRelease-a>", self.stop_moving_left)
        self.master.bind("<KeyPress-w>", self.jump)



    def start_moving_right(self, event):
        self.moving_right = True

    def stop_moving_right(self, event):
        self.moving_right = False

    def start_moving_left(self, event):
        self.moving_left = True

    def stop_moving_left(self, event):
        self.moving_left = False

    def jump(self, event):
        # Solo se puede saltar si está en el suelo
        if self.on_ground:
            self.canvas.move(self.p, 0, -self.yvelociti)
            self.on_ground = False

    

    def create (self):
        self.p =self.canvas.create_rectangle(0, 250, 50, 200, fill="brown", outline="black")

    def update_game(self):
        # Movimiento horizontal basado en las variables de estado
        if self.moving_right:
            self.canvas.move(self.p, self.xvelociti, 0)
        if self.moving_left:
            self.canvas.move(self.p, self.lvelociti, 0)

        # Obtener coordenadas actuales del rectángulo p [x1, y1, x2, y2]
        pos = self.canvas.coords(self.p)
        # Si la parte inferior del rectángulo (pos[3]) no ha llegado al suelo (y=250)
        if pos[3] < self.suelo:
            # Mover el rectángulo hacia abajo (eje y positivo)
            self.canvas.move(self.p, 0, 5)
            self.on_ground = False
        else:
            self.on_ground = True

        # Llamar al método de colisión en cada fotograma
        
        self.coli()


        # Volver a llamar a esta función después de 16ms (~60 FPS)
        self.master.after(16, self.update_game)

    def hit(self):
        # Obtener las coordenadas de los bounding box de cada rectángulo
        p_coords = self.canvas.coords(self.p)
        m_coords = self.canvas.coords(self.m)

        # Verificar si los bounding box se superponen (hay colisión)
        # p_coords = [x1, y1, x2, y2]
        try:
            if (p_coords[2] > m_coords[0] and p_coords[0] < m_coords[2] and
                p_coords[3] > m_coords[1] and p_coords[1] < m_coords[3]):
                print("colision")
                self.canvas.delete(self.p)
                self.create()
        except:
            print("personaje no encontrado")

    def coli(self):
       p_coords = self.canvas.coords(self.p)
       m_coords = self.canvas.coords(self.m)

       print(p_coords[2])
       print(m_coords[0])


       if (p_coords[2] +10 > m_coords[0]) and p_coords[3] +10 > m_coords[1] and p_coords[0] < m_coords[2] and p_coords[3]:
           self.xvelociti = 0
           self.suelo = 200
       else:
          self.xvelociti = 10
          self.suelo = 250

           

       


root = tkinter.Tk()
my_window = MyWindow(root)
root.mainloop()
