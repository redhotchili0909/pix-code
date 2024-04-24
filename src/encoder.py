import os
from PIL import Image, ImageDraw
import cv2


class Encoder:
    def __init__(self, binary_data=None, img_width=1920, img_height=1080):
        self.color_map = {
            "0": (0, 0, 0),
            "1": (255, 255, 255),
        }  # Black for '0', White for '1'
        self.img_width = img_width
        self.img_height = img_height
        self.binary_data = binary_data
        if self.binary_data is None:
            self.text_to_binary()

    def text_to_binary(self, filepath):
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
            with open(filepath, "r", encoding="utf-8") as file:
                text = file.read()
            self.binary_data = "".join(format(ord(char), "08b") for char in text)
        except FileNotFoundError:
            print("The file was not found. Please check the file path.")
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    def create_png_from_binary(self, output_folder, BLOCK_SIZE):
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
        

        img_index = 0
        directory = f"results/imgs/{output_folder}"
        os.makedirs(directory, exist_ok=True)
        img_bit_width = self.img_width//BLOCK_SIZE
        img_bit_height = self.img_height//BLOCK_SIZE

        img = Image.new(mode = 'RGB', size = (self.img_width, self.img_height), color = (74,65,42))

        drawable_img = ImageDraw.Draw(img)

        for y in range(img_bit_height):
            for x in range(img_bit_width):
                if y * img_bit_width + x >= len(self.binary_data):
                    img.save(f"{directory}/{img_index}.png", "PNG")
                    return
                drawable_img.rectangle([(x*BLOCK_SIZE, y*BLOCK_SIZE), 
                                        (x*BLOCK_SIZE + BLOCK_SIZE, y*BLOCK_SIZE + BLOCK_SIZE)], 
                                        fill=self.color_map[self.binary_data[y * img_bit_width + x]])
        img.save(f"{directory}/{img_index}.png", "PNG")
        img_index += 1
        self.binary_data = self.binary_data[img_bit_width * img_bit_height :]
    

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
        output_video_path = f"results/vids/{directory}.avi"
        fourcc = cv2.VideoWriter_fourcc(*"ffv1")
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
