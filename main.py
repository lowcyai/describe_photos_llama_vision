import ollama
import csv
from pathlib import Path
from PIL import Image
import sys
from datetime import datetime

def image_already_processed(image_name, csv_path):
    if not Path(csv_path).is_file():
        return False
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Filename'] == image_name:
                return True
    return False

def resize_image(image_path, max_size=(416, 416)):
    with Image.open(image_path) as img:
        img.thumbnail(max_size, Image.ANTIALIAS)
        resized_path = image_path.with_name(f"resized_{image_path.name}")
        img.save(resized_path)
        return resized_path

def process_and_save_image(image_path, csv_path):
    if image_already_processed(image_path.name, csv_path):
        print(f"Pomijanie: {image_path.name} (już przetworzony)")
        return

    file_exists = Path(csv_path).is_file()
    print(image_path)
    
    resized_image_path = resize_image(image_path)
    
    prompt = '''Analyze this image and provide a detailed response in exactly this format:

**Title:** [A concise, descriptive title, max 100 characters, avoid commercial names]

**Keywords:** [List relevant keywords separated by commas, max 50 keywords]'''

    response = ollama.chat(
        model='llama3.2-vision',
        messages=[{
            'role': 'user',
            'content': prompt,
            'images': [str(resized_image_path)]
        }]
    )
    
    try:
        print(response['message']['content'])
        # Wyciągnij tytuł z sekcji **Title:**
        title = response['message']['content'].split('**Title:**')[1].split('**Keywords:**')[0].strip()        
        # Wyciągnij słowa kluczowe z sekcji **Keywords:**
        keywords = response['message']['content'].split('**Keywords:**')[1].strip()
        
        with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Filename', 'Title', 'Keywords']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow({
                'Filename': image_path.name,
                'Title': title,
                'Keywords': keywords
            })
            
        print(f"Zapisano: {image_path.name} o godzinie {datetime.now().strftime('%H:%M:%S')}")
        
    except Exception as e:
        print(f"Błąd podczas przetwarzania {image_path.name}: {str(e)}")
    finally:
        resized_image_path.unlink()  # Usuń tymczasowy przeskalowany obraz

def process_folder(input_folder, output_csv):
    counter = 0
    for image_file in Path(input_folder).glob('*'):
        if image_file.suffix.lower() in ['.png']:
            try:
                process_and_save_image(image_file, output_csv)
                counter += 1
                print(f"Przetworzono {counter} obrazów")
            except Exception as e:
                print(f"Błąd podczas przetwarzania {image_file.name}: {str(e)}")
                continue

def main():
    if len(sys.argv) != 3:
        print("Użycie: python main.py <ścieżka_do_folderu> <ścieżka_do_pliku_csv>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_csv = sys.argv[2]
    process_folder(input_folder, output_csv)

if __name__ == "__main__":
    main()