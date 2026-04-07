# Safra Kesesi Ultrason Görüntülerinde Kontrast Artırma ve Kenar Tespiti Analizi

Bu proje, safra kesesi ultrason görüntülerindeki lezyon (polip, karsinom, benign yapılar) görünürlüğünü artırmak ve kenar belirginliğini analiz etmek amacıyla geliştirilmiş akademik bir görüntü işleme çalışmasıdır.

**Önemli Not:** Projenin en büyük özelliği, işlemin arka planındaki matematiği tam anlamıyla yansıtabilmek adına **OpenCV gibi harici görüntü işleme kütüphaneleri kullanılmadan**, algoritmaların doğrudan pikseller ve matrisler üzerinde sıfırdan (from scratch) kodlanmış olmasıdır.

## 📌 Proje Kapsamı ve Uygulanan Yöntemler

Projede uygulanan tüm işlemler temel matematiksel fonksiyonlar ve konvolüsyon döngüleri ile yazılmıştır:

### 1. Görüntü Ön İşleme
* **Gri Seviye Dönüşümü ve Boyutlandırma:** Görüntüler standartlaştırma amacıyla tek kanallı gri seviyeye çevrilmiş ve 256x256 piksel boyutuna getirilmiştir.
* **Gürültü Azaltma (Manuel Median Filtre):** Ultrason görüntülerindeki karakteristik "speckle" (karıncalanma) gürültüsünü, kenar ve lezyon detaylarını bozmadan temizlemek için 3x3 komşuluk pikselleri üzerinde sıralama yapılarak manuel ortanca (median) değer filtresi uygulanmıştır.

### 2. Kontrast Artırma ve Histogram Analizi
Düşük kontrastlı ultrasonik yapıları ayrıştırmak için üç farklı yöntem uygulanmış ve parlaklık dağılımı histogram grafikleriyle incelenmiştir:
* **Manuel Histogram Eşitleme (Global):** Piksellerin Kümülatif Dağılım Fonksiyonu (CDF) hesaplanarak görüntünün dinamik aralığı 0-255 arasına homojen olarak yayılmıştır.
* **Gamma Düzeltme:** Görüntü parlaklığını doğrusal olmayan bir şekilde ayarlamak için kullanılmıştır (Gamma = 1.2).
* **Logaritmik Dönüşüm:** Düşük yoğunluklu (karanlık) piksellerdeki detayları daha görünür kılmak için uygulanmıştır.

### 3. Kenar Tespiti (Manuel Konvolüsyon)
Gürültüden arındırılmış ve kontrastı artırılmış (Histogram Eşitleme uygulanmış) görüntüler üzerinden, lezyon sınırlarını belirlemek için filtre çekirdekleri (kernel) ile konvolüsyon işlemi yapılmıştır:
* **Sobel Operatörü:** Yatay ve dikey gradyanlar hesaplanarak genel sınır tespiti yapılmıştır.
* **Scharr Operatörü:** İnce detaylara ve açısal doku farklarına daha duyarlı olduğu için tıbbi yapılar üzerindeki ince kenarlar vurgulanmıştır.
* **Laplacian Operatörü:** İkinci türev temelli basit kenar tespiti analizi yapılmıştır.

## 📂 Kullanılan Veri Seti
Projede **Gallbladder Polyps Dataset** ([Mendeley Data](https://data.mendeley.com/datasets/r6h24d2d3y/2)) baz alınmıştır. Proje kapsamında her hastanın verisi birbirinden farklı olmak üzere toplam 12 görüntü analiz edilmiştir:
* **4 Adet Benign** (Çamur, duvar kalınlaşması, iyi huylu yapılar)
* **4 Adet Polip** (Safra kesesi polipleri)
* **4 Adet Karsinom** (İleri düzey lezyon / Kitle)

## 🚀 Kurulum ve Çalıştırma

Proje, kütüphane bağımlılığını minimumda tutacak şekilde tasarlanmıştır. Yalnızca görüntü okuma, matris operasyonları ve grafik çizimi için temel kütüphaneler gereklidir.

1. Gerekli paketleri yükleyin:
   ```bash
   pip install numpy Pillow matplotlib
