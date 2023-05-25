from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import io
import base64
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import numpy as np
import seaborn as sns
from collections import Counter

app = Flask(__name__)
CORS(app)

def tabla_frecuencias_Cuanti(datos):

    rango = max(datos) - min(datos)

    n = len(datos)
    num_clases = 1 + math.ceil(3.332 * math.log10(n))

    ancho_intervalo = rango / num_clases

    limites_inferiores = [min(datos) + i * ancho_intervalo for i in range(num_clases)]
    limites_superiores = [limite_inf + ancho_intervalo for limite_inf in limites_inferiores[:-1]]
    limites_superiores.append(max(datos))
    marca_clase = [(lim_inf + lim_sup) / 2 for lim_inf, lim_sup in zip(limites_inferiores, limites_superiores)]

    frecuencia_absoluta = {i: 0 for i in range(num_clases)}

    for dato in datos:
        for i in range(num_clases):
            if limites_inferiores[i] <= dato <= limites_superiores[i]:
                frecuencia_absoluta[i] += 1
                break

    frecuencia_relativa = [frec_abs / n for frec_abs in frecuencia_absoluta.values()]

    data = {
        'Intervalo': [i+1 for i in range(num_clases)],
        'Límite Inferior': limites_inferiores,
        'Límite Superior': limites_superiores,
        'Marca de Clase': marca_clase,
        'Frec. Absoluta': frecuencia_absoluta.values(),
        'Frec. Relativa': frecuencia_relativa
    }
    df = pd.DataFrame(data)
    return df

def tabla_frecuencias_Cuali(datos):
    frecuencia_absoluta = Counter(datos)

    total_datos = len(datos)
    frecuencia_relativa = [frecuencia / total_datos for frecuencia in frecuencia_absoluta.values()]

    df = pd.DataFrame({
        'Categoría': frecuencia_absoluta.keys(),
        'Frecuencia Absoluta': frecuencia_absoluta.values(),
        'Frecuencia Relativa': frecuencia_relativa
    })

    df = df.sort_values(by='Frecuencia Absoluta', ascending=False)

    df = df.reset_index(drop=True)

    return df

@app.route('/upload', methods=['POST'])
def upload_file():
    file_path = request.form.get('file_path')
    
    print(f'Ruta del archivo: {file_path}')

    extension = file_path.rsplit('.', 1)[1].lower()

    if extension == 'csv':
        df = pd.read_csv(file_path, encoding='latin-1', low_memory=False)
    elif extension == 'xlsx' or extension == 'xls':
        df = pd.read_excel(file_path, engine='openpyxl', on_bad_file='skip')
    else:
        return jsonify({'error': 'Tipo de archivo no soportado'}), 400

    columns = df.columns.tolist()
    table_html = df.to_html()

    return jsonify({'table_html': table_html, 'columns': columns})

def generate_Poligono_image(df, frecuencia, indice):
    fig = plt.figure() 
    ax = fig.add_subplot(111)

    df[0, 'Frec. Absoluta'] = 0
    df[len(df) - 1, 'Frec. Absoluta'] = 0

    plt.plot(indice, frecuencia)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close(fig)
    
    return image_base64

def generate_Histogram_image(column_name, df):
    fig = plt.figure()

    column_data = df[column_name]
    x = column_data
    
    plt.figure(figsize=(10, 6))

    plt.hist(x, bins=10) 
    plt.xlabel('Valor')
    plt.ylabel('Frecuencia')
    plt.title('Histograma de Datos Cuantitativos')

    plt.grid(True)  

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    plt.close(fig)
    
    return image_base64

def generate_ojivas_image(df):

    fig = plt.figure()
    valores = df['Marca de Clase']
    df['Frec. Relativa Acumulada'] = df['Frec. Relativa'].cumsum()
    df.at[0, 'Frec. Relativa Acumulada'] = 0
    frecuencias_relativas_acumuladas = df['Frec. Relativa Acumulada']

    plt.plot(valores, frecuencias_relativas_acumuladas, marker='o')
    plt.xlabel('Valores')
    plt.ylabel('Frecuencias relativas acumuladas')
    plt.title('Gráfica de Ojivas')
        
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    plt.close(fig)
    
    return image_base64

def grafica_barras(frecuencia, indice):

    fig, ax = plt.subplots(figsize=(22, 18))
    ax.barh(indice, frecuencia)

    ax.set_xlabel('Frecuencia')
    ax.set_ylabel('Valores')
    ax.set_title('Gráfica de barras')

    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    return image_base64

def grafica_pastel(frecuencia, indice):

    fig, ax = plt.subplots(figsize=(22, 22))
    ax.pie(frecuencia, labels=indice, autopct='%1.1f%%')

    ax.set_title('Gráfica de pastel')
    ax.axis('equal')

    buffer_pie = io.BytesIO()
    plt.savefig(buffer_pie, format='png')
    buffer_pie.seek(0)

    image_pie_base64 = base64.b64encode(buffer_pie.read()).decode('utf-8')
    return image_pie_base64

@app.route('/get_column_data', methods=['POST'])
def get_column_data():
    data = request.get_json()
    file_path = data.get('file_path')
    column_name = data.get('column_name')

    df = pd.read_csv(file_path, encoding='latin-1', low_memory=False)
    dato = df[column_name].tolist()
    if isinstance(dato[0], str):
        df_general = tabla_frecuencias_Cuali(dato)
        frecuencia = df_general['Frecuencia Absoluta']
        indice = df_general['Categoría']
        image_o_base64 = None
        image_h_base64 = None
        image_p_base64 = None
        image_base64 = grafica_barras(frecuencia, indice)
        image_pie_base64 = grafica_pastel(frecuencia, indice)
    elif isinstance(dato[0], int) or isinstance(dato[0], float):
        df_general = tabla_frecuencias_Cuanti(dato)
        frecuencia = df_general['Frec. Absoluta']
        indice = df_general['Marca de Clase']
        image_o_base64 = generate_ojivas_image(df_general)
        image_h_base64 = generate_Histogram_image(column_name, df)
        image_p_base64 = generate_Poligono_image(df_general ,frecuencia, indice)
        image_base64 = None
        image_pie_base64 = None

    return jsonify({'image1': image_base64, 'image2': image_pie_base64, 'image3': image_o_base64, 'image4': image_h_base64, 'image5':image_p_base64})

@app.route('/check_column_data', methods=['POST'])
def check_column_data():
    data = request.get_json()
    file_path = data.get('file_path')
    column_name = data.get('column_name')

    df = pd.read_csv(file_path, encoding='latin-1', low_memory=False)
    dato = df[column_name].tolist()
    print(type(dato))
    if isinstance(dato[0], str):
        df_general = tabla_frecuencias_Cuali(dato)
    elif isinstance(dato[0], int) or isinstance(dato[0], float):
        df_general = tabla_frecuencias_Cuanti(dato)

    html_table = df_general.to_html(index=False)

    return jsonify({'html_table': html_table})

if __name__ == '__main__':
    app.run()
