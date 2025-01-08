from flask import Flask, render_template, request, redirect, url_for, send_file
from googletrans import Translator
import csv
import os

app = Flask(__name__)
translator = Translator()

# Dictionary of supported languages in the googletrans package 
LANGUAGES = {
    'af': 'Afrikaans',
    'sq': 'Albanian',
    'am': 'Amharic',
    'ar': 'Arabic',
    'hy': 'Armenian',
    'az': 'Azerbaijani',
    'eu': 'Basque',
    'be': 'Belarusian',
    'bn': 'Bengali',
    'bs': 'Bosnian',
    'bg': 'Bulgarian',
    'ca': 'Catalan',
    'ceb': 'Cebuano',
    'ny': 'Chichewa',
    'zh-cn': 'Chinese (simplified)',
    'zh-tw': 'Chinese (traditional)',
    'co': 'Corsican',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English',
    'eo': 'Esperanto',
    'et': 'Estonian',
    'tl': 'Filipino',
    'fi': 'Finnish',
    'fr': 'French',
    'fy': 'Frisian',
    'gl': 'Galician',
    'ka': 'Georgian',
    'de': 'German',
    'el': 'Greek',
    'gu': 'Gujarati',
    'ht': 'Haitian creole',
    'ha': 'Hausa',
    'haw': 'Hawaiian',
    'iw': 'Hebrew',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'hmn': 'Hmong',
    'hu': 'Hungarian',
    'is': 'Icelandic',
    'ig': 'Igbo',
    'id': 'Indonesian',
    'ga': 'Irish',
    'it': 'Italian',
    'ja': 'Japanese',
    'jw': 'Javanese',
    'kn': 'Kannada',
    'kk': 'Kazakh',
    'km': 'Khmer',
    'ko': 'Korean',
    'ku': 'Kurdish (kurmanji)',
    'ky': 'Kyrgyz',
    'lo': 'Lao',
    'la': 'Latin',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'lb': 'Luxembourgish',
    'mk': 'Macedonian',
    'mg': 'Malagasy',
    'ms': 'Malay',
    'ml': 'Malayalam',
    'mt': 'Maltese',
    'mi': 'Maori',
    'mr': 'Marathi',
    'mn': 'Mongolian',
    'my': 'Myanmar (burmese)',
    'ne': 'Nepali',
    'no': 'Norwegian',
    'or': 'Odia',
    'ps': 'Pashto',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'pa': 'Punjabi',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sm': 'Samoan',
    'gd': 'Scots gaelic',
    'sr': 'Serbian',
    'st': 'Sesotho',
    'sn': 'Shona',
    'sd': 'Sindhi',
    'si': 'Sinhala',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'so': 'Somali',
    'es': 'Spanish',
    'su': 'Sundanese',
    'sw': 'Swahili',
    'sv': 'Swedish',
    'tg': 'Tajik',
    'ta': 'Tamil',
    'te': 'Telugu',
    'th': 'Thai',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'ug': 'Uyghur',
    'uz': 'Uzbek',
    'vi': 'Vietnamese',
    'cy': 'Welsh',
    'xh': 'Xhosa',
    'yi': 'Yiddish',
    'yo': 'Yoruba',
    'zu': 'Zulu',
}


# This route renders the main page with the form to enter words and select languages
@app.route('/')
def index():
    """
    Renders the index page with a list of supported languages.

    :return: The rendered HTML template for the main page.
    """

    return render_template('index.html', languages=LANGUAGES)


# This function saves language translations to a CSV file
def save_to_csv(translations, output_file):
    """
    Saves translations to a CSV file.

    :param translations: Dictionary of original words and their translated versions.
    :param output_file: Path of the CSV file to save translations.
    """

    print(f"save_to_csv Called with output_file: {output_file}")
    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Original', 'Translated'])
        for original, translated in translations.items():
            print(f"save_to_csv Writing to CSV: {original} -> {translated}")
            csv_writer.writerow([original, translated])
    print(f"save_to_csv Completed writing to {output_file}")


# This route translates the words entered by the user and saves the translations to a CSV file
@app.route('/translate', methods=['POST'])
def translate_words():
    """
    Handles the translation of words from the source language to the target language.

    :return: Redirects to the download page after saving translations to CSV.
    """

    words = request.form['words'].strip().split('\n') 
    source_lang = request.form['source_lang']          
    target_lang = request.form['target_lang']          

    print(f"/translate Words entered: {words}")
    print(f"/translate Source language: {source_lang}, Target language: {target_lang}")

    translations = {}
    for word in words:
        try:
            translation = translator.translate(word.strip(), src=source_lang, dest=target_lang)
            translations[word.strip()] = translation.text
            print(f"/translate Translated '{word.strip()}' -> '{translation.text}'")
        except Exception as e:
            translations[word.strip()] = "Error"
            print(f"/translate Error translating '{word.strip()}': {e}")

    output_file = 'translations.csv'
    print(f"/translate Saving translations to {output_file}")
    save_to_csv(translations, output_file)

    print(f"/translate Redirecting to download page.")
    return redirect(url_for('download_file'))


# This route allows the user to download the CSV file with translations
@app.route('/download')
def download_file():
    """
    Checks if the translations file exists and serves it for download.

    :return: The translations file for download if it exists, otherwise redirects to the index page.
    """

    file_path = 'translations.csv'
    print(f"/download Checking file existence: {file_path}")
    if os.path.exists(file_path):
        print(f"/download File exists. Preparing to send: {file_path}")
        return send_file(file_path, as_attachment=True)
    print(f"/download File not found: {file_path}")
    return redirect(url_for('index'))

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)

