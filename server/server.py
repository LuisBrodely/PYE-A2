import matplotlib
matplotlib.use('Agg') 
from flask import Flask, request, render_template, jsonify
import matplotlib.pyplot as plt
import math
import numpy as np
import io
import base64
import seaborn as sns
from collections import Counter
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def calculate_frequency_table(data):
    data_range = max(data) - min(data)
    n = len(data)
    num_classes = 1 + math.ceil(3.332 * math.log10(n))
    class_width = data_range / num_classes
    lower_limits = [min(data) + i * class_width for i in range(num_classes)]
    upper_limits = [lower_limit + class_width for lower_limit in lower_limits[:-1]]
    upper_limits.append(max(data))
    class_marks = [(lower_limit + upper_limit) / 2 for lower_limit, upper_limit in zip(lower_limits, upper_limits)]
    absolute_frequency = {i: 0 for i in range(num_classes)}
    for datum in data:
        for i in range(num_classes):
            if lower_limits[i] <= datum <= upper_limits[i]:
                absolute_frequency[i] += 1
                break
    relative_frequency = [abs_freq / n for abs_freq in absolute_frequency.values()]
    cumulative_absolute_frequency = np.cumsum(list(absolute_frequency.values()))
    cumulative_relative_frequency = np.cumsum(relative_frequency)
    table_data = {
        'Interval': [i+1 for i in range(num_classes)],
        'Lower Limit': lower_limits,
        'Upper Limit': upper_limits,
        'Class Mark': class_marks,
        'Absolute Frequency': absolute_frequency.values(),
        'Relative Frequency': relative_frequency,
        'Cumulative Absolute Frequency': cumulative_absolute_frequency,
        'Cumulative Relative Frequency': cumulative_relative_frequency
    }
    df = pd.DataFrame(table_data)
    return df

def calculate_frequency_table_categorical(data):
    absolute_frequency = Counter(data)

    total_data = len(data)
    relative_frequency = [frequency / total_data for frequency in absolute_frequency.values()]

    cumulative_absolute_frequency = np.cumsum(list(absolute_frequency.values()))

    cumulative_relative_frequency = np.cumsum(relative_frequency)

    df = pd.DataFrame({
        'Category': absolute_frequency.keys(),
        'Absolute Frequency': absolute_frequency.values(),
        'Relative Frequency': relative_frequency,
        'Cumulative Absolute Frequency': cumulative_absolute_frequency,
        'Cumulative Relative Frequency': cumulative_relative_frequency
    })

    df = df.sort_values(by='Absolute Frequency', ascending=False)

    df = df.reset_index(drop=True)

    return df

@app.route('/upload', methods=['POST'])
def upload_file():
    file_path = request.form.get('file_path')

    print(f'Ruta del archivo: {file_path}')

    extension = file_path.rsplit('.', 1)[1].lower()

    if extension == 'csv':
        df = pd.read_csv(file_path, encoding='latin-1', low_memory=False)
        df = df.head(100)

    elif extension == 'xlsx' or extension == 'xls':
        df = pd.read_excel(file_path, engine='openpyxl', on_bad_file='skip')

    else:
        return jsonify({'error': 'Tipo de archivo no soportado'}), 400

    columns = df.columns.tolist()
    table_html = df.to_html()

    return jsonify({'table_html': table_html, 'columns': columns})

def generate_polygon_image(df, frequency, index):
    fig = plt.figure()
    df.at[0, 'Absolute Frequency'] = 0
    df.at[len(df) - 1, 'Absolute Frequency'] = 0
    plt.plot(index, frequency)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close(fig)

    return image_base64


def media_aritmetica(columna):
    suma = sum(columna)
    media = suma / len(columna)
    return media
def media_recortada(datos, porcentaje_recorte):
    datos_ordenados = sorted(datos)
    cantidad_recorte = int(len(datos) * porcentaje_recorte / 100 / 2)
    datos_recortados = datos_ordenados[cantidad_recorte:-cantidad_recorte]
    media_recortada = sum(datos_recortados) / len(datos_recortados)
    return media_recortada

