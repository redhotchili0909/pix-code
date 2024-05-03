from pix_code_encoder import Encoder
from pix_code_decoder import Decoder
from video_pipeline import *
from time import sleep

print("Select Next Actions: ")
print("1. Encode/Generate Video")
print("2. Decode Video")
print("3. Quit")
print("-" * 20)
encoded_text = input()


match encoded_text:
    case "1":
        print("Enter a text-file to encode: ")
        filename = input()
        text_file = Encoder(f"assets/{filename}.txt")
        print("-" * 20)
        print("Enter frame rate: & pixel size: ")
        print("Ex. 1,5")
        print("-" * 20)
        frame_rate, pixel_size = input().split(",")
        print("-" * 20)
        text_file.generate_video(filename, int(frame_rate), int(pixel_size))
    case "2":
        print("-" * 20)
        print("Enter video title & pixel size: ")
        print("Ex. bee,5")
        filename, pixel_size = input().split(",")
        decoder = Decoder(video_filepath=f"results/vids/{filename}.mp4")
        text = decoder.binary_to_text(int(pixel_size))
        print("Output: ")
        print(text)
        quit()
    case "3":
        print("-" * 20)
        print("Quitting...")
        quit()
    case _:
        print("Invalid input")
        quit()

print("-" * 20)
print("Would you like to upload the video to YouTube?(Y/N): ")
upload = input()

match upload:
    case "Y":
        print("-" * 20)
        print("Uploading video to YouTube...")
        youtube = get_authenticated_service()
        file_path = f"results/vids/{filename}.mp4"
        title = f"pix-code-color-{filename}"
        description = "Testing for pix-code color video upload"
        category_id = "22"
        keywords = ["storage", "encryption"]
        privacy_status = "unlisted"

        upload_response = upload_video(
            youtube,
            file_path,
            title,
            description,
            category_id,
            keywords,
            privacy_status,
        )
        print("Uploaded video with ID:", upload_response["id"])
    case "N":
        print("-" * 20)
        print("Quitting...")
        quit()
    case _:
        print("Invalid input")
        quit()

print("-" * 20)
print("Please provide a link to the video: ")
link = input()
print("Downloading video from YouTube...")
sleep(5)
download_video(f"{link}")

print("-" * 20)
print("Would you like to decode the video to text?(Y/N): ")
decoding = input()

match decoding:
    case "Y":
        print("-" * 20)
        decoder = Decoder(video_filepath=f"results/vids/{filename}.mp4")
        text = decoder.binary_to_text(int(pixel_size))
        print("Output: ", text)
    case "N":
        print("-" * 20)
        print("Quitting...")
        quit()
    case _:
        print("Invalid input")
        quit()
