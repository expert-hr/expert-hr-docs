import json
import re
import io
import base64

import fitz

from markdownify import markdownify as md

from pdfminer.converter import HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

import cv2
import numpy as np
from PIL import Image


def extract_images(file: bytes) -> list[io.BytesIO]:
    doc = fitz.open(stream=io.BytesIO(file))

    images = []
    for idx in range(len(doc)):
        xrefs = [image[0] for image in doc.get_page_images(idx)]
        images.extend([doc.extract_image(xref)["image"] for xref in xrefs])

    pimages = [Image.open(io.BytesIO(image)) for image in images]
    images = [io.BytesIO() for _ in range(len(pimages))]
    for idx, image in enumerate(pimages):
        image.save(images[idx], "png")

    return images


def detect_face(bytes_face: str) -> bool:
    img = _readb64(bytes_face)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    face = face_classifier.detectMultiScale(
        gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
    )

    return isinstance(face, np.ndarray) and np.sum(face) != 0


def _readb64(uri):
    encoded_data = uri.split(";")[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def pdf_to_markdown(file: bytes) -> str:
    rsrcmgr = PDFResourceManager()
    retstr = io.BytesIO()
    laparams = LAParams()

    device = HTMLConverter(rsrcmgr, retstr, codec="utf-8", laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    reader = io.BytesIO(file)
    for page in PDFPage.get_pages(reader):
        interpreter.process_page(page)

    text = retstr.getvalue().decode()

    device.close()
    retstr.close()

    text = md(text)

    return text


def fix_empty_value_exception(exc: str, input_text: str):
    pattern = r"\(char (\d+)\)"
    match = re.search(pattern, exc)
    char_value = int(match.group(1))
    new_text = input_text[:char_value] + "null" + input_text[char_value:]
    return new_text


def json_loading(text):
    try:
        json_object = json.loads(text)
        return json_object
    except Exception as e:
        e = str(e)
        pattern = r"Expecting value: line \d+ column \d+ \(char \d+\)"
        if re.match(pattern, e):
            new_text = fix_empty_value_exception(e, text)
            obj = json_loading(new_text)
            return obj
        else:
            # print(e)
            return "Failed to parse"
