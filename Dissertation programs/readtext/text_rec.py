
import cv2
import os
import pytesseract
from PIL import Image
import re

def get_text(image_path, pre_processor="thresh"):
    images = cv2.imread(image_path)

    if images is None:
        raise FileNotFoundError(f"Image not found or could not be loaded: {image_path}")

    gray = cv2.cvtColor(images, cv2.COLOR_BGR2GRAY)

    if pre_processor == "thresh":
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    elif pre_processor == "blur":
        gray = cv2.medianBlur(gray, 3)

    filename = "{}.png".format(os.getpid()) #change the image format here.
    cv2.imwrite(filename, gray)
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)

    filtered_text = re.sub(r"[^\[\]1-8-]", "", text)

    return filtered_text

