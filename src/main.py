# from encoder import text_to_binary, create_png_from_binary, create_colored_png_from_binary
import os
from PIL import Image, ImageDraw
# NAME = "assets/lorem.txt"
# binary_content = text_to_binary(NAME)
# FRANKENSTEIN = "assets/frankenstein.txt"
# binary_frankenstein = text_to_binary(FRANKENSTEIN)
# print(f"I should create {len(binary_frankenstein) // (1920*1080)} images with {len(binary_frankenstein) % (1920*1080)} leftover binary")
# create_png_from_binary(binary_frankenstein, "frankenstein.png")
#create_colored_png_from_binary(binary_content, "grayscalelorem.png")
from encoder import Encoder

wb = "111110000011111000001111100000111110000001111100000"

bw = "00000111110000011111000001111100000111110000011111"
actual_wb = "0101011"
image_encoder = Encoder(binary_data = actual_wb, img_height = 100, img_width = 50)
image_encoder.create_png_from_binary("largerpixels", 25)


    
