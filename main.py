from PIL import Image
import pillow_heif
import os
from progress.bar import IncrementalBar


def convert_to_png(image_name, folder):
    pillow_heif.register_heif_opener()
    image = Image.open(f'{folder}/{image_name}')
    image_name = f'{image_name[:-5]}.png'
    image.save(os.path.join(folder, 'PNG', image_name), format('PNG'))


def convert_to_jpg(image_name, folder):
    heif_file = pillow_heif.read_heif(f'{folder}/{image_name}')
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
    )
    image_name = f'{image_name[:-5]}.jpg'
    image.save(os.path.join(folder, 'JPEG', image_name), format('JPEG'))


def heic_to_png(directory):
    if not os.path.exists(f'{directory}/PNG'):
        os.mkdir(f'{directory}/PNG')

    count_of_files = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.HEIC'):
                count_of_files += 1
    progress_bar = IncrementalBar('Progress', max=count_of_files)

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.HEIC'):
                convert_to_png(file, root)
                progress_bar.next()
    progress_bar.finish()

def heic_to_jpeg(directory):
    if not os.path.exists(f'{directory}/JPEG'):
        os.mkdir(f'{directory}/JPEG')

    count_of_files = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.HEIC'):
                count_of_files += 1
    progress_bar = IncrementalBar('Progress', max=count_of_files)

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.HEIC'):
                convert_to_jpg(file, root)
                progress_bar.next()
    progress_bar.finish()


def main():
    while True:
        directory = input("Enter path to folder with your photos:\n")
        if os.path.exists(directory):
            break
    print("Choose the converting mode:\n1. HEIC to PNG (high quality, slower)\n2. HEIC to JPEG (low quality, faster)")
    mode = 0

    while True:
        try:
            mode = int(input())
        except ValueError:
            continue
        if mode not in (1, 2):
            continue
        break

    if mode == 1:
        heic_to_png(directory)
    elif mode == 2:
        heic_to_jpeg(directory)
    else:
        print("Unexpected error")

    print("Finished!")
    input("\nPress enter to continue")


if __name__ == "__main__":
    main()
