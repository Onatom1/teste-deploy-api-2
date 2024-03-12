from PIL import Image, ImageDraw, ImageFont
import json
import textwrap

def insert_text_on_image(image_path, json_path, save_path):
    # Carregar a imagem original
    original_image = Image.open(image_path)

    # Carregar o arquivo JSON com as coordenadas, o texto e o tamanho da caixa
    with open(json_path, 'r', encoding='utf-8') as json_file:
        extracted_data = json.load(json_file)

    # Definir o tamanho da fonte
    tamanho_fonte = 18

    # Para cada texto extraído, criar uma caixa em branco com o texto
    for item in extracted_data:
        text = item['text']
        coordinates = item['coordinates']
        box_size = item['box_size']
        x, y = coordinates
        box_width, box_height = box_size

        # Escolher a fonte e o tamanho da fonte
        font = ImageFont.truetype("fonts/ComicNeue-Bold.ttf", tamanho_fonte)

        # Criar uma nova imagem com a caixa em branco e o texto
        text_image = Image.new('RGBA', (box_width, box_height), (255, 255, 255, 255))
        draw_text = ImageDraw.Draw(text_image)

        # Quebrar o texto em linhas
        lines = textwrap.wrap(text, width=15)  # Defina o comprimento máximo da linha conforme necessário

        # Calcular o tamanho total do texto e o espaço entre as linhas
        text_bbox = [draw_text.textbbox((0, 0), line, font=font) for line in lines]
        text_height = sum(box[3] - box[1] for box in text_bbox)
        line_spacing = 5

        # Verificar se o texto cabe na caixa
        if text_height + (len(lines) - 1) * line_spacing <= box_height:
            # Calcular a posição vertical inicial do texto para centralizá-lo na caixa
            y_text = (box_height - text_height - (len(lines) - 1) * line_spacing) / 2

            # Desenhar o texto na imagem
            for box, line in zip(text_bbox, lines):
                width = box[2] - box[0]
                x_text = (box_width - width) / 2
                draw_text.text((x_text, y_text), line, fill='black', font=font)
                y_text += box[3] - box[1] + line_spacing

            # Colocar a imagem do texto sobre a imagem original
            x_pos = int(x * original_image.width) - int(box_width / 2)
            y_pos = int(y * original_image.height) - int(box_height / 2)
            original_image.paste(text_image, (x_pos, y_pos), text_image)

    # Salvar a imagem combinada
    original_image.save(save_path)

# Exemplo de uso da função
if __name__ == "__main__":
    insert_text_on_image('img_or2907220633_0004.jpg', 'json/texto_extraido.json', 'combined_image.png')
