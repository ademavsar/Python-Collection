import os

def list_files(startpath, output_file='directory_structure.txt'):
    with open(output_file, 'w') as f:
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * level
            f.write(f'{indent}{os.path.basename(root)}/\n')
            subindent = ' ' * 4 * (level + 1)
            for file in files:
                f.write(f'{subindent}{file}\n')

if __name__ == "__main__":
    directory_to_scan = '.'  # Mevcut dizini tarar, başka bir dizin taramak için yolu buraya yazın
    list_files(directory_to_scan)
