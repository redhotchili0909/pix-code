from PIL import Image as img

IMG_WIDTH = 10
IMG_HEIGHT = 3
img_index = 0
COLOR_MAP = {
        "0": (0, 0, 0),   # Black
        "1": (255, 255, 255)  # White
    }

def text_to_binary(filename):
    """
    Convert the text content of a file to a binary string.

    This function reads the contents of a file given by 'filename', converts
    each character of the text into its binary representation, and returns the
    result as a single string where each character's binary code is separated by
    a space.

    Parameters:
    filename (str): The path to the text file to be converted.

    Returns:
    str: A string containing the binary representation of the file's contents,
         or None if an error occurs during file reading.

    Raises:
    FileNotFoundError: If the file cannot be found at the specified path.
    Exception: For other issues that may arise during file reading.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        print("The file was not found. Please check the file path.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    binary_data = "".join(format(ord(char), "08b") for char in text)

    filename = filename.split("/")[-1].split(".")[0]
    with open(f"results/binary/{filename}_binary.txt", "w") as output_file:
        output_file.write(binary_data)

    return binary_data


def binary_to_png(binary_data, output_filename, image_width):
    """
    Convert binary data to a PNG image file.

    This function takes a string of binary data, converts it into pixel values,
    and saves it as a PNG image. Each byte (8 bits) in the binary data is treated
    as one pixel in a grayscale image.

    Parameters:
    binary_data (str): A string of binary data separated by spaces.
    output_filename (str): Filename for the output PNG image.
    image_width (int): The width of the image in pixels.

    """
    pixel_data = [int(b, 2) for b in binary_data.split()]

    image_height = len(pixel_data) // image_width
    if len(pixel_data) % image_width != 0:
        image_height += 1

    image = img.new("L", (image_width, image_height))
    image.putdata(pixel_data)

    image.save(f"results/image/{output_filename}", "PNG")


def create_png_from_binary(binary_data, output_file, img_index=0):

    # Create a new image with the specified width and height
    im = img.new(mode = 'RGB', size = (IMG_WIDTH, IMG_HEIGHT), color = (207, 255, 4))
    data_end = False
    # Iterate through each tile and set pixel values based on the color map
    counter = 0
    #print(binary_data[:IMG_HEIGHT*IMG_WIDTH])
    for y in range(IMG_HEIGHT):
        for x in range(IMG_WIDTH):
            counter += 1
            try:
                im.putpixel((x,y), COLOR_MAP[binary_data[IMG_WIDTH*y + x]])
                #print(f"I just printed a {COLOR_MAP[binary_data[IMG_WIDTH*y + x]]} tile on {x,y} and my num is {binary_data[IMG_WIDTH*y + x]}")
            except IndexError:
                print(f"I've finished. My x is {x} and my y is {y}")
                data_end = True
                break
        if data_end:
            break

    # Save the image as a PNG file
    im.save(f"results/image/{img_index}{output_file}", "PNG")
    if len(binary_data) > IMG_HEIGHT*IMG_WIDTH:
        print(f"I didn't finish my data and I'm on {img_index}")
        img_index += 1
        create_png_from_binary(binary_data[:IMG_HEIGHT*IMG_WIDTH], output_file, img_index)
