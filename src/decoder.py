import cv2
import numpy as np


class Decoder:
    def __init__(self, video_filepath):
        self.video_filepath = video_filepath
        self.frames_converted = []

    def process_video(self, pixel_size):
        """
        Process the video by extracting each frame and selectively converting pixel colors
        to binary data based on their black or white status.

        Parameters:
        pixel_size (int): the block size representing each 3 bit encoding in the provided video
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
                self.frames_converted.append(self.convert_to_color(frame, pixel_size))
                frame_count += 1
        finally:
            cap.release()

        print(
            f"Processed {frame_count} frames. Binary data captured selectively for each pixel.", end='\n\n')

    def convert_to_color(self, frame, pixel_size):
        """
        Convert a frame to a 3-bit representation where:
        - White: 111
        - Black: 000
        - Red : 001
        - Green : 010
        - Blue : 100
        - Yellow : 110
        - Cyan : 101
        - Magenta : 011

        Parameters:
        frame (np.array): The frame to convert.
        pixel_size (int): The size of the block representing a pixel.
        ignore_threshold (int): The threshold for ignoring colors that are too close to the 'none' color.

        Returns:
        binary_frame: A 3-bit array representing the processed pixel values.
        """
        num_blocks_y = frame.shape[0] // pixel_size
        num_blocks_x = frame.shape[1] // pixel_size

        binary_frame = np.full((num_blocks_y, num_blocks_x, 3), -1, dtype=int)
        offset = pixel_size // 2

        # Color thresholds
        color_thresholds = {
            "black": np.array([0, 0, 0]),
            "white": np.array([255, 255, 255]),
            "red": np.array([0, 0, 255]),
            "green": np.array([0, 255, 0]),
            "blue": np.array([255, 0, 0]),
            "yellow": np.array([0, 255, 255]),
            "cyan": np.array([255, 255, 0]),
            "magenta": np.array([255, 0, 255]),
            "none": np.array([127, 127, 127]),
        }

        # 3-bit representations
        color_representations = {
            "black": [0, 0, 0],
            "white": [1, 1, 1],
            "red": [1, 0, 0],
            "green": [0, 1, 0],
            "blue": [0, 0, 1],
            "yellow": [1, 1, 0],
            "cyan": [0, 1, 1],
            "magenta": [1, 0, 1],
        }
        counter = 0
        for idx1 in range(num_blocks_y):
            for idx2 in range(num_blocks_x):
                center_pixel = frame[idx1 * pixel_size + offset][
                    idx2 * pixel_size + offset
                ]
                closest_color = min(
                    color_thresholds,
                    key=lambda x: np.linalg.norm(center_pixel - color_thresholds[x]),
                )
                if closest_color == "none":
                    closest_color = "black"
                    counter += 1
                binary_frame[idx1, idx2] = color_representations[closest_color]

        print(f"I was uncertain about {counter} characters")
        return binary_frame

    def binary_to_text(self):
        """
        Convert the stored binary data from all frames back into text.
        Assumes each 8 bits (a row from the binary matrix) represents one ASCII character.
        """
        text_output = ""
        binary_chunk = ""
        for frame in self.frames_converted:
            for row in frame:
                filtered_row = row.flatten()
                binary_string = "".join(str(bit) for bit in filtered_row if bit != -1)
                binary_chunk += binary_string
        binary_chunk = binary_chunk[:-2]
        print("Binary Chunk Length: ", len(binary_chunk))
        # Convert each 8 bits to an ASCII character
        text_chars = [binary_chunk[i : i + 8] for i in range(0, len(binary_chunk), 8)]
        for char in text_chars:
            if len(char) == 8:
                text_output += chr(int(char, 2))
        return text_output
