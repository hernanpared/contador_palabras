from flask import Flask, render_template, request, redirect, url_for
import os

# Configurar la aplicación
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ruta principal - Formulario para subir texto o archivo
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Opción 1: Usuario pega texto manualmente
        texto = request.form.get('texto_manual')

        # Opción 2: Usuario sube un archivo
        archivo = request.files.get('archivo_txt')

        if texto:
            return redirect(url_for('resultado_texto', texto=texto))
        elif archivo:
            ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], archivo.filename)
            archivo.save(ruta_archivo)
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            return redirect(url_for('resultado_texto', texto=contenido))
        else:
            return render_template('index.html', mensaje="Por favor, sube un archivo o pega un texto.")

    return render_template('index.html')

# Ruta para mostrar resultados
@app.route('/resultado')
def resultado_texto():
    texto = request.args.get('texto', '')

    # Procesar el texto
    palabras = texto.split()
    cantidad_palabras = len(palabras)

    return render_template('result.html', total_palabras=cantidad_palabras, texto=texto)

# Ejecutar la app
if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
