import os
import img2pdf
import numpy as np
from pdf2image import convert_from_path
from PIL import ImageOps, Image

# Requires brew install of poppler !!!!

# Define the printer-paper white color range to floor it
BEIGE_LOWER = (187, 188, 187)  # Lower bound of beige
BEIGE_UPPER = (250, 250, 240)  # Upper bound of beige
PURE_WHITE = (255, 255, 255)


def floor_beige_to_white(img):
    """Convert beige background to pure white using NumPy for efficiency."""
    img_array = np.array(img)  # Convert image to NumPy array
    mask = np.all((img_array >= BEIGE_LOWER) & (img_array <= BEIGE_UPPER), axis=-1)  # Find beige pixels
    img_array[mask] = PURE_WHITE  # Replace with pure white
    return Image.fromarray(img_array)  # Convert back to PIL image


def invert_pdf_colors(input_pdf, output_pdf, temp_folder="temp_images"):
    """Inverts colors of a PDF and ensures the background is pure white."""
    if not os.path.exists(input_pdf):
        print(f"Error: Input file '{input_pdf}' not found!")
        return

    os.makedirs(temp_folder, exist_ok=True)

    images = convert_from_path(input_pdf)
    inverted_image_paths = []

    for i, img in enumerate(images):
        inverted_img = ImageOps.invert(img.convert("RGB"))  # Invert colors
        cleaned_img = floor_beige_to_white(inverted_img)  # Floor beige to white

        # Save temporarily
        temp_path = os.path.join(temp_folder, f"page_{i}.png")
        cleaned_img.save(temp_path)
        inverted_image_paths.append(temp_path)

    # Save as a new PDF
    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert(inverted_image_paths))

    # # Cleanup temp images
    # for temp_file in inverted_image_paths:
    #     os.remove(temp_file)

    print(f"Inverted PDF and floored to white, saved as: {output_pdf}")

if __name__ == "__main__":
    # Input Directory, File Name, and Output Path Below
    main_dir = 'data/'
    file_name = 'Problem Set 3 Revised.pdf'
    output_path = f"{main_dir}inverted/{file_name}"
    invert_pdf_colors(f"{main_dir}{file_name}", output_path)