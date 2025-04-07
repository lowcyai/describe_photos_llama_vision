# Analiza obrazów z Llama 3.2 Vision - automatyzacja opisów

## Wprowadzenie

Ten projekt to praktyczne narzędzie do automatycznego analizowania obrazów przy użyciu modelu Llama 3.2 Vision poprzez Ollama. Program przetwarza obrazy PNG z wskazanego folderu, generując dla każdego z nich opisowy tytuł oraz zestaw słów kluczowych, a następnie zapisuje wyniki do pliku CSV.

## Wymagania

- Python 3.6+
- Zainstalowany i skonfigurowany Ollama z modelem `llama3.2-vision`
- Biblioteki: ollama, PIL (Pillow)

## Instalacja

```bash
# Instalacja wymaganych bibliotek
pip install ollama Pillow

# Upewnij się, że masz zainstalowane Ollama z modelem llama3.2-vision
ollama pull llama3.2-vision
```

## Jak używać

Program uruchamia się z linii poleceń, podając dwa argumenty:
1. Ścieżkę do folderu zawierającego obrazy PNG do analizy
2. Ścieżkę do pliku CSV, w którym zostaną zapisane wyniki

```bash
python main.py /ścieżka/do/folderu/z/obrazami /ścieżka/do/pliku/wynikowego.csv
```

## Jak to działa

Program wykonuje następujące kroki:

1. Skanuje podany folder w poszukiwaniu plików PNG
2. Dla każdego obrazu sprawdza, czy był już wcześniej przetworzony (aby uniknąć duplikatów)
3. Przeskalowuje obraz do rozmiaru 416x416 pikseli dla optymalizacji
4. Wysyła obraz do modelu Llama 3.2 Vision z prośbą o analizę
5. Ekstrahuje tytuł i słowa kluczowe z odpowiedzi AI
6. Zapisuje wyniki do pliku CSV
7. Usuwa przeskalowany obraz tymczasowy

## Opis głównych funkcji

### `image_already_processed()`
Sprawdza, czy dany obraz był już przetworzony, zapobiegając dubletom.

### `resize_image()`
Zmniejsza rozmiar obrazu, aby przyspieszyć przesyłanie i przetwarzanie.

### `process_and_save_image()`
Główna funkcja przetwarzająca pojedynczy obraz - od przeskalowania do zapisania wyników.

### `process_folder()`
Przetwarza wszystkie obrazy PNG w danym folderze.

## Praktyczne zastosowania

- **Katalogowanie zbiorów obrazów** - szybkie tworzenie opisów i tagów dla bibliotek zdjęć
- **SEO dla stron z galeriami** - automatyczne generowanie meta-tagów i opisów
- **Porządkowanie archiwów graficznych** - klasyfikacja i kategoryzacja dużych zbiorów obrazów
- **Przygotowanie danych dla e-commerce** - generowanie opisów produktów na podstawie zdjęć

## Uwagi implementacyjne

Program jest zaprojektowany z myślą o odporności na błędy:
- Pomija już przetworzone obrazy
- Obsługuje wyjątki dla poszczególnych obrazów, kontynuując pracę
- Pokazuje informacje o postępie przetwarzania
- Automatycznie czyści pliki tymczasowe

## Podsumowanie

Ten projekt pokazuje, jak można praktycznie wykorzystać modele wizyjne AI do automatyzacji zadań związanych z opisywaniem i klasyfikacją obrazów. Dzięki prostocie implementacji i wykorzystaniu lokalnego modelu Llama 3.2 przez Ollama, możemy szybko i efektywnie generować wysokiej jakości opisy i słowa kluczowe bez konieczności ręcznego opisywania każdego obrazu.

---

*Projekt jest przykładem praktycznego zastosowania technologii AI w codziennych zadaniach związanych z przetwarzaniem danych wizualnych.*
