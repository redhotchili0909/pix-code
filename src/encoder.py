from PIL import Image as img

IMG_WIDTH = 1920
IMG_HEIGHT = 1080
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


def create_png_from_binary(binary_data, output_file, img_index=0):
    """
    Convert binary data to a PNG image file.

    This function takes a string of binary data, converts it into pixel values,
    and saves it into PNG images of a given size until it runs out of data. Each 
    bit in the binary data is treated as one pixel in a black and white image.

    Parameters:
    binary_data (str): A string of binary data separated by spaces.
    output_filename (str): Filename for the output PNG image.
    img_index (int) : An integer index for the PNG

    """

    # Create a new image with the specified width and height
    im = img.new(mode = 'RGB', size = (IMG_WIDTH, IMG_HEIGHT), color = (74,65,42))
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
                print(f"I've finished. My x is {x} and my y is {y} and the counter is {counter}")
                data_end = True
                break
        if data_end:
            break

    # Save the image as a PNG file
    im.save(f"results/image/{img_index}{output_file}", "PNG")
    if len(binary_data) > IMG_HEIGHT*IMG_WIDTH:
        print(f"creating {output_file}{img_index} ...")
        create_png_from_binary(binary_data[IMG_HEIGHT*IMG_WIDTH:], output_file, img_index + 1)

    # remaining_data = binary_data[IMG_HEIGHT*IMG_WIDTH:]
    # if remaining_data:
    #     print(f"creating {output_file}{img_index} ...")
    #     create_png_from_binary(remaining_data, output_file, img_index + 1)


def create_colored_png_from_binary(binary_data, output_file, img_index=0):
    """
    Convert binary data to a PNG image file.

    This function takes a string of binary data, converts it into pixel values,
    and saves it into PNG images of a given size until it runs out of data. Each 
    byte in the binary data is treated as one pixel in a black and white image.

    Parameters:
    binary_data (str): A string of binary data separated by spaces.
    output_filename (str): Filename for the output PNG image.
    img_index (int) : An integer index for the PNG
    """

    # Define constants
    BYTE_SIZE = 8  # Number of bits in a byte

    # Calculate the number of bytes needed for one image
    bytes_per_image = IMG_HEIGHT * IMG_WIDTH // BYTE_SIZE

    # Create a new image with the specified width and height
    im = img.new(mode='RGB', size=(IMG_WIDTH, IMG_HEIGHT), color=(74, 65, 42))

    # Iterate through each byte of binary data
    for byte_index in range(bytes_per_image):
        # Calculate the start and end index for this byte in the binary data
        start_index = byte_index * BYTE_SIZE
        end_index = (byte_index + 1) * BYTE_SIZE

        # Extract one byte from the binary data
        byte = binary_data[start_index:end_index]

        # Convert the byte to an integer value
        pixel_value = int(byte, 2)

        # Calculate the pixel coordinates
        y = byte_index // IMG_WIDTH
        x = byte_index % IMG_WIDTH

        # Set the pixel value in the image
        im.putpixel((x, y), (255-pixel_value, pixel_value, pixel_value))

    # Save the image as a PNG file
    im.save(f"results/image/{img_index}_{output_file}", "PNG")

    # If there is more binary data remaining, recursively call the function for the next image
    remaining_data = binary_data[bytes_per_image * BYTE_SIZE:]
    if remaining_data:
        create_colored_png_from_binary(remaining_data, output_file, img_index + 1)

