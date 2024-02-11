import numpy as np
from PIL import Image


def invert_colors(image):
    """
    Inverts the colors of black and white pixels in an image, leaving other colors unchanged.

    Args:
        image: The image to invert.

    Returns:
        The inverted image.
    """

    img = Image.open(image)
    data = np.array(img)

    for i in range(len(data)):
        for j in range(len(data[0])):
            # Check for black or white pixels using np.all() to handle multiple channels
            if np.all(data[i][j] == 0) or np.all(data[i][j] == 255):
                data[i][j] = 255 - data[i][j]

    new_img = Image.fromarray(data, 'RGB')
    return new_img


# Exemple d'utilisation.
image = "logo_horizontal.png"
new_image = invert_colors(image)
new_image.save("image_inverse.png")
