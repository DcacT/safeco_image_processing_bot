from PIL import Image
import numpy as np
import matplotlib.pyplot as plt




Img_Sample_Path = r'C:\Users\steve\Documents\safeco_image_mod_bot\safeco_image_processing_bot\main\1_og.png'
Img_Target_Path = r'C:\Users\steve\Documents\safeco_image_mod_bot\safeco_image_processing_bot\main\IMG_3569_modded.png'

def get_avg_rgb(input_img, is_path = 0):
    if is_path == 1:
        input_img = load_img_to_nparray(input_img)
    r, g, b, a = input_img[:,:,0], input_img[:,:,1], input_img[:,:,2], input_img[:,:,3]
    average_r = np.mean(r[a>0])
    average_g = np.mean(g[a>0])
    average_b = np.mean(b[a>0])
    
    return (average_r , average_g , average_b)

def load_img_to_nparray(Img_path):
    return np.array(Image.open(Img_path).convert('RGBA'))

def mod_img(Img_Sample_Path, Img_Target_Path, ):#Img_Output_Path):

    
    Img_Sample_Pixels = load_img_to_nparray(Img_Sample_Path)
    Img_Target_Pixels = load_img_to_nparray(Img_Target_Path)

    Img_Sample_Pixels_avg = get_avg_rgb(Img_Sample_Pixels)
    Img_Target_Pixels_avg = get_avg_rgb(Img_Target_Pixels)
    
    difference_r, difference_g, difference_b= tuple(a - b for a, b in zip(Img_Sample_Pixels_avg, Img_Target_Pixels_avg))
    print(difference_r, difference_g, difference_b)
    Img_Output_Pixels = Img_Target_Pixels.copy()
    a =  Img_Target_Pixels[:,:,3]
    
    Img_Output_Pixels[a>0, 0] = np.clip(Img_Output_Pixels[a>0, 0].astype(np.float64) + difference_r, 0, 255).astype(np.uint8)
    Img_Output_Pixels[a>0, 1] = np.clip(Img_Output_Pixels[a>0, 1].astype(np.float64) + difference_g, 0, 255).astype(np.uint8)
    Img_Output_Pixels[a>0, 2] = np.clip(Img_Output_Pixels[a>0, 2].astype(np.float64) + difference_b, 0, 255).astype(np.uint8)

    # Ensure that the values remain in the valid range [0, 255]
    Img_Output_Pixels = np.clip(Img_Output_Pixels, 0, 255).astype(np.uint8)

    # Convert modified image data back to an image
    modified_image = Image.fromarray(Img_Output_Pixels, 'RGBA')
    return modified_image
    # Save or display the modified image
    # Img_Sample.show() 
    # Img_Target.show() 

    # modified_image.show() 
    # modified_image.save('modified_image.png')
    # plt.figure(figsize=(2, 2))
    # plt.imshow([[average_color]])
    # plt.axis('off')
    # plt.show()
    # print((average_r,average_g,average_b))

# mod_img(Img_Sample_Path,Img_Target_Path)
