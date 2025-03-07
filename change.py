import cv2
import os

input_folder = "D:/Projects/japan-app/dataset"
output_folder = "D:/Projects/japan-app/dataset_large"

os.makedirs(output_folder, exist_ok=True)

for letter in os.listdir(input_folder):
    letter_folder = os.path.join(input_folder, letter)
    output_letter_folder = os.path.join(output_folder, letter)
    os.makedirs(output_letter_folder, exist_ok=True)

    for img_name in os.listdir(letter_folder):
        img_path = os.path.join(letter_folder, img_name)
        image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        if image is None:
            continue
        
        # Keičiam dydį į 256x256
        image_resized = cv2.resize(image, (256, 256), interpolation=cv2.INTER_CUBIC)

        output_path = os.path.join(output_letter_folder, img_name)
        cv2.imwrite(output_path, image_resized)

print("✅ Visi vaizdai sėkmingai padidinti iki 256x256")
