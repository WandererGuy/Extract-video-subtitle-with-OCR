import os

def keep_first_n_lines(input_filepath, output_filepath, n):
    """
    Reads an input file and writes the first n lines to an output file.

    Args:
        input_filepath (str): Path to the input file.
        output_filepath (str): Path to the output file.
        n (int): The number of lines to keep from the beginning of the input file.
    """
    lines_written = 0
    print(f"Processing file: {input_filepath}...")
    print(f"Keeping the first {n} lines.")

    try:
        # Open files with UTF-8 encoding, suitable for text files like yours
        with open(input_filepath, 'r', encoding='utf-8') as infile, \
             open(output_filepath, 'w', encoding='utf-8') as outfile:

            # Read lines one by one
            for line in infile:
                # Check if we have already written n lines
                if lines_written >= n:
                    break  # Stop processing if we've reached the limit

                # Write the current line to the output file
                outfile.write(line)
                lines_written += 1

        print(f"Finished processing.")
        # Check if fewer lines were found than requested
        if lines_written < n:
            print(f"  Note: Input file had only {lines_written} lines, which is less than the requested {n}.")
        else:
            print(f"  Successfully wrote {lines_written} lines.")
        print(f"  Output saved to: {output_filepath}\n")

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_filepath}")
    except ValueError:
        print(f"Error: Invalid number specified for lines to keep (n={n}). Please provide a positive integer.")
    except IOError as e:
        print(f"Error reading/writing file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Main Script ---
if __name__ == "__main__":
    # --- Configuration ---
    input_filename = 'VIETOCR_DATASET_VAL.txt'
    # You can change the number of lines here
    num_lines_to_keep = 1800
    # Construct the output filename dynamically
    base, ext = os.path.splitext(input_filename)
    output_filename = f"{base}_first_{num_lines_to_keep}{ext}"
    # Directory where the files are located (assuming current directory)
    file_directory = '.'
    # --- End Configuration ---

    input_path = os.path.join(file_directory, input_filename)
    output_path = os.path.join(file_directory, output_filename)

    # Validate n before proceeding
    if not isinstance(num_lines_to_keep, int) or num_lines_to_keep <= 0:
        print(f"Error: Number of lines to keep ({num_lines_to_keep}) must be a positive integer.")
    elif not os.path.exists(input_path):
         print(f"Error: Input file '{input_filename}' not found in directory '{file_directory}'.")
    else:
        # Run the function
        keep_first_n_lines(input_path, output_path, num_lines_to_keep)

    print("Script finished.")
