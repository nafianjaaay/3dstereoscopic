import tkinter as tk
from tkinter import Canvas, Toplevel
from PIL import Image, ImageTk

class Nimp2(tk.Frame):
    def __init__(self, parent, controller, images, rotations):
        super().__init__(parent, bg='#1a1a1a')
        self.controller = controller
        self.images = images
        self.rotations = rotations
        self.anchor_points = [None, None, None, None]

        # Main Frame
        self.main_frame = tk.Frame(self, bg='#1a1a1a')
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.preview_labels = []
        self.choose_buttons = []

        for col in range(4):
            if images[col] is not None:
                # Apply rotation
                rotated_img = images[col].rotate(self.rotations[col], expand=True)
                self.images[col] = rotated_img

                # Preview Frame
                preview_frame = tk.Frame(self.main_frame, bg='#1a1a1a', width=360, height=640)
                preview_frame.grid(row=0, column=col, padx=20, pady=10)
                preview_frame.pack_propagate(False)

                # Image Preview
                img_resized = self.resize_image(rotated_img, 360, 640)
                img_tk = ImageTk.PhotoImage(img_resized)
                preview_label = tk.Label(preview_frame, image=img_tk, bg='#000')
                preview_label.image = img_tk
                preview_label.pack(fill='both', expand=True)
                self.preview_labels.append(preview_label)

                # Choose Anchor Button
                choose_button = tk.Button(self.main_frame, text='Choose Anchor Point', 
                                          command=lambda idx=col: self.open_anchor_selector(idx), 
                                          font=('Helvetica', 14), bg='#444', fg='white', width=20, bd=0)
                choose_button.grid(row=1, column=col, pady=10)
                self.choose_buttons.append(choose_button)

        # Next Button
        self.next_button = tk.Button(self.main_frame, text='Next', 
                                     command=self.next_menu, font=('Helvetica', 18, 'bold'), 
                                     bg='#5577cc', fg='white', width=20, bd=0)
        self.next_button.grid(row=2, column=0, columnspan=4, pady=20)

    def resize_image(self, img, target_width, target_height):
        img_w, img_h = img.size
        scale = min(target_width / img_w, target_height / img_h)
        new_size = (int(img_w * scale), int(img_h * scale))
        return img.resize(new_size, Image.Resampling.LANCZOS)

    def open_anchor_selector(self, index):
        anchor_window = Toplevel(self)
        anchor_window.attributes('-fullscreen', True)
        anchor_window.configure(bg='black')
        
        # Create a Canvas for zoom and pan
        canvas = Canvas(anchor_window, bg='black')
        canvas.pack(fill='both', expand=True)
        
        # Load and display the image
        rotated_img = self.images[index]
        img_tk = ImageTk.PhotoImage(rotated_img)
        image_id = canvas.create_image(0, 0, anchor='nw', image=img_tk)
        canvas.image = img_tk
        
        # Center image
        img_w, img_h = rotated_img.size
        screen_w = anchor_window.winfo_screenwidth()
        screen_h = anchor_window.winfo_screenheight()
        offset_x = (screen_w - img_w) // 2
        offset_y = (screen_h - img_h) // 2
        canvas.move(image_id, offset_x, offset_y)

        # Store image position and scale
        self.img_offset = [offset_x, offset_y]
        self.scale_factor = 1.0

        # Crosshair
        h_line = canvas.create_line(0, screen_h // 2, screen_w, screen_h // 2, fill='red', width=2)
        v_line = canvas.create_line(screen_w // 2, 0, screen_w // 2, screen_h, fill='red', width=2)

        # Update crosshair on mouse movement
        def update_crosshair(event):
            canvas.coords(h_line, 0, event.y, screen_w, event.y)
            canvas.coords(v_line, event.x, 0, event.x, screen_h)

        # Save anchor point on click
        def save_anchor(event):
            # Convert to image coordinates
            img_x = (event.x - self.img_offset[0]) / self.scale_factor
            img_y = (event.y - self.img_offset[1]) / self.scale_factor
            self.anchor_points[index] = (img_x, img_y)
            print(f"Anchor Point for Photo {index+1} set to: ({img_x}, {img_y})")
            anchor_window.destroy()

        # Movement with WASD and Arrow Keys
        def move_image(dx, dy):
            self.img_offset[0] += dx
            self.img_offset[1] += dy
            canvas.move(image_id, dx, dy)

        # Bind movement keys
        def on_key_press(event):
            step = 10
            if event.keysym in ['w', 'Up']:
                move_image(0, -step)
            elif event.keysym in ['s', 'Down']:
                move_image(0, step)
            elif event.keysym in ['a', 'Left']:
                move_image(-step, 0)
            elif event.keysym in ['d', 'Right']:
                move_image(step, 0)
            elif event.keysym == '=':
                zoom(1.1)
            elif event.keysym == '-':
                zoom(0.9)

        # Zoom and pan
        def zoom(scale):
            self.scale_factor *= scale
            canvas.scale('all', screen_w // 2, screen_h // 2, scale, scale)
            canvas.configure(scrollregion=canvas.bbox('all'))

        # Shift + Scroll Zoom
        def on_scroll(event):
            if event.state & 0x0001:  # Shift key is pressed
                scale = 1.1 if event.delta > 0 else 0.9
                zoom(scale)

        # Mouse bindings
        canvas.bind('<Motion>', update_crosshair)
        canvas.bind('<Button-1>', save_anchor)
        canvas.bind("<MouseWheel>", on_scroll)
        anchor_window.bind("<KeyPress>", on_key_press)
        anchor_window.focus_set()

    def next_menu(self):
        # Placeholder for the next page
        print("Next page coming soon...")
