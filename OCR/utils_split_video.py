import subprocess
import os
import sys
import pathlib
import time # Added for timing

# --- Video Splitting Function (Handles ONE video) ---
# Modified slightly to return success/failure and accept specific output dir
def split_video_equal_length(input_video_path: str, segment_duration_sec: int, video_specific_output_dir: str) -> bool:
    """
    Splits a SINGLE video into segments of equal duration using FFmpeg.

    Args:
        input_video_path (str): Path to the input video file.
        segment_duration_sec (int): The desired duration of each segment in seconds.
        video_specific_output_dir (str): The specific directory where segments
                                         for THIS video will be saved.

    Returns:
        bool: True if splitting was successful, False otherwise.
    """
    input_path = pathlib.Path(input_video_path)
    # Basic check for duration validity within the function
    if not isinstance(segment_duration_sec, int) or segment_duration_sec <= 0:
        print(f"Error: Segment duration must be a positive integer (seconds). (Video: {input_path.name})")
        return False # Indicate failure

    # Ensure the specific output directory for this video exists
    output_path = pathlib.Path(video_specific_output_dir)
    try:
        output_path.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"(!) Error creating output directory '{output_path}': {e}")
        return False

    # Construct the output filename pattern within the specific directory
    output_filename_pattern = output_path / f"{input_path.stem}_seg_%03d{input_path.suffix}"

    # Build FFmpeg Command
    command = [
        'ffmpeg',
        '-i', str(input_path),
        '-f', 'segment',
        '-segment_time', str(segment_duration_sec),
        '-c', 'copy',            # Copy streams (fast, no re-encoding)
        '-reset_timestamps', '1', # Reset timestamps for each segment
        # '-an',                 # Optional: Uncomment to remove audio
        '-y',                    # Optional: Overwrite output files without asking
        str(output_filename_pattern)
    ]

    print(f"--- Processing Video: {input_path.name} ---")
    print(f"    Segments will be saved to: {output_path.resolve()}")
    # print(f"    Running command: {' '.join(command)}") # Can be verbose, uncomment if needed

    # Execute FFmpeg Command
    try:
        # Use the standard call for Python 3.7+
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        # Optional: print ffmpeg logs only if needed for debugging, stderr often has progress
        # print(f"    FFmpeg Log (stderr):\n{result.stderr}")
        print(f"    Successfully split {input_path.name}.")
        return True # Indicate success

    except subprocess.CalledProcessError as e:
        print(f"(!) Error processing {input_path.name} (FFmpeg failed):")
        print(f"    Return code: {e.returncode}")
        # Print only stderr on error, as it usually contains the useful error message
        print(f"    FFmpeg Error Output:\n{e.stderr}")
        return False # Indicate failure
    except Exception as e:
        # Catch other potential errors during subprocess execution
        print(f"(!) An unexpected error occurred processing {input_path.name}: {e}")
        print(f"    Exception type: {type(e).__name__}")
        return False # Indicate failure


