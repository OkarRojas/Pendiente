import tkinter as tk
from PIL import Image, ImageTk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Platformer Game")
        self.root.geometry("900x600")
        
        # Variables de control
        self.moving_left = False
        self.moving_right = False
        self.jumping = False
        self.falling = False
        self.velocity_y = 0
        self.gravity = 0.8
        self.jump_strength = -16
        self.move_speed = 5
        
        # Configuración del canvas
        self.canvas = tk.Canvas(root, width=900, height=600, bg="lightblue")
        self.canvas.pack(fill="both", expand=False)
        
        # Crear plataformas
        self.platforms = [
            self.canvas.create_rectangle(0,500,-400,0, fill="black"),
            self.canvas.create_rectangle(400, 400, 500, 420, fill="green", outline="black"),  # Plataforma 1
            self.canvas.create_rectangle(600, 300, 700, 320, fill="green", outline="black"),  # Plataforma 2
            self.canvas.create_rectangle(200, 200, 300, 220, fill="green", outline="black"),  # Plataforma 3
            self.canvas.create_rectangle(0, 500, 900, 520, fill="brown", outline="black"),
            self.canvas.create_rectangle(100, 500, 150, 450, fill="red", outline="black")     # Suelo
        ]
        
        # Cargar sprites
        sprite_paths = [
            f"C:\\Users\\oscar\\Documents\\Mi_primer_juego\\craftpix-net-563568-free-wraith-tiny-style-2d-sprites\\PNG\\Wraith_01\\PNG Sequences\\Idle\\Wraith_01_Idle_0{str(i).zfill(2)}.png"
            for i in range(12)
        ]
       
        self.frames = []
        target_size = (64, 64)
        
        for path in sprite_paths:
            try:
                image = Image.open(path)
                resized_image = image.resize(target_size, Image.Resampling.LANCZOS)
                frame_tk = ImageTk.PhotoImage(resized_image)
                self.frames.append(frame_tk)
            except:
                # Crear un frame de relleno si no se puede cargar la imagen
                placeholder = Image.new('RGBA', target_size, (255, 0, 0, 255))
                frame_tk = ImageTk.PhotoImage(placeholder)
                self.frames.append(frame_tk)
        
        self.current_frame = 0
        self.sprite = self.canvas.create_image(200, 480, image=self.frames[self.current_frame], anchor='s')
        
        # Iniciar bucles de actualización
        self.animate()
        self.update_movement()
        self.update_physics()
        
        # Configurar eventos de teclado
        self.setup_bindings()

    def setup_bindings(self):
        self.root.bind("<KeyPress-a>", self.start_moving_left)
        self.root.bind("<KeyRelease-a>", self.stop_moving_left)
        self.root.bind("<KeyPress-d>", self.start_moving_right)
        self.root.bind("<KeyRelease-d>", self.stop_moving_right)
        self.root.bind("<KeyPress-space>", self.jump)
        self.root.focus_set()  # Asegurar que la ventana captura las teclas

    def start_moving_left(self, event):
        self.moving_left = True

    def stop_moving_left(self, event):
        self.moving_left = False

    def start_moving_right(self, event):
        self.moving_right = True

    def stop_moving_right(self, event):
        self.moving_right = False

    def animate(self):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.canvas.itemconfig(self.sprite, image=self.frames[self.current_frame])
        self.root.after(100, self.animate)

    def update_movement(self):
        dx = 0
        if self.moving_left:
            dx -= self.move_speed
        if self.moving_right:
            dx += self.move_speed
            
        if dx != 0:
            self.canvas.move(self.sprite, dx, 0)
            # Verificar colisiones laterales después de mover
            self.check_collision()
            
        self.root.after(16, self.update_movement)  # ~60 FPS

    def jump(self, event):
        if not self.jumping and not self.falling:
            self.jumping = True
            self.velocity_y = self.jump_strength
            self.falling = False

    def is_on_platform(self):
        # Obtener la posición y el bounding box del sprite
        sprite_bbox = self.canvas.bbox(self.sprite)
        if not sprite_bbox:
            return False
            
        # Ajustar el bounding box para comprobar solo los pies (un poco por debajo del sprite)
        feet_bbox = (sprite_bbox[0], sprite_bbox[3] - 5, sprite_bbox[2], sprite_bbox[3] + 5)
        
        # Verificar colisión con cada plataforma
        for platform in self.platforms:
            platform_bbox = self.canvas.bbox(platform)
            
            # Comprobar si los pies del sprite están tocando la plataforma
            if (feet_bbox[2] > platform_bbox[0] and feet_bbox[0] < platform_bbox[2] and
                feet_bbox[3] > platform_bbox[1] and feet_bbox[1] < platform_bbox[3] and
                self.velocity_y >= 0):
                return True
                
        return False

    def update_physics(self):
        # Siempre aplicar gravedad si no estamos en una plataforma
        if not self.is_on_platform():
            self.falling = True
        else:
            # Si estamos en una plataforma y no saltando, detener la caída
            if self.velocity_y > 0:
                self.velocity_y = 0
                self.falling = False
                self.jumping = False

        # Aplicar gravedad si estamos cayendo o saltando
        if self.falling or self.jumping:
            self.velocity_y += self.gravity
            self.canvas.move(self.sprite, 0, self.velocity_y)
            
        # Verificar colisiones después de aplicar la física
        self.check_collision()
            
        self.root.after(16, self.update_physics)  # ~60 FPS

    def check_collision(self):
        # Obtener posición actual del sprite
        x, y = self.canvas.coords(self.sprite)
        sprite_bbox = self.canvas.bbox(self.sprite)
        if not sprite_bbox:
            return
        
        # Verificar colisión con cada plataforma
        for platform in self.platforms:
            platform_bbox = self.canvas.bbox(platform)
            
            # Si hay colisión, ajustar la posición
            if (sprite_bbox[2] > platform_bbox[0] and sprite_bbox[0] < platform_bbox[2] and
                sprite_bbox[3] > platform_bbox[1] and sprite_bbox[1] < platform_bbox[3]):
                
                # Colisión desde arriba (cayendo sobre la plataforma)
                if self.velocity_y > 0 and sprite_bbox[3] > platform_bbox[1]:
                    # Colocamos el sprite justo encima de la plataforma
                    self.canvas.coords(self.sprite, x, platform_bbox[1] - 32)
                    self.velocity_y = 0
                    self.jumping = False
                    self.falling = False
                
                # Colisión lateral desde la derecha
                elif self.moving_right and sprite_bbox[2] > platform_bbox[0] and sprite_bbox[0] < platform_bbox[0]:
                    self.canvas.coords(self.sprite, platform_bbox[0] - 32, y)
                
                # Colisión lateral desde la izquierda
                elif self.moving_left and sprite_bbox[0] < platform_bbox[2] and sprite_bbox[2] > platform_bbox[2]:
                    self.canvas.coords(self.sprite, platform_bbox[2] + 32, y)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()