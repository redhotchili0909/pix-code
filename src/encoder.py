import os
from PIL import Image
import cv2


class Encoder:
    def __init__(self, filepath):
        self.filepath = filepath
        self.img_width = 1920
        self.img_height = 1080
        self.color_map = {
            "0": (0, 0, 0),
            "1": (255, 255, 255),
        }  # Black for '0', White for '1'
        self.binary_data = None
        self.text_to_binary()

    def text_to_binary(self):
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
            with open(self.filepath, "r", encoding="utf-8") as file:
                text = file.read()
            self.binary_data = "".join(format(ord(char), "08b") for char in text)
        except FileNotFoundError:
            print("The file was not found. Please check the file path.")
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    def create_png_from_binary(self, output_folder):
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
        if self.binary_data is None:
            raise ValueError("Binary data is not generated yet.")

        binary_data = self.binary_data
        img_index = 0
        directory = f"results/imgs/{output_folder}"
        os.makedirs(directory, exist_ok=True)

        while binary_data:
            img = Image.new("RGB", (self.img_width, self.img_height), (74, 65, 42))
            for y in range(self.img_height):
                for x in range(self.img_width):
                    if y * self.img_width + x >= len(binary_data):
                        img.save(f"{directory}/{img_index}.png", "PNG")
                        return
                    img.putpixel(
                        (x, y), self.color_map[binary_data[y * self.img_width + x]]
                    )
            img.save(f"{directory}/{img_index}.png", "PNG")
            img_index += 1
            binary_data = binary_data[self.img_width * self.img_height :]

    def generate_video(self, directory, frame_rate):
        """
        Generate a video from a sequence of PNG images stored in a specified directory.

        This function reads a specified number of PNG images from a directory,
        and compiles them into a single video file with a specified frame rate.
        The output video is saved in the 'results/vids/' directory.
        It handles image reading failures by stopping the video creation
        if an image file cannot be loaded.

        Parameters:
        num_images (int): The number of images to include in the video.
        directory (str): The directory path where the PNG images are stored.
        frame_rate (float): The frame rate of the output video in frames per second.

        Raises:
        FileNotFoundError: If the specified directory does not contain the images.
        Exception: For issues that may arise during video file creation.
        """
        output_video_path = f"results/vids/{directory}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        first_image_path = f"results/imgs/{directory}/0.png"
        frame = cv2.imread(first_image_path)

        if frame is None:
            raise FileNotFoundError(
                "The first image could not be loaded. Ensure the directory contains the images."
            )

        video = cv2.VideoWriter(
            output_video_path, fourcc, frame_rate, (frame.shape[1], frame.shape[0])
        )

        img_index = 0
        while True:
            img_path = f"results/imgs/{directory}/{img_index}.png"
            frame = cv2.imread(img_path)
            if frame is None:
                break
            video.write(frame)
            img_index += 1

        video.release()
        print(f"Video of {directory} created successfully.")

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

