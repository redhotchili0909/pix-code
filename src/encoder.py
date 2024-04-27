import os
from PIL import Image, ImageDraw
import cv2


class Encoder:
    def __init__(self, filepath=None, binary_data=None, img_width=1920, img_height=1080):
        self.color_map = {
            "0": (0, 0, 0),
            "1": (255, 255, 255),
        }  # Black for '0', White for '1'
        self.color_thresholds = {
            '000': (0, 0, 0),
            '111': (255, 255, 255),
            '001': (0, 0, 255),
            '010': (0, 255, 0),
            '100': (255, 0, 0),
            '011': (0, 255, 255),
            '101': (255, 255, 0),
            '110': (255, 0, 255)
        }
        self.img_width = img_width
        self.img_height = img_height
        self.binary_data = binary_data
        self.filepath = filepath
        if self.binary_data is None and self.filepath is not None:
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

    def create_pngs_from_binary(self, output_folder, BLOCK_SIZE, img_index=0, COLOR=True):
        CHUNK_SIZE = 1 if not COLOR else 3
        (print("Creating colored image data...") 
         if COLOR else 
         print("Creating black and white image data..."))
        def process_image(current_data, img_index):
            directory = f"results/imgs/{output_folder}"
            os.makedirs(directory, exist_ok=True)
            img_bit_width = self.img_width // BLOCK_SIZE
            img_bit_height = self.img_height // BLOCK_SIZE

            img = Image.new(mode='RGB', size=(self.img_width, self.img_height), color=(74, 65, 42))
            drawable_img = ImageDraw.Draw(img)

            split_binary_chunks = []
            for i in range(
                CHUNK_SIZE, 
                len(current_data) + CHUNK_SIZE, CHUNK_SIZE
                ):
                encoding = current_data[i-CHUNK_SIZE:i]
                while len(encoding) < CHUNK_SIZE:
                    encoding += "0"
                split_binary_chunks.append(encoding)

            for y in range(img_bit_height):
                for x in range(img_bit_width):
                    chunk_index = y * img_bit_width + x
                    if chunk_index >= len(split_binary_chunks):
                        print(f"Now saving image {directory}/{img_index}.png\n")
                        img.save(f"{directory}/{img_index}.png", "PNG")
                        return
                    # print(f"Placing {split_binary_chunks[y * img_bit_width + x]} block " +
                    #       f"at {(x*BLOCK_SIZE, y*BLOCK_SIZE)}, " + 
                    #       f"{(x*BLOCK_SIZE + BLOCK_SIZE - 1, y*BLOCK_SIZE + BLOCK_SIZE - 1)}")
                    fill = (
                        self.color_thresholds[split_binary_chunks[chunk_index]]
                        if COLOR else
                        self.color_map[current_data[y * img_bit_width + x]]
                    )
                    drawable_img.rectangle([(x*BLOCK_SIZE, y*BLOCK_SIZE),
                                            (x*BLOCK_SIZE + BLOCK_SIZE - 1, 
                                             y*BLOCK_SIZE + BLOCK_SIZE - 1)],
                                            fill=fill)
            print(f"Now saving image {directory}/{img_index}.png")
            img.save(f"{directory}/{img_index}.png", "PNG")
            
            binary_per_image = img_bit_height * img_bit_width * CHUNK_SIZE
            if len(current_data) > binary_per_image:
                next_data = current_data[binary_per_image:]
                process_image(next_data, img_index + 1)

        # Call the inner function with the initial binary data
        if self.binary_data is None:
            raise ValueError("Binary data is not generated yet.")
        process_image(self.binary_data, img_index)

    def generate_video(self, output_folder, frame_rate, BLOCK_SIZE, COLOR=True):
        """
        Generate a video from a sequence of PNG images stored in a specified directory.

        This function reads a specified number of PNG images from a directory,
        and compiles them into a single video file with a specified frame rate.
        The output video is saved in the 'results/vids/' directory.
        It handles image reading failures by stopping the video creation
        if an image file cannot be loaded.

        Parameters:
        num_images (int): The number of images to include in the video.
        output_folder (str): The directory path where the PNG images are stored.
        frame_rate (float): The frame rate of the output video in frames per second.
        BLOCK_SIZE (int): The size of the blocks where bits of binary data are stored

        Raises:
        FileNotFoundError: If the specified directory does not contain the images.
        Exception: For issues that may arise during video file creation.
        """
        path = f"results/imgs/{output_folder}"
        if not os.path.exists(path) or not os.path.isdir(path):
            self.create_pngs_from_binary(output_folder, BLOCK_SIZE, COLOR=COLOR)
        output_video_path = f"results/vids/{output_folder}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        first_image_path = path + "/0.png"
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
            img_path = path + f"/{img_index}.png"
            frame = cv2.imread(img_path)
            if frame is None:
                break
            video.write(frame)
            img_index += 1

        video.release()
        print(f"Video of {output_folder} created successfully.")
