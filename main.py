import os
import shutil
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk

class ImageViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")
        self.root.geometry("600x600")
        
        self.image_label = tk.Label(self.root, text="Select a directory to view images", font=("Arial", 12, "bold"), pady=10)
        self.image_label.pack()
        
        self.canvas = tk.Canvas(self.root, width=500, height=400, bg="gray", highlightthickness=2, relief="ridge")
        self.canvas.pack(pady=10)
        
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.btn_select_dir = tk.Button(button_frame, text="Select Directory", command=self.load_images, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        self.btn_select_dir.grid(row=0, column=0, padx=5)
        
        self.btn_prev = tk.Button(button_frame, text="Previous", command=self.prev_image, bg="#008CBA", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        self.btn_prev.grid(row=0, column=1, padx=5)
        
        self.btn_next = tk.Button(button_frame, text="Next", command=self.next_image, bg="#008CBA", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        self.btn_next.grid(row=0, column=2, padx=5)
        
        self.btn_add_category = tk.Button(button_frame, text="Add Category", command=self.add_category, bg="#f39c12", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        self.btn_add_category.grid(row=0, column=3, padx=5)
        
        self.category_frame = tk.Frame(self.root)
        self.category_frame.pack(pady=10)
        
        self.image_list = []
        self.current_index = 0
        self.categories = {}
        self.category_buttons = []
        
        self.root.bind("<KeyPress>", self.key_pressed)

    def load_images(self):
        dir_path = filedialog.askdirectory()
        if not dir_path:
            return
        
        self.image_list = [os.path.join(dir_path, f) for f in os.listdir(dir_path) 
                           if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]
        
        if self.image_list:
            self.current_index = 0
            self.display_image()
        else:
            self.image_label.config(text="No images found in the selected directory")
            self.canvas.delete("all")

    def display_image(self):
        try:
            img_path = self.image_list[self.current_index]
            img = Image.open(img_path)
            img.thumbnail((500, 400))
            img = ImageTk.PhotoImage(img)

            self.canvas.delete("all")
            self.canvas.create_image(250, 200, image=img)
            self.canvas.image = img

            self.image_label.config(text=os.path.basename(img_path))
        except OSError:
            self.image_label.config(text="Corrupted image, skipping...")
            self.next_image()

    def next_image(self):
        if self.image_list and self.current_index < len(self.image_list) - 1:
            self.current_index += 1
            self.display_image()
    
    def prev_image(self):
        if self.image_list and self.current_index > 0:
            self.current_index -= 1
            self.display_image()
    
    def add_category(self):
        category_name = simpledialog.askstring("Add Category", "Enter category name:")
        if category_name and category_name not in self.categories:
            index = len(self.category_buttons) + 1
            row, col = divmod(len(self.category_buttons), 3)  # Arrange buttons in grid
            category_btn = tk.Button(self.category_frame, text=f"{index}. {category_name}", command=lambda cn=category_name: self.move_image_to_category(cn), bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
            category_btn.grid(row=row, column=col, padx=5, pady=5)
            self.categories[category_name] = category_btn
            self.category_buttons.append(category_btn)
    
    def move_image_to_category(self, category_name):
        if self.image_list:
            img_path = self.image_list[self.current_index]
            category_folder = os.path.join(os.getcwd(), category_name)
            os.makedirs(category_folder, exist_ok=True)
            shutil.copy(img_path, os.path.join(category_folder, os.path.basename(img_path)))
            self.image_label.config(text=f"Moved to {category_name}")
            self.next_image()

    def key_pressed(self, event):
        if event.char.isdigit():
            index = int(event.char) - 1
            if 0 <= index < len(self.category_buttons):
                category_name = list(self.categories.keys())[index]
                self.move_image_to_category(category_name)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewerApp(root)
    root.mainloop()