from flask import Flask, render_template, request, redirect, url_for, session
import os
from collections import Counter
import matplotlib.pyplot as plt

# Configuración inicial
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'una_clave_secreta_segura'  # Necesario para usar session

# Ruta principal
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        texto = request.form.get('texto_manual')
        archivo = request.files.get('archivo_txt')

        if texto:
            session['texto'] = texto  # Guardamos el texto en sesión
            return redirect(url_for('resultado_texto'))
        elif archivo:
            ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], archivo.filename)
            archivo.save(ruta_archivo)
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            session['texto'] = contenido
            return redirect(url_for('resultado_texto'))
        else:
            return render_template('index.html', mensaje="Por favor, sube un archivo o pega un texto.")

    return render_template('index.html')

# Ruta para mostrar resultados
@app.route('/resultado', methods=['GET'])
def resultado_texto():
    texto = session.get('texto', '')

    # Procesar el texto
    palabras = texto.lower().split()
    palabras_limpias = [p.strip('.,¡!¿?()[]{}:;\"\'') for p in palabras if p.strip('.,¡!¿?()[]{}:;\"\'')]

    cantidad_palabras = len(palabras_limpias)
    contador = Counter(palabras_limpias)
    palabras_mas_comunes = contador.most_common(10)

    # Crear gráfico
    if palabras_mas_comunes:
        palabras, frecuencias = zip(*palabras_mas_comunes)

        plt.figure(figsize=(10,5))
        plt.bar(palabras, frecuencias, color='skyblue')
        plt.title('Top 10 palabras más frecuentes')
        plt.xlabel('Palabras')
        plt.ylabel('Frecuencia')
        plt.xticks(rotation=45)
        plt.tight_layout()

        ruta_grafico = os.path.join('static/images', 'grafico.png')
        plt.savefig(ruta_grafico)
        plt.close()
    else:
        ruta_grafico = None

    return render_template('result.html',
                           total_palabras=cantidad_palabras,
                           texto=texto,
                           palabras_frecuencias=palabras_mas_comunes,
                           grafico_url=ruta_grafico)

# Ejecutar la aplicación
if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