# --- Folder Processing Function ---
def process_folder(input_folder_path: str, segment_duration_sec: int, main_output_dir: str = "output_segments"):
    """
    Finds video files in a folder and splits each into segments,
    saving segments in subdirectories named after the original video.
    """
    input_dir = pathlib.Path(input_folder_path)
    main_out_dir = pathlib.Path(main_output_dir)

    # --- Input Folder Validation ---
    if not input_dir.is_dir():
        print(f"Error: Input folder not found or is not a directory: '{input_folder_path}'")
        return

    # --- Define recognizable video extensions (add more if needed) ---
    # Using lowercase for case-insensitive matching
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.mpg', '.mpeg'}
    print(f"Recognized video extensions: {', '.join(sorted(list(video_extensions)))}")

    # --- Check for FFmpeg (only need to check once) ---
    try:
        print("Checking for FFmpeg...")
        subprocess.run(['ffmpeg', '-version'], check=True, capture_output=True, text=True)
        print("FFmpeg found.")
    except FileNotFoundError:
        print("Error: 'ffmpeg' command not found.")
        print("Please ensure FFmpeg is installed and added to your system's PATH.")
        sys.exit(1) # Exit if FFmpeg is missing
    except subprocess.CalledProcessError as e:
         # Log stderr from ffmpeg -version if it fails
         print(f"Warning: Could not verify FFmpeg version (Error: {e.stderr.strip()}). Attempting to proceed.")
    print("-" * 30)

    # --- Scan for Video Files ---
    print(f"Scanning folder: {input_dir.resolve()}")
    videos_to_process = []
    for item in input_dir.iterdir():
        # Check if it's a file and if its suffix is in our list
        if item.is_file() and item.suffix.lower() in video_extensions:
            videos_to_process.append(item)

    if not videos_to_process:
        print("No video files with recognized extensions found in the specified folder.")
        return

    print(f"Found {len(videos_to_process)} video file(s) to process:")
    # Sort for consistent processing order
    videos_to_process.sort()
    for video_path in videos_to_process:
        print(f"  - {video_path.name}")
    print("-" * 30)

    # --- Process Each Video ---
    success_count = 0
    failure_count = 0
    start_time_all = time.time()

    for index, video_path in enumerate(videos_to_process):
        print(f"\n[{index + 1}/{len(videos_to_process)}] Starting job for: {video_path.name}")
        start_time_video = time.time()

        # Create a specific output sub-directory for this video's segments
        # named after the video file (without extension)
        video_specific_output_path = main_out_dir / video_path.stem

        # Call the splitting function for the current video
        success = split_video_equal_length(
            str(video_path),                # Pass video path as string
            segment_duration_sec,           # Pass duration
            str(video_specific_output_path) # Pass specific output dir as string
        )

        end_time_video = time.time()
        duration_video = end_time_video - start_time_video

        if success:
            success_count += 1
            print(f"    Finished processing {video_path.name} in {duration_video:.2f} seconds.")
        else:
            failure_count += 1
            # Error message is printed inside split_video_equal_length
            print(f"    Failed to process {video_path.name}.")
        # Add a small separator line between video logs
        print("-" * 20)


    # --- Final Summary ---
    end_time_all = time.time()
    total_duration = end_time_all - start_time_all
    print("\n" + "=" * 30)
    print("      Batch Processing Summary      ")
    print("=" * 30)
    print(f"Total videos scanned: {len(videos_to_process)}")
    print(f"Successfully processed: {success_count}")
    print(f"Failed: {failure_count}")
    print(f"Total processing time: {total_duration:.2f} seconds")
    print(f"Output segments located in subdirectories under: {main_out_dir.resolve()}")
    print("=" * 30)


# --- Main Execution Block (`if __name__ == "__main__":`) ---
if __name__ == "__main__":
    print("--- Video Folder Splitter ---")

    # Get folder path from user
    while True:
        folder_path_str = input("Enter the full path to the FOLDER containing video files: ")
        input_folder = pathlib.Path(folder_path_str)
        if input_folder.is_dir():
            break
        else:
            print(f"Error: Folder not found or not a directory. Please check the path: '{folder_path_str}'")

    # Get segment duration from user (same as before)
    while True:
        try:
            duration_str = input("Enter the desired duration for each segment (in seconds): ")
            duration_sec = int(duration_str)
            if duration_sec > 0:
                break
            else:
                print("Please enter a positive number of seconds.")
        except ValueError:
            print("Invalid input. Please enter a whole number for seconds.")

    # Get main output directory name (optional, same as before)
    main_output_folder = input("Enter the main output directory name (e.g., 'processed_videos') [leave blank for 'output_segments']: ")
    if not main_output_folder:
        main_output_folder = "output_segments" # Default value

    # Call the folder processing function
    process_folder(str(input_folder), duration_sec, main_output_folder)