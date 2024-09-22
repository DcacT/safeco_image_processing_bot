import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
from main import get_avg_rgb, load_img_to_nparray, mod_img


root = tk.Tk()
root.title('safeco image manipulation bott')
images = {}
images_original = {}
sample_rgb, target_rgb = np.array([0, 0, 0]), np.array([0, 0, 0])

def display_image(canvas, img_label, path, avg_label):
    img = Image.open(path)
    img.thumbnail((200, 200))  # Resize the image to fit the canvas
    img_tk = ImageTk.PhotoImage(img)
    canvas.config(width=img_tk.width(), height=img_tk.height())
    canvas.create_image(0, 0, anchor="nw", image=img_tk)
    canvas.image = img_tk  # Keep a reference to prevent garbage collection
    
    # Calculate and display the average RGB
    avg_rgb = get_avg_rgb(path, is_path = 1)
    avg_label.config(text=f"Avg RGB (A==0): {tuple(round(num) for num in avg_rgb)}")
    
    return avg_rgb

def load_sample_image():
    path = filedialog.askopenfilename(title="Select Sample PNG", filetypes=[("PNG Files", "*.png")])
    if path:
        sample_rgb = display_image(sample_canvas, sample_img_label, path, sample_avg_label)
        images['sample'] = path
def load_target_image():
    global target_rgb
    path = filedialog.askopenfilename(title="Select Target PNG", filetypes=[("PNG Files", "*.png")])
    if path:
        target_rgb = display_image(target_canvas, target_img_label, path, target_avg_label)
        images['target'] = path

def generate_image():
    if not images.get('sample') or not images.get('target'):
        messagebox.showerror("Error", "Please select both sample and target images!")
        return
    modified_image = mod_img(images['sample'], images['target'])
    print(type(modified_image))

    img_tk = ImageTk.PhotoImage(modified_image.resize((200, 200)))
    result_canvas.config(width=img_tk.width(), height=img_tk.height())
    result_canvas.create_image(0, 0, anchor="nw", image=img_tk)
    result_canvas.image = img_tk  # Keep reference to prevent garbage collection

    images['modified'] = modified_image

def save_image():
    if 'modified' not in images:
        messagebox.showerror("Error", "No modified image to save!")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    if file_path:
        images['modified'].save(file_path)
        messagebox.showinfo("Saved", "Image saved successfully!")

# Part 1 - Sample Image
sample_frame = tk.LabelFrame(root, text="Sample", padx=10, pady=10)
sample_frame.grid(row=0, column=0, padx=10, pady=10)

sample_canvas = tk.Canvas(sample_frame, width=200, height=200)
sample_canvas.pack()

sample_avg_label = tk.Label(sample_frame, text="Avg RGB (A==0): N/A")
sample_avg_label.pack()

sample_img_label = tk.Label(sample_frame, text="No sample image")
sample_img_label.pack()

sample_button = tk.Button(sample_frame, text="Select Sample PNG", command=load_sample_image)
sample_button.pack(pady=5)

# Part 2 - Target Image
target_frame = tk.LabelFrame(root, text="Target", padx=10, pady=10)
target_frame.grid(row=0, column=1, padx=10, pady=10)

target_canvas = tk.Canvas(target_frame, width=200, height=200)
target_canvas.pack()

target_avg_label = tk.Label(target_frame, text="Avg RGB (A==0): N/A")
target_avg_label.pack()

target_img_label = tk.Label(target_frame, text="No target image")
target_img_label.pack()

target_button = tk.Button(target_frame, text="Select Target PNG", command=load_target_image)
target_button.pack(pady=5)

# Part 3 - Generate Button and Result Image
generate_button = tk.Button(root, text="Generate", command=generate_image)
generate_button.grid(row=1, column=0, columnspan=2, pady=10)

result_frame = tk.LabelFrame(root, text="Modified Image", padx=10, pady=10)
result_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

result_canvas = tk.Canvas(result_frame, width=200, height=200)
result_canvas.pack()

save_button = tk.Button(root, text="Save Modified Image", command=save_image)
save_button.grid(row=3, column=0, columnspan=2, pady=10)
root.mainloop()
