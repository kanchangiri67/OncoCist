# app/utils/image_preprocessor.py

import numpy as np

class ImagePreprocessor:
    @staticmethod
    def normalize(image):
        import numpy as np
        image = np.float64(image)
        min_val, max_val = np.min(image), np.max(image)
        if max_val == min_val:
            return np.zeros_like(image, dtype=np.uint8)
        return np.uint8(255 * (image - min_val) / (max_val - min_val))

    def cnn_image_preprocessor(image):
        # Change grayscale image to rgb for CNN model
        image = np.repeat(image, 3, axis=-1)

        # Normalize the data
        image = image / 255.0
        return image