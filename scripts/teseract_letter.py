import cv2
import pytesseract

from dictionaries import hiragana_dict
# Nurodykite teisingą Tesseract kelią
pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"


# Įkelti paveikslėlį
image = cv2.imread("D:\Projects\japan-app\scripts\data/hiragana-a.png")

# Konvertuoti į pilką spalvą
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

# Išsaugoti apdorotą paveikslėlį (patikrinimui)
cv2.imwrite("processed_image.png", binary)
