import cv2
import numpy as np


class Decoder:
    def __init__(self, video_filepath):
        self.video_filepath = video_filepath
        self.frames = []

    def process_video(self, pixel_size):
        """
        Process the video by extracting each frame and selectively converting pixel colors
        to binary data based on their black or white status.
        """
        # Open the video file
        cap = cv2.VideoCapture(self.video_filepath)
        if not cap.isOpened():
            raise ValueError("Error opening video file.")

        frame_count = 0
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                converted = self.convert_to_binary(frame, pixel_size)
                self.frames.append(converted)
                frame_count += 1
                return converted
        finally:
            cap.release()

        print(
            f"Processed {frame_count} frames. Binary data captured selectively for each pixel."
        )

    def convert_to_binary(self, frame, pixel_size):
        """
        Convert a frame to a binary representation where:
        - White is represented by 1 (pixel values near 255).
        - Black is represented by 0 (pixel values near 0).
        - Other colors are ignored and set to -1.

        Parameters:
        frame (np.array): The frame to convert.
        pixel_size (int): The size of the block representing a pixel.

        Returns:
        binary_frame: A binary array representing the processed pixel values.
        """
        num_blocks = frame.shape[0] // pixel_size

        binary_frame = np.full((num_blocks, num_blocks), -1, dtype=int)
        offset = pixel_size // 2

        for idx1 in range(num_blocks):
            for idx2 in range(num_blocks):
                center_pixel = frame[idx1 * pixel_size + offset][
                    idx2 * pixel_size + offset
                ]
                _, binary_pixel = cv2.threshold(
                    center_pixel, 127, 255, cv2.THRESH_BINARY
                )
                binary_frame[idx1, idx2] = 1 if np.mean(binary_pixel) == 255 else 0
        return binary_frame

    def convert_to_color(self, frame, pixel_size):
        """
        Convert a frame to a 3-bit representation where:
        - White: 111
        - Black: 000
        - Red : 001
        - Green : 010
        - Blue : 100
        - Yellow : 011
        - Cyan : 101
        - Magenta : 110
        - Other colors are ignored and set to -1-1-1.

        Parameters:
        frame (np.array): The frame to convert.
        pixel_size (int): The size of the block representing a pixel.

        Returns:
        binary_frame: A 3-bit array representing the processed pixel values.
        """
        num_blocks = frame.shape[0] // pixel_size

        # Prepare the binary frame with a shape to accommodate 3-bit color representations
        binary_frame = np.full((num_blocks, num_blocks, 3), -1, dtype=int)
        offset = pixel_size // 2

        # Color thresholds
        color_thresholds = {
            'black': np.array([0, 0, 0]),
            'white': np.array([255, 255, 255]),
            'red': np.array([0, 0, 255]),
            'green': np.array([0, 255, 0]),
            'blue': np.array([255, 0, 0]),
            'yellow': np.array([0, 255, 255]),
            'cyan': np.array([255, 255, 0]),
            'magenta': np.array([255, 0, 255])
        }

        # 3-bit representations
        color_representations = {
            'black': [0, 0, 0],
            'white': [1, 1, 1],
            'red': [0, 0, 1],
            'green': [0, 1, 0],
            'blue': [1, 0, 0],
            'yellow': [0, 1, 1],
            'cyan': [1, 1, 0],
            'magenta': [1, 0, 1]
        }

        for idx1 in range(num_blocks):
            for idx2 in range(num_blocks):
                center_pixel = frame[idx1 * pixel_size + offset][idx2 * pixel_size + offset]
                closest_color = min(color_thresholds, key=lambda x: np.linalg.norm(center_pixel - color_thresholds[x]))
                binary_frame[idx1, idx2] = color_representations[closest_color]

        return binary_frame

    def binary_to_text(self):
        """
        Convert the stored binary data from all frames back into text, ignoring any '-1' values.
        Assumes each 8 bits (a row from the binary matrix) represents one ASCII character.
        """
        text_output = ""
        for frame in self.frames:
            for row in frame:
                filtered_row = row[row != -1]
                binary_string = "".join(map(str, filtered_row))
                text_chars = [
                    binary_string[i : i + 8] for i in range(0, len(binary_string), 8)
                ]
                for char in text_chars:
                    if len(char) == 8:
                        text_output += chr(int(char, 2))
        return text_output


try:
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
                checkerboard[y : y + pix_size, x : x + pix_size] = (
                    255  # Fill with 255 (white squares)
                )
    decoder = Decoder("results/vids/test_1920x1080_15x15.mp4")
    converted = decoder.process_video(15)
    print((checkerboard == converted).all())
except Exception as e:
    print(f"An error occurred: {e}")
