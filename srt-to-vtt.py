import glob

def srt_to_vtt(srt_file_path, vtt_file_path):
    with open(srt_file_path, 'r', encoding='utf-8') as srt_file:
        lines = srt_file.readlines()

    vtt_lines = ['WEBVTT\n\n']

    for line in lines:
        if '-->' in line:
            line = line.replace(',', '.')
        vtt_lines.append(line)

    with open(vtt_file_path, 'w', encoding='utf-8') as vtt_file:
        vtt_file.writelines(vtt_lines)

def convert_all_srt_to_vtt():
    # Çalışma dizinindeki tüm .srt dosyalarını bul
    srt_files = glob.glob('*.srt')

    for srt_file in srt_files:
        # Dosya isminin temelini al ve .vtt uzantısı ekle
        vtt_file = f"{srt_file.rsplit('.', 1)[0]}.vtt"
        srt_to_vtt(srt_file, vtt_file)
        print(f"'{srt_file}' başarıyla '{vtt_file}' olarak dönüştürüldü.")

# Tüm .srt dosyalarını .vtt'ye dönüştür
convert_all_srt_to_vtt()
