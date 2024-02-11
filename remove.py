
from PIL import Image, ImageDraw, ImageFont
from rembg import remove

def remove_background(image):    

    input = Image.open(image)

    output = remove(input)

    bbox = output.getbbox()

    cropped_image = output.crop(bbox)

    cropped_image.save("cropped_image.png")

    return cropped_image



    
