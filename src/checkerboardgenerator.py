from PIL import Image
import numpy as np

# Dimensions of the final image
width, height = 1920, 1080

# Size of each square in the checkerboard pattern
pix_size = 5

# Create an empty array for the image data
# numpy.zeros() creates an array filled with zeros (black squares)
checkerboard = np.zeros((height, width), dtype=np.uint8)

# Fill the array to create the checkerboard pattern
for y in range(0, height, pix_size):
    for x in range(0, width, pix_size):
        if (x // pix_size + y // pix_size) % 2 == 0:
            checkerboard[y:y+pix_size, x:x+pix_size] = 255  # Fill with 255 (white squares)

# Create an image from the array
image = Image.fromarray(checkerboard, 'L')  # 'L' mode for grayscale

# Save the image to a PNG file
image_path = f"assets/checkerboard_1920x1080_{pix_size}x{pix_size}.png"
image.save(image_path)

image_path