def text_to_binary(filename):
    """
    Convert the text content of a file to a binary string.

    This function reads the contents of a file given by 'filename', converts
    each character of the text into its binary representation, and returns the
    result as a single string where each character's binary code is separated by
    a space.

    Parameters:
    filename (str): The path to the text file to be converted.

    Returns:
    str: A string containing the binary representation of the file's contents,
         or None if an error occurs during file reading.

    Raises:
    FileNotFoundError: If the file cannot be found at the specified path.
    Exception: For other issues that may arise during file reading.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        print("The file was not found. Please check the file path.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    binary_data = " ".join(format(ord(char), "08b") for char in text)

    # with open('output_binary.txt', 'w') as output_file:
    #     output_file.write(binary_data)

    return binary_data
