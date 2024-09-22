import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np

# Function to calculate the average RGB values where alpha is 0
def calculate_average_rgb(image_path):

    Img = Image.open(image_path).convert('RGBA')
    Img_Pixels = np.array(Img)

    r, g, b, a = Img_Pixels[:,:,0], Img_Pixels[:,:,1], Img_Pixels[:,:,2], Img_Pixels[:,:,3]
    average_r = np.mean(r[a>0])
    average_g = np.mean(g[a>0])
    average_b = np.mean(b[a>0])
    
    return (average_r , average_g , average_b)

# Function to display image on the canvas
def display_image(canvas, img_label, path, avg_label):
    img = Image.open(path)
    img.thumbnail((200, 200))  # Resize the image to fit the canvas
    img_tk = ImageTk.PhotoImage(img)
    canvas.config(width=img_tk.width(), height=img_tk.height())
    canvas.create_image(0, 0, anchor="nw", image=img_tk)
    canvas.image = img_tk  # Keep a reference to prevent garbage collection
    
    # Calculate and display the average RGB
    avg_rgb = calculate_average_rgb(path)
    avg_label.config(text=f"Avg RGB (A==0): {avg_rgb.astype(int)}")
    
    return avg_rgb

# Function to load sample image
def load_sample_image():
    global sample_rgb
    path = filedialog.askopenfilename(title="Select Sample PNG", filetypes=[("PNG Files", "*.png")])
    if path:
        sample_rgb = display_image(sample_canvas, sample_img_label, path, sample_avg_label)
        images['sample'] = path

# Function to load target image
def load_target_image():
    global target_rgb
    path = filedialog.askopenfilename(title="Select Target PNG", filetypes=[("PNG Files", "*.png")])
    if path:
        target_rgb = display_image(target_canvas, target_img_label, path, target_avg_label)
        images['target'] = path

# Function to generate the modified image
def generate_image():
    if not images.get('sample') or not images.get('target'):
        messagebox.showerror("Error", "Please select both sample and target images!")
        return

    # Calculate the difference between the sample and target average RGB values
    diff_rgb = sample_rgb - target_rgb
    
    # Load the target image and apply the modifications
    target_img = Image.open(images['target']).convert('RGBA')
    np_target = np.array(target_img, dtype=np.float32)  # Use float32 for calculations
    
    # Modify pixels where alpha is not 0
    alpha_channel = np_target[:, :, 3]
    non_zero_alpha_mask = alpha_channel != 0
    
    np_target[non_zero_alpha_mask, :3] += diff_rgb.astype(float)
    
    # Clip the values to ensure they are within valid RGB range
    np_target[:, :3] = np.clip(np_target[:, :3], 0, 255)
    
    # Convert back to uint8
    np_target = np_target.astype(np.uint8)
    
    # Create and display the modified image
    modified_img = Image.fromarray(np_target)
    modified_img.thumbnail((200, 200))
    img_tk = ImageTk.PhotoImage(modified_img)
    result_canvas.config(width=img_tk.width(), height=img_tk.height())
    result_canvas.create_image(0, 0, anchor="nw", image=img_tk)
    result_canvas.image = img_tk  # Keep reference to prevent garbage collection

    images['modified'] = modified_img
# Function to save the modified image
def save_image():
    if 'modified' not in images:
        messagebox.showerror("Error", "No modified image to save!")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    if file_path:
        images['modified'].save(file_path)
        messagebox.showinfo("Saved", "Image saved successfully!")

# Set up tkinter window
root = tk.Tk()
root.title("Image Manipulation with RGB Calculation")

images = {}
sample_rgb, target_rgb = np.array([0, 0, 0]), np.array([0, 0, 0])

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