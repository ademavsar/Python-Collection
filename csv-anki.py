import os
import csv
import re

def extract_expressions(srt_content):
    expressions = []
    is_expression = False

    for line in srt_content:
        line = line.strip()
        if "-->" in line:  # Zaman damgası satırını bul
            is_expression = True
        elif line.isdigit() or not line:  # Yeni altyazı bloğu veya boş satır
            is_expression = False
            if expressions:
                yield "\n".join(expressions)  # Satırları '\n' ile birleştir
                expressions = []
        elif is_expression:  # Zaman damgasından sonraki metin satırları
            expressions.append(line)
    
    if expressions:  # Son altyazı bloğunu da ekleyelim
        yield "\n".join(expressions)

# Çalışma dizinini al
work_dir = os.getcwd()

# CSV dosyası oluştur
csv_file = 'anki_import.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # CSV başlıklarını yaz (video sütunu 8. sırada)
    writer.writerow(['Id', 'Expression', 'Meaning', 'Notes', 'Add Reverse', 'Snapshot', 'Audio', 'Video', 'Tags'])

    # Dizin içindeki dosyalara göz at
    for filename in os.listdir(work_dir):
        if filename.endswith(('.mp4', '.mkv', '.webm')):  # Video dosyalarını kontrol et
            # Dosya isminden ID'yi çıkart
            base_name = os.path.splitext(filename)[0]
            srt_filename = base_name + '.srt'
            # Sezon ve bölüm bilgilerini çıkar (örneğin "S01E01")
            season_episode_match = re.search(r'S(\d+)E(\d+)', filename)
            season_episode_tag = f"S{season_episode_match.group(1)}E{season_episode_match.group(2)}" if season_episode_match else ""

            # Eğer ilgili SRT dosyası varsa, içeriğini oku
            if os.path.exists(srt_filename):
                with open(srt_filename, 'r', encoding='utf-8') as srt_file:
                    srt_content = srt_file.readlines()
                    expressions = list(extract_expressions(srt_content))
                    # Her replik için bir satır oluştur
                    for expression in expressions:
                        writer.writerow([base_name, expression.replace("\n", "<br>"), '', '', '', '', '', f'[sound:{filename}]', season_episode_tag])

print(f'{csv_file} dosyası başarıyla oluşturuldu.')
