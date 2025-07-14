import csv

def check_vazamento(user_input):
    resultados = []

    with open('data/vazamentos.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if user_input.lower() in (row['email'].lower(), row['cpf']):
                resultados.append({
                    'site': row['site'],
                    'data': row['data'],
                    'senha': row['senha']
                })
    print(f"[DEBUG] Verificando: {user_input}")
    return resultados