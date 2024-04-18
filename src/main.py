from encoder import text_to_binary, binary_to_png, create_png_from_binary

NAME = "assets/lorem.txt"
binary_content = text_to_binary(NAME)
FRANKENSTEIN = "assets/frankenstein.txt"
binary_frankenstein = text_to_binary(FRANKENSTEIN)
create_png_from_binary(binary_frankenstein, "frankenstein.png")
