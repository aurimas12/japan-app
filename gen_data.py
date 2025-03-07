import os
import cv2
import numpy as np

def generate_hiragana_dataset(input_files, output_dir, num_variants=1000):
    # Užtikriname, kad išvesties katalogas egzistuoja
    os.makedirs(output_dir, exist_ok=True)
    
    # Augmentacijos funkcijos
    def augment_image(image, num_variants):
        augmented_images = []
        
        # Konvertuojam į pilką formatą
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Salt & Pepper triukšmo procentas
        s_vs_p = 0.02  # 2% triukšmo proporcija
        
        for i in range(num_variants):
            # Atsitiktinis kontrastas ir ryškumas
            alpha = np.random.uniform(0.7, 1.3)
            beta = np.random.randint(-50, 50)
            adjusted = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
            
            # Atsitiktinis pasukimas
            angle = np.random.randint(-15, 15)
            (h, w) = adjusted.shape[:2]
            M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
            rotated = cv2.warpAffine(adjusted, M, (w, h))
            
            # Patikrinkime, ar vaizdas yra spalvotas (3 kanalai)
            if len(rotated.shape) == 3:  # RGB vaizdas
                # Pridėti Gauss’o triukšmą
                gauss = np.random.normal(0, 25, (h, w, 3)).astype('uint8')
                noisy_gauss = cv2.add(rotated, gauss)
                
                # Pridėti "Salt & Pepper" triukšmą
                noisy_sp = rotated.copy()
                num_salt = np.ceil(s_vs_p * h * w)
                coords = [np.random.randint(0, i - 1, int(num_salt)) for i in noisy_sp.shape]
                noisy_sp[coords[0], coords[1]] = 255
                num_pepper = np.ceil(s_vs_p * h * w)
                coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in noisy_sp.shape]
                noisy_sp[coords[0], coords[1]] = 0
                
                # Inversija
                inverted = cv2.bitwise_not(noisy_gauss)
                
                # Sepia efektas
                sepia = cv2.applyColorMap(rotated, cv2.COLORMAP_PINK)
                
                # Atsitiktinis blur
                blur_level = np.random.choice([3, 5, 7])
                blurred = cv2.GaussianBlur(rotated, (blur_level, blur_level), 0)
                
                # Fono keitimas
                backgrounds = [255, 128, 0]  # Balta, pilka, juoda
                bg_color = np.random.choice(backgrounds)
                background = np.full((h, w, 3), bg_color, dtype=np.uint8)
                masked = cv2.bitwise_or(rotated, background)
                
                # Perspective Transform
                pts1 = np.float32([[5, 5], [w-5, 5], [5, h-5], [w-5, h-5]])
                pts2 = np.float32([[np.random.randint(0, 10), np.random.randint(0, 10)],
                                    [w-np.random.randint(0, 10), np.random.randint(0, 10)],
                                    [np.random.randint(0, 10), h-np.random.randint(0, 10)],
                                    [w-np.random.randint(0, 10), h-np.random.randint(0, 10)]])
                matrix = cv2.getPerspectiveTransform(pts1, pts2)
                perspective = cv2.warpPerspective(rotated, matrix, (w, h))
                
                # RGB Shift
                shift = np.random.randint(-20, 20, 3)
                rgb_shifted = cv2.merge([np.clip(rotated[:,:,0] + shift[0], 0, 255),
                                         np.clip(rotated[:,:,1] + shift[1], 0, 255),
                                         np.clip(rotated[:,:,2] + shift[2], 0, 255)])
                
                # JPEG Artefaktai (sugadintas kokybės efektas)
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), np.random.randint(20, 70)]
                _, encoded_image = cv2.imencode('.jpg', rotated, encode_param)
                jpeg_artifact = cv2.imdecode(encoded_image, 1)
                
                augmented_images.extend([rotated, noisy_gauss, noisy_sp, inverted, sepia, blurred, masked, perspective, rgb_shifted, jpeg_artifact])
            else:
                # Jei vaizdas yra pilkos spalvos, atlikti tik pilkos spalvos operacijas
                gauss = np.random.normal(0, 25, (h, w)).astype('uint8')
                noisy_gauss = cv2.add(rotated, gauss)
                
                noisy_sp = rotated.copy()
                num_salt = np.ceil(s_vs_p * h * w)
                coords = [np.random.randint(0, i - 1, int(num_salt)) for i in noisy_sp.shape]
                noisy_sp[coords[0], coords[1]] = 255
                num_pepper = np.ceil(s_vs_p * h * w)
                coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in noisy_sp.shape]
                noisy_sp[coords[0], coords[1]] = 0
                
                inverted = cv2.bitwise_not(noisy_gauss)
                
                blurred = cv2.GaussianBlur(rotated, (3, 3), 0)
                
                augmented_images.extend([rotated, noisy_gauss, noisy_sp, inverted, blurred])
        
        return augmented_images

    dataset = {}
    for label, filepath in input_files.items():
        # Įkelti originalų vaizdą
        image = cv2.imread(filepath)
        augmented_images = augment_image(image, num_variants)
        
        # Sukurti katalogą su etiketės pavadinimu
        label_dir = os.path.join(output_dir, label)
        os.makedirs(label_dir, exist_ok=True)  # Sukuriame subdirektoriją kiekvienai etiketei
        
        # Išsaugoti kiekvieną sugeneruotą vaizdą su unikaliu pavadinimu
        for idx, img in enumerate(augmented_images):
            filename = os.path.join(label_dir, f"{label}_augmented_{idx+1}.jpg")
            cv2.imwrite(filename, img)
        
        dataset[label] = augmented_images
    
    return dataset

# Įrašyti kelią su originaliais failais
input_files = {
    "a": "scripts/data/hiragana-a.PNG",
    "i": "scripts/data/hiragana-i.PNG",
    "u": "scripts/data/hiragana-u.PNG",
    "e": "scripts/data/hiragana-e.PNG",
    "o": "scripts/data/hiragana-o.PNG",
}

# Nurodyti išvesties katalogą
output_dir = 'gen_dataset'  # Katalogas, kuriame bus išsaugoti sugeneruoti vaizdai

# Sugeneruoti datasetą su 1000 variantų
augmented_dataset = generate_hiragana_dataset(input_files, output_dir, num_variants=1000)

# Pavyzdys, kaip pasiekti sugeneruotus vaizdus
print("Sugeneruotų vaizdų keliai:")

for label, images in augmented_dataset.items():
    print(f"{label} - {len(images)} variantų sugeneruota.")
    for i, img in enumerate(images[:10]):  # Pavyzdžiui, atspausdinti pirmus 10 variantų
        print(f"  {label}_augmented_{i+1}.jpg")
