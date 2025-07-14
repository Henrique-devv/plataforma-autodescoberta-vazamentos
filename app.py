from flask import Flask, render_template, request, send_file, flash, redirect, url_for 
from checker import check_vazamento
from reportlab.pdfgen import canvas
from datetime import datetime
import io
import os
import csv

app = Flask(__name__)
app.secret_key = "007"  # Necessário para usar flash()

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    dado = None
    if request.method == "POST":
        dado = request.form["input"]
        resultado = check_vazamento(dado)
    return render_template("index.html", resultado=resultado, dado=dado)

@app.route("/exportar_pdf", methods=["POST"])
def exportar_pdf():
    dado = request.form.get("input")
    if not dado:
        return "Nenhum dado fornecido para exportação", 400

    resultado = check_vazamento(dado)

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setTitle("Relatório de Vazamentos")

    pdf.drawString(100, 800, f"Relatório de Vazamentos para: {dado}")
    y = 770

    if resultado:
        for item in resultado:
            texto = f"- {item['site']} | {item['data']} | Senha: {item['senha']}"
            pdf.drawString(100, y, texto)
            y -= 20
            if y < 100:
                pdf.showPage()
                y = 800
    else:
        pdf.drawString(100, y, "Nenhum vazamento encontrado.")

    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="relatorio_vazamentos.pdf",
        mimetype="application/pdf"
    )

@app.route("/monitorar", methods=["POST"])
def monitorar():
    dado = request.form.get("input")
    if not dado:
        return "Nenhum dado fornecido", 400

    caminho = "data/monitorados.csv"
    os.makedirs("data", exist_ok=True)

    ja_cadastrado = False
    if os.path.exists(caminho):
        with open(caminho, newline='', encoding='utf-8') as f:
            leitor = csv.reader(f)
            for linha in leitor:
                if linha and linha[0] == dado:
                    ja_cadastrado = True
                    break

    if not ja_cadastrado:
        with open(caminho, "a", newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            escritor.writerow([dado, datetime.now().strftime("%Y-%m-%d")])
        mensagem = f"{dado} agora está sendo monitorado!"
    else:
        mensagem = f"{dado} já está sendo monitorado."

    flash(mensagem)
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)