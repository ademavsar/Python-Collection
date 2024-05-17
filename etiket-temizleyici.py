import os
import re

# Bulunduğunuz dizindeki tüm .vtt dosyalarını dolaş
for filename in os.listdir('.'):
    if filename.endswith('.vtt'):
        # Dosyayı oku
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()

        # {\an8} etiketlerini kaldır
        updated_content = re.sub(r'\{\\an8\}', '', content)

        # Güncellenmiş içeriği aynı dosyaya yaz
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(updated_content)

        print(f'{filename} dosyasından \\an8 etiketleri temizlendi.')
