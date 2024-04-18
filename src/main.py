from encoder import Encoder

bee = Encoder("assets/bee.txt")
bee.create_png_from_binary("bee")
bee.generate_video("bee", 1)
