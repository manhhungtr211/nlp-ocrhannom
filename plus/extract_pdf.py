import fitz  # PyMuPDF
import os
import cv2

# STEP 1: Define the file path and the output directory
file = "resources/p61-p102_TongTapVanHocVietNam06.pdf"
output_dir = "data/images"
data_name = "TongHopVanHocVietNam06_page"


# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Open the PDF file
pdf_file = fitz.open(file)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate over each page in the PDF
for page_index in range(len(pdf_file)):
    # Load the page
    page = pdf_file.load_page(page_index)
    # Get all images on the page
    image_list = page.get_images(full=True)

    # Print the number of images found on this page
    if image_list:
        print(f"[+] Found {len(image_list)} image(s) on page {page_index + 1}")

        for img_index, img in enumerate(image_list):
            # Get the XREF of the image
            xref = img[0]
            # Extract the image bytes
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]
            # Get the image extension
            image_ext = base_image["ext"]
            # Create the image file name
            image_name = f"{data_name}{page_index + 1:03}.png"
            # Full path for saving the image
            image_path = os.path.join(output_dir, image_name)

            # Save the image
            with open(image_path, "wb") as image_file:
                image_file.write(image_bytes)
                print(f"[+] Image saved as {image_path}")
    else:
        print(f"[!] No images found on page {page_index + 1}")

# Close the PDF file
pdf_file.close()
print(f"All images have been saved in the '{output_dir}' directory.")
