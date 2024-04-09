import os
import subprocess


def list_files(directory):
    files = os.listdir(directory)
    return [file for file in files if file.endswith((".wav", ".mp3", ".ogg"))]


def play_file(file_path):
    print(file_path)
    subprocess.run(["aplay", file_path])


def main():
    music_dir = os.path.expanduser("~/Music")
    files = list_files(music_dir)

    if not files:
        print("No playable files found in ~/Music directory.")
        return

    print("Select a file to play:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")

    selection = input("Enter the number of the file to play: ")

    try:
        selection_index = int(selection) - 1
        if 0 <= selection_index < len(files):
            file_to_play = os.path.join(music_dir, files[selection_index])
            play_file(file_to_play)
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()
