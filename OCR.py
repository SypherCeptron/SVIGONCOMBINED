import pytesseract
def OCR(Image):

    Text = pytesseract.image_to_string(Image)
    return Text
