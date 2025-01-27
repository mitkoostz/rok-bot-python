import pytesseract
from PIL import Image
import cv2
import re


class ImageNumberParser:
    @staticmethod
    def parse_number_from_image(image):
        # Convert the image to a format suitable for pytesseract
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image)
        # Use pytesseract to extract text from the image
        text = pytesseract.image_to_string(pil_image, config='--psm 6')
        match = re.search(r'\d{1,3}(?:,\d{3})*', text)
        if match:
            return int(match.group(0).replace(',', ''))
        else:
            return None
