from encoder import Encoder
import os

# frankenstein = Encoder("assets/frankenstein.txt")
# frankenstein.generate_video("frankenstein", 5, 5)

# hello = Encoder("assets/hello.txt")
# hello.generate_video("hello", 1, 120)

# manual_hello = Encoder(binary_data="0110100001100101011011000110110001101111")
# manual_hello.generate_video("manual_hello", 1, 120)

manual_test = Encoder(binary_data="011010")
manual_test.generate_video("manual_test", 1, 120)
