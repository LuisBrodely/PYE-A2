from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import io
import base64
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Configurar el backend no interactivo antes de importar pyplot
import matplotlib.pyplot as plt
import math
import numpy as np
import seaborn as sns

app = Flask(__name__)
CORS(app)

class Calculos:

    rangoMayor = 0
    rangoMenor = 0
    rango = 0
    numClass = 0.0
    widthClass = 0
    classMark = 0
    frecAbs = 0
    freRel = 0

    list_numClass = []
    list_limtMayor = []
    list_limtMenor = []
    list_widthClass = []
    list_classMark = []
    list_frecAbs = []
    list_freRel = []
    list_rango = []
    
    def createClassID_ESTADO_MUNICIPIO_RESPONSABLE(self , array, df, colum_name):

        self.rangoMayor = df[colum_name].max()
        self.rangoMenor = df[colum_name].min()
        self.rango = self.rangoMayor - self.rangoMenor
        self.numClass = int(1 + (3.3 * math.log10(len(array))))
        self.widthClass = (round(self.rango / self.numClass))
        limiteMenor = self.rangoMenor

        for i in range(self.numClass):

            limiteMayor = limiteMenor + self.widthClass
            self.list_limtMenor.append(limiteMenor)
            self.list_limtMayor.append(limiteMayor)
            marca = 0.0
            marca = (limiteMenor + limiteMayor)/2
            self.list_classMark.append(marca)
            for y in range(len(array)):
                arraytotal = array[y]
                #self.frecAbs = df.loc[(df.Peso_Kg >= limiteMenor) & (df.Peso_Kg <= limiteMayor)  ].agg(frecuency= ("Peso_Kg" , "count"))
                if (arraytotal >= limiteMenor and arraytotal <= limiteMayor): 
                    self.frecAbs = self.frecAbs + 1
                    self.freRel = (self.frecAbs * 100) /len(array)

            self.list_frecAbs.append(self.frecAbs)

            self.list_freRel.append(round(self.freRel,2))
            self.frecAbs = 0
            self.freRel = 0 
            limiteMenor = limiteMayor

        Lim_Menor=pd.DataFrame(self.list_limtMenor,columns=['Lim Menor'])
        Lim_Mayor=pd.DataFrame(self.list_limtMayor,columns=['Lim Mayor'])
        Marca_clases=pd.DataFrame(self.list_classMark,columns=['Marca de clase'])
        frecuencia_Absoluta=pd.DataFrame(self.list_frecAbs,columns=['Frec Absoluta'])
        frecuencia_Relativa=pd.DataFrame(self.list_freRel,columns=['Frec Relativa'])

        global DFgeneral
        DFgeneral = None
        DFgeneral=pd.concat([Lim_Menor,Lim_Mayor,Marca_clases,frecuencia_Absoluta,frecuencia_Relativa],axis=1)
        return DFgeneral

@app.route('/upload', methods=['POST'])
def upload_file():
    file_path = request.form.get('file_path')
    # Utiliza la variable 'file_path' para realizar las operaciones necesarias
    # con la ruta del archivo

    # Por ejemplo, puedes imprimir la ruta del archivo
    print(f'Ruta del archivo: {file_path}')
    # Aquí puedes utilizar la ruta del archivo para abrirlo o realizar otras operaciones
    # Por ejemplo, leer el archivo con pandas y generar la tabla HTML

    # Obtener la extensión del archivo
    extension = file_path.rsplit('.', 1)[1].lower()

    if extension == 'csv':
        # Leer archivo CSV con pandas
        df = pd.read_csv(file_path, encoding='latin-1', low_memory=False)
    elif extension == 'xlsx' or extension == 'xls':
        # Leer archivo XLSX o XLS con pandas
        df = pd.read_excel(file_path, engine='openpyxl', on_bad_file='skip')
    else:
        return jsonify({'error': 'Tipo de archivo no soportado'}), 400

    # Generar representación HTML de la tabla
    table_html = df.to_html()

    # Retornar la tabla HTML y la ruta del archivo al cliente
    return jsonify({'table_html': table_html, 'file_path': file_path})

def generate_Poligono_image(df, column_name):
    column_data = df[column_name]
    x = column_data

    fig = plt.figure() 
    ax = sns.kdeplot(column_data)

    # Establecer los límites del eje y y x en 0
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)

    # Guardar la gráfica como imagen en un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convertir la gráfica a base64
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    plt.close(fig)
    
    # Retornar la imagen en formato base64
    return image_base64

