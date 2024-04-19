import cv2
import numpy as np


class Decoder:
    def __init__(self, video_filepath):
        self.video_filepath = video_filepath
        self.frames = []

    def process_video(self):
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
                # Convert frame to grayscale to simplify color detection
                cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                binary_data = self.convert_to_binary(frame)
                self.frames.append(binary_data)
                frame_count += 1
        finally:
            cap.release()

        print(
            f"Processed {frame_count} frames. Binary data captured selectively for each pixel."
        )

    def convert_to_binary(self, gray_frame):
        """
        Convert a grayscale frame to a binary representation where:
        - White is represented by 1 (pixel values near 255).
        - Black is represented by 0 (pixel values near 0).
        - Other colors (gray shades not close to black or white) are represented by -1 (ignored).

        Parameters:
        gray_frame (np.array): The grayscale frame to convert.

        Returns:
        np.array: A binary matrix representing the processed pixel colors.
        """
        binary_frame = np.array(dtype=int)
        binary_frame[gray_frame == 0] = 0
        binary_frame[gray_frame == 255] = 1
        return binary_frame

    def get_frame_binary_data(self, frame_index):
        """
        Retrieve the binary color data for a specific frame.

        Parameters:
        frame_index (int): The index of the frame for which to retrieve binary color data.

        Returns:
        np.array: A binary matrix for the specified frame, or None if the index is out of range.
        """
        if frame_index < len(self.frames):
            return self.frames[frame_index]
        else:
            print("Frame index out of range.")
            return None

    def binary_to_text(self):
        """
        Convert the stored binary data from all frames back into text, ignoring any '-1' values.
        Assumes each 8 bits (a row from the binary matrix) represents one ASCII character.
        """
        text_output = ""
        binary_block = ""
        for frame in self.frames:
            print(frame)
            for row in frame:
                binary_string = "".join(map(str, row))
                binary_block += binary_string
        text_chars = [binary_block[i : i + 8] for i in range(0, len(binary_block), 8)]
        for char in text_chars:
            if len(char) == 8:
                text_output += chr(int(char, 2))
        return text_output


try:
    decoder = Decoder("results/vids/frankenstein.mp4")
    decoder.process_video()
    extracted_text = decoder.binary_to_text()
    print("Extracted Text:", extracted_text)
except Exception as e:
    print(f"An error occurred: {e}")
