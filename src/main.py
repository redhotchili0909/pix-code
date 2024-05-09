from pix_code_encoder import Encoder
from pix_code_decoder import Decoder
from video_pipeline import *
from time import sleep

PRINT_LINE_WIDTH = 40
print("Select Next Actions: ")
print("1. Encode/Generate Video")
print("2. Decode Video")
print("3. Quit")
print("-" * PRINT_LINE_WIDTH)
encoded_text = input()

match encoded_text:
    case "1":
        print("Enter a text-file to encode: ")
        print("-" * PRINT_LINE_WIDTH)
        filename = input()
        print("Enter frame rate & pixel size \nEx. 1,5")
        print("-" * PRINT_LINE_WIDTH)
        frame_rate, block_size = input().split(",")
        encoder_instance = Encoder(f"assets/{filename}.txt")
        encoder_instance.generate_video(
            output_folder=filename, 
            frame_rate=int(frame_rate), 
            BLOCK_SIZE=int(block_size)
            )
    case "2":
        print("-" * PRINT_LINE_WIDTH)
        print("Enter video title & pixel size: ")
        print("Ex. bee,5")
        filename, block_size = input().split(",")
        decoder = Decoder(video_filepath=f"results/vids/{filename}.mp4")
        text = decoder.binary_to_text(int(block_size))
        print("Output: ")
        print(text)
        quit()
    case "3":
        print("-" * PRINT_LINE_WIDTH)
        print("Quitting...")
        quit()
    case _:
        print("Invalid input")
        quit()

print("-" * PRINT_LINE_WIDTH)
print("Would you like to upload the video to YouTube? (Y/N): ")
upload = input()
YOUTUBE = True

match upload:
    case "Y":
        print("-" * PRINT_LINE_WIDTH)
        print("Uploading video to YouTube...")
        try:
            youtube = get_authenticated_service()
        except Exception as e:
            # Handle any other exceptions
            print("An error occurred:", e)
            print("YouTube upload unsuccessful. Please add your credentials file into" +  
                  "the pix-code directory, as outlined in the README")
            YOUTUBE = False
        
        if YOUTUBE:
            print(YOUTUBE)
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
        YOUTUBE = False
    case _:
        print("Invalid input")
        quit()

if YOUTUBE:
    print("-" * PRINT_LINE_WIDTH)
    print("Please provide a link to the video: ")
    link = input()
    print("Downloading video from YouTube...")
    sleep(5)
    download_video(f"{link}")

print("-" * PRINT_LINE_WIDTH)
print("Would you like to decode the video to text? (Y/N) (This may take a while if your file is long): ")
decoding = input()

match decoding:
    case "Y":
        print("-" * PRINT_LINE_WIDTH)
        decoder = Decoder(video_filepath=f"results/vids/{filename}.mp4")
        text = decoder.binary_to_text(int(block_size))
        print("\n")
        print("Output:\n", text)
    case "N":
        print("-" * PRINT_LINE_WIDTH)
        print("Quitting...")
        quit()
    case _:
        print("Invalid input")
        quit()

if encoded_text == "2":
    print("-" * PRINT_LINE_WIDTH)
    print("Do you want to save this all to a text file? (Y/N)")
    save_text = input()
    match save_text:
        case "Y":
            print("What do you want the text file to be named?")
            filename = input()
            text_file = open(f"{filename}.txt", "w")
            text_file.write(text)
            text_file.close()
        case "N":
            print("Quitting...")
            quit()
        case _:
            print("Invalid input")
            quit()
        