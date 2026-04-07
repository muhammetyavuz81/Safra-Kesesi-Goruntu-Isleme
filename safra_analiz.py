import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

def safra_kesesi_analiz(image_path):
    if not os.path.exists(image_path):
        print(f"Hata: {image_path} bulunamadı. Lütfen dosya adını kontrol edin.")
        return


    img = Image.open(image_path).convert('L')
    img = img.resize((256, 256))
    img_array = np.array(img, dtype=float)

   
    def manual_median(data):
        h, w = data.shape
        output = np.copy(data)
        for i in range(1, h-1):
            for j in range(1, w-1):
                neighbors = data[i-1:i+2, j-1:j+2].flatten()
                output[i, j] = np.sort(neighbors)[4]
        return output

    img_denoised = manual_median(img_array)

    
    
    def hist_eq(data):
        hist, _ = np.histogram(data.flatten(), 256, [0,256])
        cdf = hist.cumsum()
        cdf_m = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())
        return cdf_m[data.astype('uint8')]


    def gamma_corr(data, g=1.2):
        return 255 * (data / 255) ** g

   
    def log_trans(data):
        c = 255 / np.log(1 + np.max(data))
        return c * np.log(1 + data)

    img_he = hist_eq(img_denoised)
    img_gamma = gamma_corr(img_denoised)
    img_log = log_trans(img_denoised)


    def apply_kernel(data, kernel):
        h, w = data.shape
        res = np.zeros((h, w))
        for i in range(1, h-1):
            for j in range(1, w-1):
                res[i, j] = np.sum(data[i-1:i+2, j-1:j+2] * kernel)
        return res

    
    sx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sy = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    sobel = np.sqrt(apply_kernel(img_he, sx)**2 + apply_kernel(img_he, sy)**2)

    
    shx = np.array([[-3, 0, 3], [-10, 0, 10], [-3, 0, 3]])
    shy = np.array([[-3, -10, -3], [0, 0, 0], [3, 10, 3]])
    scharr = np.sqrt(apply_kernel(img_he, shx)**2 + apply_kernel(img_he, shy)**2)

    
    lap_k = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
    laplacian = np.abs(apply_kernel(img_he, lap_k))

   
    fig, axs = plt.subplots(3, 3, figsize=(15, 12))
    plt.suptitle(f"Analiz: {image_path}", fontsize=16)

    
    axs[0, 0].imshow(img_array, cmap='gray'); axs[0, 0].set_title("Orijinal (Gri)")
    axs[0, 1].imshow(img_denoised, cmap='gray'); axs[0, 1].set_title("Median Filtre (Gürültü Azaltma)")
    axs[0, 2].hist(img_array.flatten(), 256, [0,256], color='gray'); axs[0, 2].set_title("Orijinal Histogram")

    
    axs[1, 0].imshow(img_he, cmap='gray'); axs[1, 0].set_title("Histogram Eşitleme")
    axs[1, 1].imshow(img_gamma, cmap='gray'); axs[1, 1].set_title("Gamma Düzeltme")
    axs[1, 2].imshow(img_log, cmap='gray'); axs[1, 2].set_title("Logaritmik Dönüşüm")

    
    axs[2, 0].imshow(sobel, cmap='gray'); axs[2, 0].set_title("Sobel Operatörü")
    axs[2, 1].imshow(scharr, cmap='gray'); axs[2, 1].set_title("Scharr Operatörü")
    axs[2, 2].imshow(laplacian, cmap='gray'); axs[2, 2].set_title("Laplacian Operatörü")

    for ax in axs.flat:
        if ax != axs[0, 2]: 
            ax.axis('off')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
 

if __name__ == "__main__":
 
    safra_kesesi_analiz("test.jpg")  // test yerine resmin ismini yazın orn:b1.jpg
