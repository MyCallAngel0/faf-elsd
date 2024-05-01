from PIL import Image
import pytesseract
import json

with open('tokens.json', 'r') as file:
  data = json.load(file)

pytesseract.pytesseract.tesseract_cmd = data['TESSERACT_LOCATION']

print(pytesseract.image_to_string(Image.open('assets/images/hello-world.png'), config='psm 11'))

print(pytesseract.image_to_string('assets/images/Cedric.png', config='psm 7'))