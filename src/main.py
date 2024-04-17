from encoder import text_to_binary, binary_to_png

NAME = "assets/lorem.txt"
binary_content = text_to_binary(NAME)

binary_to_png(binary_content, "lorem.png", 20)
