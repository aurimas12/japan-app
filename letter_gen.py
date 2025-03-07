import tensorflow as tf
import numpy as np
import random
import os
from PIL import Image, ImageDraw, ImageFont

# Hiragana simboliai
hiragana_chars = list("あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん")
n_chars = len(hiragana_chars)

# Parametrai
dataset_size = 10000  # Kiek duomenų taškų sugeneruoti
image_size = (64, 64)  # Vaizdo dydis
font_path = "NotoSansJP-Regular.otf"  # Japonų simbolius palaikantis šriftas
output_dir = "hiragana_dataset"  # Kur saugoti vaizdus
os.makedirs(output_dir, exist_ok=True)

# Generuojame atsitiktines raides
data = [random.choice(hiragana_chars) for _ in range(dataset_size)]

# Teisingas simbolių indeksų žemėlapis
char_to_index = {char: idx for idx, char in enumerate(hiragana_chars)}

# Generuojame ir saugome vaizdus
def create_image(character, index):
    img = Image.new("RGB", image_size, color=(255, 255, 255))  # Baltas fonas, geresnis kontrastas
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype(font_path, 48)  # Naudojame japonų simbolius palaikantį šriftą
    except Exception as e:
        print(f"Klaida įkeliant šriftą: {e}")
        return
    
    bbox = draw.textbbox((0, 0), character, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (image_size[0] - text_width) / 2
    y = (image_size[1] - text_height) / 2
    
    draw.text((x, y), character, font=font, fill=(0, 0, 0))  # Juodas tekstas geresniam matomumui
    draw.rectangle([(0, 0), (image_size[0] - 1, image_size[1] - 1)], outline=(0, 0, 0))  # Rėmelis debugging'ui
    
    # Išsaugome tik jei simbolis yra žemėlapyje
    if character in char_to_index:
        img.save(os.path.join(output_dir, f"{index}_{char_to_index[character]}.png"))
    else:
        print(f"Įspėjimas: Simbolis '{character}' nerastas žemėlapyje!")

# Sukuriame ir išsaugome vaizdus
for i, char in enumerate(data):
    create_image(char, i)

print(f"Išsaugota {dataset_size} vaizdų kataloge '{output_dir}'")
