from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

Img_Sample_Path = r'C:\Users\steve\Documents\safeco_color_modder\8 oz.png'
Img_Target_Path = r'C:\Users\steve\Documents\safeco_color_modder\IMG_2214_mod.png'

def get_avg_color(input_img):
    r, g, b, a = input_img[:,:,0], input_img[:,:,1], input_img[:,:,2], input_img[:,:,3]
    average_r = np.mean(r[a>0])
    average_g = np.mean(g[a>0])
    average_b = np.mean(b[a>0])
    
    return (average_r , average_g , average_b)

def mod_img(Img_Sample_Path, Img_Target_Path, ):#Img_Output_Path):
    Img_Sample = Image.open(Img_Sample_Path).convert('RGBA')
    Img_Target = Image.open(Img_Target_Path).convert('RGBA')
    
    Img_Sample_Pixels = np.array(Img_Sample)
    Img_Target_Pixels = np.array(Img_Target)
    Img_Sample_Pixels_avg = get_avg_color(Img_Sample_Pixels)
    Img_Target_Pixels_avg = get_avg_color(Img_Target_Pixels)
    
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

    # Save or display the modified image
    modified_image.show() 

    # plt.figure(figsize=(2, 2))
    # plt.imshow([[average_color]])
    # plt.axis('off')
    # plt.show()
    # print((average_r,average_g,average_b))

mod_img(Img_Sample_Path,Img_Target_Path)