def medinana(datos):
    datos_ordenados = sorted(datos)
    n = len(datos_ordenados)
    if n % 2 == 1:
        mediana = datos_ordenados[n // 2]
    else:
        mediana = (datos_ordenados[n // 2 - 1] + datos_ordenados[n // 2]) / 2
    return mediana

def moda(datos):
    conteo = Counter(datos)
    moda = max(conteo, key=conteo.get)
    frecuencia_moda = conteo[moda]
    
    modas = [valor for valor, frecuencia in conteo.items() if frecuencia == frecuencia_moda]
    
    if len(modas) == len(conteo):
        return "No hay moda"
    else:
        return modas
def rango(datos):
    valor_maximo = max(datos)
    valor_minimo = min(datos)
    rango = valor_maximo - valor_minimo
    return rango

def Varianza(datos):
    media = sum(datos) / len(datos)
    diferencias_cuadrado = [(x - media) ** 2 for x in datos]
    varianza = sum(diferencias_cuadrado) / len(datos)
    return varianza

def Desviacion_Estandar(datos):    
    varianza = Varianza(datos)  
    desviacion_estandar = math.sqrt(varianza)
    return desviacion_estandar

def calcular_sesgo(datos):
    n = len(datos)
    media = sum(datos) / n
    desviacion_estandar = math.sqrt(sum((x - media) ** 2 for x in datos) / n)
    tercer_momento_central = sum((x - media) ** 3 for x in datos) / n
    sesgo = tercer_momento_central / (desviacion_estandar ** 3)
    return sesgo

@app.route('/get_stats', methods=['POST'])
def obtener_estadisticas():
    data = request.get_json()
    file_path = data.get('file_path')
    column_name = data.get('column_name')

    df = pd.read_csv(file_path, encoding='latin-1', low_memory=False)
    datos = df[column_name].tolist()
    valor_maximo = max(datos)
    valor_minimo = min(datos)

    if isinstance(datos[0], str):
            resultados = {
                'Moda': moda(datos),
             }
    elif isinstance(datos[0], int) or isinstance(datos[0], float):
            resultados = {
                'Mediana': medinana(datos),
                'Moda': moda(datos),
                'Rango': rango(datos),
                'Varianza': Varianza(datos),
                'Desviación Estándar': Desviacion_Estandar(datos),
                'Minimo': valor_minimo,
                'Maximo': valor_maximo,
                'Sesgo': calcular_sesgo(datos)
            }
    
    df = pd.DataFrame(resultados, index=[0])
    html_table = df.to_html(index=False)

    return jsonify({'html_table': html_table})

@app.route('/get_medianas', methods=['POST'])
def obtener_medianas():
    data = request.get_json()
    file_path = data.get('file_path')
    column_name = data.get('column_name')
    porcentaje = data.get('porcentaje')

    df = pd.read_csv(file_path, encoding='latin-1', low_memory=False)
    datos = df[column_name].tolist()

    if isinstance(datos[0], str):
            resultados = {
             }
    elif isinstance(datos[0], int) or isinstance(datos[0], float):
            resultados = {
                'Media_aritmetica': media_aritmetica(datos),
                'Media_Recortada': media_recortada(datos, porcentaje),
            }

    
    df = pd.DataFrame(resultados, index=[0])
    html_table = df.to_html(index=False)

    return jsonify({'html_table': html_table})

def generate_histogram_image(column_name, df):
    fig = plt.figure()
    column_data = df[column_name]
    x = column_data

    plt.figure(figsize=(10, 6))
    plt.hist(x, bins=10)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram of Quantitative Data')
    plt.grid(True)

    buffer = io.BytesIO()

    plt.savefig(buffer, format='png')

    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    plt.close(fig)

    return image_base64

def generate_cumulative_frequency_plot(df):
    fig = plt.figure()
    values = df['Class Mark']
    df['Cumulative Relative Frequency'] = df['Relative Frequency'].cumsum()
    df.at[0, 'Cumulative Relative Frequency'] = 0  
    cumulative_frequencies = df['Cumulative Relative Frequency']
    plt.plot(values, cumulative_frequencies, marker='o')
    plt.xlabel('Values')
    plt.ylabel('Cumulative Relative Frequencies')
    plt.title('Cumulative Frequency Plot')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close(fig)

    return image_base64

def generate_bar_graph(data, labels):
    fig, ax = plt.subplots(figsize=(22, 18))
    ax.barh(labels, data)

    ax.set_xlabel('Frequency')
    ax.set_ylabel('Values')
    ax.set_title('Bar Graph')

    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    return image_base64


def generate_pie_chart(data, labels):
    fig, ax = plt.subplots(figsize=(22, 22))
    ax.pie(data, labels=labels, autopct='%1.1f%%')
    ax.set_title('Pie Chart')
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
        df_general = calculate_frequency_table_categorical(dato)
        frecuencia = df_general['Absolute Frequency']
        indice = df_general['Category']
        image_o_base64 = None
        image_h_base64 = None
        image_p_base64 = None
        image_base64 = generate_bar_graph(frecuencia, indice)
        image_pie_base64 = generate_pie_chart(frecuencia, indice)
    elif isinstance(dato[0], int) or isinstance(dato[0], float):
        df_general = calculate_frequency_table(dato)
        frecuencia = df_general['Absolute Frequency']
        indice = df_general['Class Mark']
        image_o_base64 = generate_cumulative_frequency_plot(df_general)
        image_h_base64 = generate_histogram_image(column_name, df)
        image_p_base64 = generate_polygon_image(df_general ,frecuencia, indice)
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
    if isinstance(dato[0], str):
        df_general = calculate_frequency_table_categorical(dato)
    elif isinstance(dato[0], int) or isinstance(dato[0], float):
        df_general = calculate_frequency_table(dato)

    html_table = df_general.to_html(index=False)

    return jsonify({'html_table': html_table})

if __name__ == '__main__':
    app.run()
