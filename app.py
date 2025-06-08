from flask import Flask, render_template, request, send_file
from docxtpl import DocxTemplate
import datetime, io, os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_PLANTILLA = os.path.join(BASE_DIR, 'plantilla.docx')

@app.route('/')
def formulario():
    return render_template('index.html')

@app.route('/generar', methods=['POST'])
def generar():
    if not os.path.isfile(RUTA_PLANTILLA):
        return f"Error: No se encontró la plantilla en: {RUTA_PLANTILLA}", 500

    try:
        doc = DocxTemplate(RUTA_PLANTILLA)
    except Exception as e:
        return f"Error cargando plantilla: {str(e)}", 500

    nombre = request.form['nombre']
    cargo = request.form['cargo']
    fecha = datetime.datetime.now().strftime("%d/%m/%Y")

    context = { 'nombre': nombre, 'cargo': cargo, 'fecha': fecha }
    doc.render(context)

    output = io.BytesIO()
    doc.save(output)
    output.seek(0)

    return send_file(output, as_attachment=True, download_name="documento_generado.docx")

if __name__ == '__main__':
    app.run(debug=True)
