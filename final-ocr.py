import pandas as pd
import re
import pytesseract
import easyocr
from glob import glob
from tqdm.notebook import tqdm

# Membaca daftar file gambar
img_fns = glob('/Users/sulis/OneDrive/Desktop/New folder/image/*')

# Inisialisasi easyocr reader
reader = easyocr.Reader(['id'], gpu=True)

# Membuat list untuk menyimpan hasil ekstraksi teks
results_list = []

# Loop melalui setiap file gambar
for img_fn in tqdm(img_fns, desc='Processing Images'):
    # Menggunakan pytesseract untuk mendapatkan teks dari gambar
    tesseract_text = pytesseract.image_to_string(img_fn, lang='ind')
    
    # Menggunakan easyocr untuk mendapatkan teks dan bounding box dari gambar
    easyocr_results = reader.readtext(img_fn)
    
    # Menemukan kata yang memiliki kemungkinan tinggi menjadi nama
    possible_names = re.findall(r'\b(?:[A-Z][a-z]*\s*){2,}\b', tesseract_text)
    
    # Jika ada kemungkinan nama, ambil yang pertama
    if possible_names:
        name = possible_names[0]
    else:
        name = None
    
    # Menambahkan hasil ke dalam list
    results_list.append({
        'Image Filename': img_fn,
        'Tesseract Text': tesseract_text,
        'EasyOCR Results': easyocr_results,
        'Name': name
    })

# Membuat DataFrame dari list hasil
df_results = pd.DataFrame(results_list)

# Menyimpan DataFrame ke dalam file Excel
excel_filename = '/Users/sulis/OneDrive/Desktop/New folder/hasil_ekstraksi_teks.xlsx'
df_results.to_excel(excel_filename, index=False)

print(f'Hasil ekstraksi teks disimpan dalam file Excel: {excel_filename}')
