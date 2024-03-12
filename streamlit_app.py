import streamlit as st
from utils.manga_coordinates_balloon import detect_and_save_balloons
from utils.text_extract import extract_text_to_json
from utils.inserir_imagem import insert_text_on_image
from utils.translator import translate_json
import os
import shutil

# Configurações para o upload de arquivos
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# Verificar se a extensão do arquivo é permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def main():
    st.title('Processamento de Imagem com Streamlit')

    uploaded_file = st.file_uploader("Faça o upload da sua imagem", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        if allowed_file(uploaded_file.name):
            # Salvar o arquivo enviado
            with open(os.path.join(UPLOAD_FOLDER, uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Caminho do arquivo enviado
            filepath = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

            # Caminho para salvar os resultados
            save_path = 'runs/detect'

            # Verificar se a pasta de saída existe e removê-la
            predict_path = os.path.join(save_path, 'predict')
            if os.path.exists(predict_path):
                shutil.rmtree(predict_path)

            # Chamar a função para detectar e salvar balões
            detect_and_save_balloons(filepath, save_path)

            # Caminho do arquivo de coordenadas
            coordinates_path = os.path.join(save_path, 'predict', 'labels', os.path.splitext(uploaded_file.name)[0] + '.txt')

            # Caminho de saída do arquivo JSON com os dados extraídos
            output_json_path = os.path.join('json', 'coordinates_box_text.json')

            # Chamar a função para extrair o texto das coordenadas e salvar em um arquivo JSON
            extract_text_to_json(filepath, coordinates_path, output_json_path)
            
            json_file_path = 'json/coordinates_box_text.json'
            translate_json(json_file_path)

            # Gerar o nome do arquivo de imagem combinada
            combined_image_path = filepath

            # Chamar a função para inserir o texto na imagem
            insert_text_on_image(filepath, output_json_path, combined_image_path)

            # Exibir a imagem processada
            st.image(combined_image_path, caption='Imagem Processada', use_column_width=True)
        else:
            st.error("Formato de arquivo não suportado. Por favor, envie um arquivo JPG, JPEG ou PNG.")

if __name__ == "__main__":
    main()
