import os

def create_allowed_char_set():
    """Creates a set of allowed characters including Vietnamese, Latin, digits, and punctuation."""
    # Standard Latin alphabet (lower and upper)
    allowed_chars = "abcdefghijklmnopqrstuvwxyz"
    allowed_chars += allowed_chars.upper()

    # Digits
    allowed_chars += "0123456789"

    # Vietnamese characters (lower and upper) - comprehensive list
    vietnamese_chars = "áàảãạăắằẳẵặâấầẩẫậđéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ"
    allowed_chars += vietnamese_chars
    allowed_chars += vietnamese_chars.upper() # Add uppercase versions

    # Common punctuation, symbols, and whitespace - Adjust this list as needed!
    # Check your dataset for any other specific symbols you want to allow.
    allowed_chars += " .,;:!?'\"-()[]{}<>_/\\%&*+=#@\t\n\r"
    # Example: Add degree symbol if needed: allowed_chars += "°"

    # Create a set for efficient checking
    return set(allowed_chars)

def clean_vietnamese_file(input_filepath, output_filepath, allowed_set):
    """
    Reads a file, keeps lines where the text part contains only allowed characters
    (Vietnamese, Latin, digits, punctuation, whitespace).

    Args:
        input_filepath (str): Path to the input file.
        output_filepath (str): Path to the output file for cleaned lines.
        allowed_set (set): A set containing all allowed characters.
    """
    lines_read = 0
    lines_written = 0
    lines_removed = 0
    print(f"Processing file: {input_filepath}...")

    try:
        # Open files with UTF-8 encoding
        with open(input_filepath, 'r', encoding='utf-8') as infile, \
             open(output_filepath, 'w', encoding='utf-8') as outfile:

            for line in infile:
                lines_read += 1
                original_line = line # Keep the original line to write if valid
                line_to_check = line # Default: check the whole line

                # Check if the line structure is filepath<TAB>text
                parts = line.split('\t', 1)
                if len(parts) == 2:
                    # If tab exists, only check the text part after the first tab
                    line_to_check = parts[1]
                # If no tab, line_to_check remains the full line

                # Check characters in the relevant part of the line
                # We check against the line *without* trailing newline/CR for validation
                text_to_validate = line_to_check.rstrip('\n\r')

                is_valid = True
                offending_char = None
                for char in text_to_validate:
                    if char not in allowed_set:
                        is_valid = False
                        offending_char = char # Record the first invalid character found
                        break # No need to check further characters in this line

                if is_valid:
                    outfile.write(original_line) # Write the original, unmodified line
                    lines_written += 1
                else:
                    lines_removed += 1
                    # Optional: uncomment to print details about removed lines
                    # print(f"  Removed line {lines_read}: Invalid char '{offending_char}' in '{text_to_validate[:60]}...'")

        print(f"Finished processing {input_filepath}.")
        print(f"  Total lines read: {lines_read}")
        print(f"  Valid lines written: {lines_written} (containing only allowed chars)")
        print(f"  Invalid lines removed: {lines_removed}")
        print(f"  Cleaned file saved as: {output_filepath}\n")

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_filepath}")
    except IOError as e:
        print(f"Error reading/writing file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred processing {input_filepath}: {e}")

# --- Main Script ---
if __name__ == "__main__":
    # Create the set of allowed characters once
    allowed_characters = create_allowed_char_set()

    # List of files to process
    files_to_process = [
        'VIETOCR_DATASET_VAL.txt',
        'VIETOCR_DATASET_TRAIN.txt'
    ]

    # Directory where the files are located (assuming current directory)
    # Change this if your files are in a different folder
    file_directory = '.'

    for filename in files_to_process:
        input_path = os.path.join(file_directory, filename)

        if not os.path.exists(input_path):
            print(f"Warning: File '{filename}' not found in directory '{file_directory}'. Skipping.")
            continue

        # Construct the output filename with a descriptive suffix
        base, ext = os.path.splitext(filename)
        output_filename = f"{base}_vietnamese_only{ext}"
        output_path = os.path.join(file_directory, output_filename)

        # Clean the file based on allowed characters
        clean_vietnamese_file(input_path, output_path, allowed_characters)

    print("Script finished.")
