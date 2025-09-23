import tkinter

class MyWindow:
    def __init__(self, master):
        self.master = master
        master.title("Mi Ventana con Rectángulo")
        master.geometry("600x400")
        master.resizable(False, False)

        ## Velocidades
        self.xvelociti = 10
        self.jump_strength = 20 # Aumentado para un salto más alto
        self.gravity = 1.5
        self.velocity_y = 0

        ## Altura del suelo
        self.suelo = 350

        # Variables de estado para el movimiento
        self.moving_left = False
        self.moving_right = False
        self.on_ground = True

        self.canvas = tkinter.Canvas(master, width=600, height=400, bg="lightblue")
        self.canvas.pack()
        self.platforms = []

        # Dibujar un rectángulo que ocupe toda la parte inferior
        # Las coordenadas son (x1, y1, x2, y2)
        # x1=0, y1=altura_ventana - altura_rectangulo, x2=ancho_ventana, y2=altura_ventana
        self.ps = self.canvas.create_rectangle(0, 350, 600, 400, fill="brown", outline="black")
        self.m = self.canvas.create_rectangle(300, 200, 350, 250, fill="black", outline="black")
        self.p = self.canvas.create_rectangle(0, 200, 50, 250, fill="blue", outline="black")
        self.l = self.canvas.create_rectangle(150, 200, 200, 250, fill="brown", outline="black")
        self.v = self.canvas.create_rectangle(200, 150, 250, 200, fill="brown", outline="black")
        self.u = self.canvas.create_rectangle(650, 300, 700, 350, fill="brown", outline="black")
        self.p1 = self.canvas.create_rectangle(800, 250, 950, 275, fill="black", outline="black")
        self.p2 = self.canvas.create_rectangle(650, 150, 450, 175, fill="black", outline="black")
        
        # Añadir objetos con los que se puede colisionar a una lista
        self.platforms.extend([self.m])
        self.platforms.extend([self.l])
        self.platforms.extend([self.v])
        self.platforms.extend([self.p1])
        self.platforms.extend([self.p2])



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
            self.velocity_y = -self.jump_strength
            self.on_ground = False

    def update_game(self):
        count = 0
        # 1. Manejar movimiento y colisión horizontal
        dx = 0
        if self.moving_right:
            dx += self.xvelociti
        if self.moving_left:
            dx -= self.xvelociti


        if self.canvas.coords(self.p)[2]>500:
            self.canvas.move("all", -10, 0)
        if self.canvas.coords(self.p)[0]<100 and self.canvas.coords(self.ps)[0]<0:
            self.canvas.move("all", 10, 0)
        
        self.canvas.move(self.p, dx, 0)
        self.check_horizontal_collisions()

        # 2. Manejar movimiento y colisión vertical (gravedad y salto)
        self.velocity_y += self.gravity
        self.canvas.move(self.p, 0, self.velocity_y)
        self.check_vertical_collisions()

        # Volver a llamar a esta función después de 16ms (~60 FPS)
        self.master.after(4, self.update_game)

    def check_horizontal_collisions(self):
        p_coords = self.canvas.coords(self.p)
        # Colisión con los bordes de la ventana
        if p_coords[0] < 0:
            self.canvas.coords(self.p, 0, p_coords[1], 50, p_coords[3])
        elif p_coords[2] > 600:
            self.canvas.coords(self.p, 600 - 50, p_coords[1], 600, p_coords[3])

        for platform in self.platforms:
            plat_coords = self.canvas.coords(platform)
            if (p_coords[2] > plat_coords[0] and p_coords[0] < plat_coords[2] and
                p_coords[3] > plat_coords[1] and p_coords[1] < plat_coords[3]):
                # Colisionó, determinar de qué lado
                if self.moving_right: # Chocó con el lado izquierdo de la plataforma
                    self.canvas.coords(self.p, plat_coords[0] - 50, p_coords[1], plat_coords[0], p_coords[3])
                elif self.moving_left: # Chocó con el lado derecho de la plataforma
                    self.canvas.coords(self.p, plat_coords[2], p_coords[1], plat_coords[2] + 50, p_coords[3])

    def check_vertical_collisions(self):
        p_coords = self.canvas.coords(self.p)
        self.on_ground = False

        # Colisión con el suelo principal
        if p_coords[3] >= self.suelo:
            self.canvas.coords(self.p, p_coords[0], self.suelo - 50, p_coords[2], self.suelo)
            self.velocity_y = 0
            self.on_ground = True

        for platform in self.platforms:
            plat_coords = self.canvas.coords(platform)
            if (p_coords[2] > plat_coords[0] and p_coords[0] < plat_coords[2] and
                p_coords[3] > plat_coords[1] and p_coords[1] < plat_coords[3]):
                # Cayendo sobre la plataforma
                if self.velocity_y > 0:
                    self.canvas.coords(self.p, p_coords[0], plat_coords[1] - 50, p_coords[2], plat_coords[1])
                    self.velocity_y = 0
                    self.on_ground = True
                # Saltando y chocando desde abajo
                elif self.velocity_y < 0:
                    self.canvas.coords(self.p, p_coords[0], plat_coords[3], p_coords[2], plat_coords[3] + 50)
                    self.velocity_y = 0

root = tkinter.Tk()
my_window = MyWindow(root)
root.mainloop()
