from PIL import Image as img


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

    binary_data = " ".join(format(ord(char), "08b") for char in text)

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
