import os
import cv2
import pytesseract
from constants import teserract
from dictionaries import hiragana_dict

# Nurodykite teisingą Tesseract kelią
pytesseract.pytesseract.tesseract_cmd = teserract



image = cv2.imread(r"D:\Projects\japan-app\scripts\data\hiragana-e.PNG")  # Naudok bet kokį paveikslėlį su hiragana
text = pytesseract.image_to_string(image, lang="jpn")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Binarizuoti paveikslėlį
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Atpažinti simbolį
text = pytesseract.image_to_string(binary, lang='jpn', config='--psm 8').strip()

# Surasti reikšmę žodyne
meaning = hiragana_dict.get(text, "Nerasta")

# Atspausdinti rezultatą
print(f"Nuskaitytas simbolis: {text}")
print(f"Reikšmė: {meaning}")
print("Atpažintas tekstas:", text)
