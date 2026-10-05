import pytesseract
from PIL import Image

import code_solver


def read_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text.strip()


def solve_from_image(image_path):
    text = read_text(image_path)
    if not text:
        return "I couldn't read anything in that photo."

    if "=" in text or any(c.isalpha() for c in text):
        result = code_solver.solve_equation(text)
    else:
        result = code_solver.run_code(f"print({text})")

    return f'I read "{text}" and got: {result}'
