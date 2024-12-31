from googletrans import Translator
import csv

def read_file(input_file):
    """
    Read the file and store words in a list.

    """

    with open(input_file, 'r', encoding='utf-8') as file:
        words = [line.strip() for line in file]

    print(f"{input_file} read successfully.")
    return words


def translate(words):
    """
    Translates a list of Spanish words/phrases to English using googletrans.
    Returns a dictionary with Spanish as keys and English as values.
    """
    translator = Translator()
    translations = {}

    for word in words:
        try:
            translation = translator.translate(word, src='es', dest='en')
            translations[word] = translation.text
        except Exception as e:
            print(f"Error translating '{word}': {e}")
            translations[word] = "Error"

    return translations


def save_to_csv(translations, output_file):
    """
    Saves a dictionary of translations to a CSV file.

    """
    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write the header
        csv_writer.writerow(['Spanish', 'English'])
        # Write each translation
        for spanish, english in translations.items():
            csv_writer.writerow([spanish, english])
    print(f"Translations saved to {output_file}")


def clear_csv_file(file_path):
    """
    Clears the contents of a CSV file by overwriting it with an empty header.

    """
    with open(file_path, 'w', encoding='utf-8', newline='') as csvfile:
        csvfile.truncate()  # Ensures the file is completely cleared
    print(f"The contents of the CSV file '{file_path}' have been cleared.")


def clear_txt_file(file_path):
    """
    Clears the contents of a TXT file.

    """
    with open(file_path, 'w', encoding='utf-8') as txtfile:
        txtfile.truncate()  # Ensures the file is completely cleared
    print(f"The contents of the TXT file '{file_path}' have been cleared.")


def main():
    # Define file paths
    input_file = 'vocab.txt'
    output_file = 'translations.csv'

    # Read words/phrases from the input file
    words = read_file(input_file)

    # Dummy translations for demonstration (replace with actual translation logic)
    # translations = {word: f"Translated-{word}" for word in words}

    # Translate words/phrases to English
    translations = translate(words)

    # Save translations to a CSV file
    save_to_csv(translations, output_file)


# Run the program
if __name__ == '__main__':
    main()
    #clear_csv_file('translations.csv')  
    #clear_txt_file('vocab.txt')         