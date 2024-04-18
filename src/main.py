from encoder import text_to_binary, binary_to_png, create_png_from_binary

NAME = "assets/lorem.txt"
binary_content = text_to_binary(NAME)
# FRANKENSTEIN = "assets/frankenstein.txt"
# binary_frankenstein = text_to_binary(FRANKENSTEIN)
#binary_to_png(binary_content, "lorem.png", 20)
create_png_from_binary(binary_content, "loremnew.png")
