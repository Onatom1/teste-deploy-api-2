from deep_translator import GoogleTranslator
import json

def translate_json(json_file_path, source_language='en', target_language='pt'):
    # Carrega o arquivo JSON
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Cria um tradutor
    translator = GoogleTranslator(source=source_language, target=target_language)

    # Itera sobre os itens do JSON
    for item in data:
        # Traduz o texto
        translated_text = translator.translate(item['text'])

        # Substitui o texto original pelo texto traduzido
        item['text'] = translated_text

    # Salva as alterações de volta no arquivo JSON
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# Exemplo de uso da função
if __name__ == "__main__":
    json_file_path = 'json/coordinates_box_text.json'
    translate_json(json_file_path)
