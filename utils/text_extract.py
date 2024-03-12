import json
from PIL import Image
import pytesseract
import os

# Função para extrair texto das coordenadas especificadas e salvar em um arquivo JSON
def extract_text_to_json(image_path, coordinates_path, output_json_path, increment=1):
    # Abrir a imagem
    image = Image.open(image_path)

    # Inicializar o Pytesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Ler as coordenadas do arquivo
    with open(coordinates_path, 'r', encoding='utf-8') as file:
        coordinates = file.readlines()

    # Extrair texto das coordenadas e armazenar em uma lista de dicionários
    extracted_text = []
    for coord in coordinates:
        data = coord.strip().split()
        label = int(data[0])
        coords = list(map(float, data[1:]))

        # Verificar se há pelo menos 5 valores para as coordenadas (incluindo o texto)
        if len(coords) >= 5:
            x, y, w, h = coords[:4]

            # Calcular as novas dimensões do box_size com incremento
            box_width = int(w * image.width + increment)
            box_height = int(h * image.height + increment)

            # Calcular coordenadas da região de interesse
            left = int((x - w / 2) * image.width)
            top = int((y - h / 2) * image.height)
            right = left + box_width
            bottom = top + box_height

            # Extrair texto da região especificada
            cropped_image = image.crop((left, top, right, bottom))
            text = pytesseract.image_to_string(cropped_image)

            # Remover quebras de linha do texto
            text = text.replace('\n', ' ')

            # Adicionar as coordenadas, o texto extraído e o tamanho da caixa à lista
            extracted_text.append({
                'coordinates': (x, y),
                'text': text.strip(),
                'box_size': (box_width, box_height)
            })

    # Salvar os dados extraídos em um arquivo JSON
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(extracted_text, json_file, indent=4, ensure_ascii=False)

    print(f"Texto extraído: {output_json_path}")

# Exemplo de uso
if __name__ == "__main__":
    # Caminho da imagem original
    image_path = 'img_or2907220633_0004.jpg'

    # Caminho do arquivo de coordenadas
    coordinates_path = 'runs/detect/predict/labels/img_or2907220633_0004.txt'

    # Caminho de saída do arquivo JSON com os dados extraídos
    output_json_path = 'json/coordinates_box_text.json'

    # Chamar a função para extrair o texto das coordenadas e salvar em um arquivo JSON
    extract_text_to_json(image_path, coordinates_path, output_json_path)
