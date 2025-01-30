import pytesseract
from PIL import Image
import cv2
import re


class ImageNumberExtractor:
    @staticmethod
    def get_comma_separated_decimal(image):
        match = ImageNumberExtractor.get_first_number_match(image, r'\d{1,3}(?:,\d{3})*')
        if match is not None:
            return int(match.replace(',', ''))
        else:
            return None

    @staticmethod
    def get_integer_from_image(self, image):
        match = ImageNumberExtractor.get_first_number_match(image, r'\d+')
        if match is not None:
            return int(match)
        else:
            return None

    @staticmethod
    def get_first_number_match(image, regex):
        # Convert the image to a format suitable for pytesseract
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image)
        # Use pytesseract to extract text from the image
        text = pytesseract.image_to_string(pil_image, config='--psm 6')
        match = re.search(regex, text)
        if match:
            return match.group(0)
        else:
            return None