def generate_Histogram_image(column_name, df):
    fig = plt.figure()

    column_data = df[column_name]
    x = column_data
    
    plt.figure(figsize=(10, 6))  # Opcional: ajusta el tamaño de la figura

    # Si son cuantitativos
    plt.hist(x, bins=10)  # Opcional: ajusta el número de bins
    plt.xlabel('Valor')
    plt.ylabel('Frecuencia')
    plt.title('Histograma de Datos Cuantitativos')

    plt.grid(True)  # Opcional: añade una cuadrícula al gráfico

    # Guardar la gráfica como imagen en un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convertir la gráfica a base64
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    plt.close(fig)
    
    # Retornar la imagen en formato base64
    return image_base64



def generate_ojivas_image(column_data):
    fig = plt.figure()

    value_counts = pd.Series(column_data).value_counts()
    y_acumulativo = np.cumsum(value_counts)
    plt.plot(y_acumulativo.index, y_acumulativo, marker='o')
    plt.title('Gráfica de Ojivas')
    plt.xlabel('Datos')
    plt.ylabel('Porcentaje acumulativo')
    plt.grid(True)
        
    
    # Guardar la gráfica como imagen en un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    # Convertir la gráfica a base64
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    plt.close(fig)
    
    # Retornar la imagen en formato base64
    return image_base64


@app.route('/get_column_data', methods=['POST'])
def get_column_data():
    data = request.get_json()
    file_path = data.get('file_path')
    column_name = data.get('column_name')

    # Leer el archivo con pandas
    df = pd.read_csv(file_path, encoding='latin-1', low_memory=False)

    # Obtener los datos de la columna
    column_data = df[column_name].tolist()
    image_o_base64 = generate_ojivas_image(column_data)
    try:
        image_h_base64 = generate_Histogram_image(column_name, df)

        image_p_base64 = generate_Poligono_image(df, column_name)
    except:
        image_p_base64 = None
        image_h_base64 = None
        pass

    # Contar la frecuencia de cada valor en la columna
    value_counts = pd.Series(column_data).value_counts()

    # Crear la gráfica de barras
    fig, ax = plt.subplots(figsize=(22, 18))
    ax.barh(value_counts.index, value_counts.values)

    # Personalizar la gráfica
    ax.set_xlabel('Frecuencia')
    ax.set_ylabel('Valores')
    ax.set_title('Gráfica de barras')

    # Ajustar el espaciado entre las barras
    plt.tight_layout()

    # Convertir la gráfica en una imagen
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convertir la gráfica a base64
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    
    # Crear la gráfica de pastel
    fig, ax = plt.subplots(figsize=(22, 22))
    ax.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')

    # Personalizar la gráfica de pastel
    ax.set_title('Gráfica de pastel')
    ax.axis('equal')

    # Convertir la gráfica de pastel en una imagen
    buffer_pie = io.BytesIO()
    plt.savefig(buffer_pie, format='png')
    buffer_pie.seek(0)

    # Convertir la gráfica de pastel a base64
    image_pie_base64 = base64.b64encode(buffer_pie.read()).decode('utf-8')

    # Retornar la imagen como respuesta en formato JSON
    return jsonify({'image1': image_base64, 'image2': image_pie_base64, 'image3': image_o_base64, 'image4': image_h_base64, 'image5':image_p_base64})

@app.route('/check_column_data', methods=['POST'])
def check_column_data():
    data = request.get_json()
    file_path = data.get('file_path')
    column_name = data.get('column_name')

    # Leer el archivo con pandas
    df = pd.read_csv(file_path, encoding='latin-1', low_memory=False)

    # Obtener los datos de la columna
    column_data = df[column_name].astype(float).tolist()
    array = np.array(df[column_name].sort_values())

    calculos = Calculos()

    df_general = calculos.createClassID_ESTADO_MUNICIPIO_RESPONSABLE(column_data, df, column_name)

    # Convertir el DataFrame a una tabla HTML
    html_table = df_general.to_html(index=False)

    # Retornar la tabla HTML al cliente como respuesta en formato JSON
    return jsonify({'html_table': html_table})

if __name__ == '__main__':
    app.run()

