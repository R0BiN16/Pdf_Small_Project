from pathlib import Path
from typing import Union, Literal, List
from PyPDF2 import PdfReader, PdfWriter

def text_extractor(page_number: int):
    try:
        reader = PdfReader("file1.pdf")
        page = reader.pages[page_number - 1]  # Adjust index since pages are 0-indexed
        text = page.extract_text()

        # Create a new PDF with the extracted text
        with open(f"page_{page_number}_text.pdf", "wb") as f:
            writer = PdfWriter()
            writer.add_page(page)
            writer.write(f)

        print(f"Text from page {page_number} extracted and saved to page_{page_number}_text.pdf")
    except Exception as e:
        print(f"An error occurred: {e}")

def extract_images():
    try:
        reader = PdfReader("file1.pdf")
        page = reader.pages[0]
        count = 0
        for image_file_object in page.images:
            with open(f"{count}_{image_file_object.name}", "wb") as fp:
                fp.write(image_file_object.data)
                count += 1
        print("Images extracted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def encryption():
    reader = PdfReader("file1.pdf")
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt("my-secret-password")
    with open("encrypted-pdf.pdf", "wb") as f:
        writer.write(f)

def decryption():
    reader = PdfReader("file1.pdf")
    writer = PdfWriter()
    if reader.is_encrypted:
        reader.decrypt("my-secret-password")
    for page in reader.pages:
        writer.add_page(page)
    with open("decrypted-pdf.pdf", "wb") as f:
        writer.write(f)

def watermark(
    content_pdf: Path,
    stamp_pdf: Path,
    pdf_result: Path,
    page_indices: Union[Literal["ALL"], List[int]] = "ALL",
):
    reader = PdfReader(content_pdf)
    if page_indices == "ALL":
        page_indices = list(range(0, len(reader.pages)))

    writer = PdfWriter()
    for index in page_indices:
        content_page = reader.pages[index]
        mediabox = content_page.mediabox

        # You need to load it again, as the last time it was overwritten
        reader_stamp = PdfReader(stamp_pdf)
        image_page = reader_stamp.pages[0]

        image_page.merge_page(content_page)
        image_page.mediabox = mediabox
        writer.add_page(image_page)

    with open(pdf_result, "wb") as fp:
        writer.write(fp)

def merger():
    merger = PdfWriter()

    for pdf in ["file1.pdf", "file2.pdf", "file3.pdf"]:
        merger.append(pdf)

    merger.write("merged-pdf.pdf")
    merger.close()

def filesize_reduce():
    reader = PdfReader("file1.pdf")
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.add_metadata(reader.metadata)
    with open("smaller-new-file.pdf", "wb") as fp:
        writer.write(fp)

def image_quality():
    reader = PdfReader("file1.pdf")
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    for page in writer.pages:
        for img in page.images:
            img.replace(img.image, quality=80)
    with open("out.pdf", "wb") as f:
        writer.write(f)

print("Which function do you want to run?")
options = [
    ("Text extractor+merger", text_extractor),
    ("Image extracting", extract_images),
    ("Encryption", encryption),
    ("Decryption", decryption),
    ("Watermark", watermark),
    ("Merger", merger),
    ("Reduce File size", filesize_reduce),
    ("Reduce Image quality", image_quality)
]

for i, (option, _) in enumerate(options):
    print(f"For {option}, press {i + 1}")

user_input = int(input("Enter the Number: ")) - 1
if 0 <= user_input < len(options):
    if options[user_input][0] == "Text extractor+merger":
        page_number = int(input("Enter the page number: "))
        options[user_input][1](page_number)
    else:
        options[user_input][1]()
else:
    print("Invalid input!")
