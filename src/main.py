from encoder import text_to_binary, create_png_from_binary, create_colored_png_from_binary

NAME = "assets/lorem.txt"
binary_content = text_to_binary(NAME)
FRANKENSTEIN = "assets/frankenstein.txt"
binary_frankenstein = text_to_binary(FRANKENSTEIN)
print(f"I should create {len(binary_frankenstein) // (1920*1080)} images with {len(binary_frankenstein) % (1920*1080)} leftover binary")
create_png_from_binary(binary_frankenstein, "frankenstein.png")
#create_colored_png_from_binary(binary_content, "grayscalelorem.png")