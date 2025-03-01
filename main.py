from PIL import Image
import pillow_heif
import os
import time
from concurrent.futures import ThreadPoolExecutor
from progress.bar import IncrementalBar


def convert_heic(image_name, folder, output_format, progress_bar):
    output_folder = os.path.join(folder, output_format)
    os.makedirs(output_folder, exist_ok=True)
    output_name = f"{os.path.splitext(image_name)[0]}.{output_format.lower()}"
    output_path = os.path.join(output_folder, output_name)

    if os.path.exists(output_path):  # Пропускаем, если уже конвертировано
        progress_bar.next()
        return

    pillow_heif.register_heif_opener()
    image = Image.open(os.path.join(folder, image_name))
    image.save(output_path, output_format.upper())
    progress_bar.next()


def convert_heic_files(directory, output_format):
    output_folder = os.path.join(directory, output_format)
    os.makedirs(output_folder, exist_ok=True)

    files = [file for file in os.listdir(directory) if file.lower().endswith('.heic')]
    if not files:
        print("No HEIC files found.")
        return

    progress_bar = IncrementalBar('Progress', max=len(files))

    with ThreadPoolExecutor() as executor:
        for file in files:
            executor.submit(convert_heic, file, directory, output_format, progress_bar)

    progress_bar.finish()
    print(f"Finished! The results are saved in {output_folder}")


def main():
    while True:
        directory = input("Enter path to folder with your photos:\n").strip()
        if os.path.isdir(directory):
            break
        print("Invalid path. Try again.")

    print("Choose the converting mode:\n1. HEIC to PNG (high quality, slower)\n2. HEIC to JPEG (low quality, faster)")

    while True:
        try:
            mode = int(input())
            if mode in (1, 2):
                break
        except ValueError:
            pass
        print("Invalid choice. Enter 1 or 2.")

    t1 = time.time()
    format_map = {1: "PNG", 2: "JPEG"}
    convert_heic_files(directory, format_map[mode])
    t2 = time.time()

    print(f"Consumed time: {t2 - t1:.2f} seconds")
    input("\nPress enter to exit")


if __name__ == "__main__":
    main()
