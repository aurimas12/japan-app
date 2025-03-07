import tensorflow as tf
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Įkeliame vaizdą
image_path = '/mnt/data/hiragana-e.PNG'
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Keičiam į RGB, nes OpenCV naudoja BGR

# Keletas transformacijų su tf.image
def augment_image(image):
    # Atsitiktinis pasukimas
    image = tf.image.rot90(image)  # Sukimas 90 laipsnių kampu

    # Atsitiktinis dydžio pakeitimas
    image = tf.image.resize(image, (256, 256))

    # Atsitiktinis triukšmo pridėjimas (pvz., Gaussian noise)
    noise = tf.random.normal(shape=tf.shape(image), mean=0.0, stddev=0.1, dtype=tf.float32)
    image = tf.clip_by_value(image + noise, 0.0, 255.0)

    return image

# Atlikti augmentavimą
augmented_image = augment_image(image)

# Pavaizduoti originalų ir augmentuotą vaizdą
plt.subplot(1, 2, 1)
plt.imshow(image)
plt.title('Originalus Vaizdas')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(augmented_image)
plt.title('Augmentuotas Vaizdas')
plt.axis('off')

plt.show()
