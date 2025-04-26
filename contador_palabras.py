# contador_palabras.py

def contar_palabras(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
            palabras = contenido.split()
            total_palabras = len(palabras)

            contador = {}
            for palabra in palabras:
                palabra = palabra.lower().strip('.,¡!¿?()[]{}:;')  # Limpieza básica
                if palabra:
                    contador[palabra] = contador.get(palabra, 0) + 1

            print(f"Total de palabras: {total_palabras}")
            print("\nFrecuencia de palabras:")
            for palabra, cantidad in sorted(contador.items(), key=lambda x: x[1], reverse=True):
                print(f"{palabra}: {cantidad}")

    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no se encontró.")

if __name__ == "__main__":
    archivo = input("Introduce el nombre del archivo .txt: ")
    contar_palabras(archivo)
