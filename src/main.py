from encoder import Encoder
import os

frankenstein = Encoder("assets/frankenstein.txt")
frankenstein.generate_video("frankenstein", frame_rate=5, BLOCK_SIZE=3)

# file = str(input("Enter the name of the text file (excluding the file extension) you want to turn into a video:"))
# encoder = Encoder(f"assets/{file}.txt")
# encoder.generate_video(file, 1, 120)
