from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

# -----------------------------
# CONFIGURAÇÃO DO E-MAIL (GMAIL)
# -----------------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'egobebygu2@gmail.com'           # <-- SEU E-MAIL AQUI
app.config['MAIL_PASSWORD'] = 'egjl dvjp pjmn ujvt'      # <-- SENHA DE APP (não a senha normal)
app.config['MAIL_DEFAULT_SENDER'] = ('Suporte do Site', 'seuemail@gmail.com')

mail = Mail(app)


# Bibliotecas
library_bombs = {'oil': 60, 'tnt': 250, 'c4': 750, 'ciclonite': 1250}
library_base_resorces = {
    'coal': 30, 'sulfur': 20, 'iron': 20,
    'string': 2, 'oil': 5, 'chip': 2, 'energy': 2
}

def calculate_bomb_resources(bomb, value):
   
    if bomb == "oil":
        resources = {
            'coal': library_base_resorces['coal'] * 6 * value,
            'sulfur': library_base_resorces['sulfur'] * 6 * value,
            'iron': library_base_resorces['iron'] * value
        }
    elif bomb == "tnt":
        resources = {
            'coal': library_base_resorces['coal'] * 25 * value,
            'sulfur': library_base_resorces['sulfur'] * 25 * value,
            'oil': library_base_resorces['oil'] * 5 * value,
            'iron': library_base_resorces['iron'] * 25 * value,
            'string': library_base_resorces['string'] * value
        }
    elif bomb == "c4":
        resources = {
            'coal': library_base_resorces['coal'] * 75 * value,
            'sulfur': library_base_resorces['sulfur'] * 75 * value,
            'iron': library_base_resorces['iron'] * 75 * value,
            'string': library_base_resorces['string'] * value,
            'chip': library_base_resorces['chip'] * value
        }
    elif bomb == "ciclonite":
        resources = {
            'coal': library_base_resorces['coal'] * 125 * value,
            'sulfur': library_base_resorces['sulfur'] * 125 * value,
            'iron': library_base_resorces['iron'] * 125 * value,
            'string': library_base_resorces['string'] * value,
            'chip': library_base_resorces['chip'] * value,
            'energy': library_base_resorces.get('energy', 0) * value
        }
    else:
        # bomba inválida -> retorna dicionário vazio e 0 como fallback
        return {}, 0

    gunpowder = library_bombs.get(bomb, 0) * value
    return resources, gunpowder


# Rotas;

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    # CORREÇÃO: usar parênteses em get(...)
    bomb = request.form.get('bomb')
    value_raw = request.form.get('value', '0')

    # valida value
    try:
        value = int(value_raw)
        if value <= 0:
            raise ValueError("value must be > 0")
    except ValueError:
        error = "Invalid quantity. Please enter an integer greater than zero."
        return render_template('index.html', error=error, previous_bomb=bomb, previous_value=value_raw)

    # valida bomb
    if not bomb or bomb not in library_bombs:
        error = "Invalid bomb type."
        return render_template('index.html', error=error, previous_bomb=bomb, previous_value=value_raw)

    # calcula recursos (função retorna o dicionário)
    try:
        resources, gunpowder = calculate_bomb_resources(bomb, value)
    except KeyError as e:
        # caso falte alguma chave em library_base_resorces
        return render_template('index.html', error=f"Missing resource key: {e}", previous_bomb=bomb, previous_value=value_raw)

    # renderiza o resultado
    return render_template('result.html',
                           bomb=bomb,
                           value=value,
                           resources=resources,
                           gunpowder=gunpowder)




@app.route('/support', methods=['GET', 'POST'])
def support():
    if request.method == 'POST':
        nome = request.form.get('name')
        email = request.form.get('email')
        mensagem = request.form.get('message')

        msg = Message(subject=f"Mensagem de suporte de {nome}",
                      recipients=['egobebygu2@gmail.com'])  # para onde vai o e-mail
        msg.body = f"De: {nome} <{email}>\n\n{mensagem}"

        mail.send(msg)
        return render_template('support.html', success=True)

    return render_template('support.html')






if __name__ == '__main__':
    app.run(debug=True)

