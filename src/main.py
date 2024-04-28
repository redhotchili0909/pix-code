from encoder import Encoder
import os

frankenstein = Encoder("assets/frankenstein.txt")
frankenstein.create_pngs_from_binary("frankenstein", 5)
frankenstein.generate_video("frankenstein", 5, 5)
