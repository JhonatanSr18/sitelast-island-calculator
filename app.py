from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

# -----------------------------
# CONFIGURAÇÃO DE EMAIL (GMAIL)
# -----------------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'egobebygu2@gmail.com'
app.config['MAIL_PASSWORD'] = 'egjl dvjp pjmn ujvt'   # senha de app
app.config['MAIL_DEFAULT_SENDER'] = ('Last Island Support', 'egobebygu2@gmail.com')

mail = Mail(app)

# -----------------------------
# BIBLIOTECAS DE ITENS
# -----------------------------
library_bombs = {'oil': 60, 'tnt': 250, 'c4': 750, 'ciclonite': 1250}

library_base_resorces = {
    'coal': 30,
    'sulfur': 20,
    'iron': 20,
    'string': 2,
    'oil': 5,
    'chip': 2,
    'energy': 2
}


def calculate_bomb_resources(bomb, value):

    if bomb == "oil":
        resources = {
            'coal': library_base_resorces['coal'] * 6 * value,
            'sulfur': library_base_resorces['sulfur'] * 6 * value,
            'iron': library_base_resorces['iron'] * value,
        }

    elif bomb == "tnt":
        resources = {
            'coal': library_base_resorces['coal'] * 25 * value,
            'sulfur': library_base_resorces['sulfur'] * 25 * value,
            'oil': library_base_resorces['oil'] * 5 * value,
            'iron': library_base_resorces['iron'] * 25 * value,
            'string': library_base_resorces['string'] * value,
        }

    elif bomb == "c4":
        resources = {
            'coal': library_base_resorces['coal'] * 75 * value,
            'sulfur': library_base_resorces['sulfur'] * 75 * value,
            'iron': library_base_resorces['iron'] * 75 * value,
            'string': library_base_resorces['string'] * value,
            'chip': library_base_resorces['chip'] * value,
        }

    elif bomb == "ciclonite":
        resources = {
            'coal': library_base_resorces['coal'] * 125 * value,
            'sulfur': library_base_resorces['sulfur'] * 125 * value,
            'iron': library_base_resorces['iron'] * 125 * value,
            'string': library_base_resorces['string'] * value,
            'chip': library_base_resorces['chip'] * value,
            'energy': library_base_resorces['energy'] * value,
        }

    else:
        return {}, 0

    gunpowder = library_bombs.get(bomb, 0) * value
    return resources, gunpowder


# -----------------------------
# ROTAS CORRETAS DO SITE
# -----------------------------

# 1) PÁGINA INICIAL = ABOUT US
@app.route('/')
def about():
    return render_template('about.html')


# 2) PÁGINA PRINCIPAL (CALCULADORA)
@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html')


# 3) PROCESSA O CÁLCULO
@app.route('/calculate', methods=['POST'])
def calculate():
    bomb = request.form.get('bomb')
    value_raw = request.form.get('value', '0')

    # valida quantidade
    try:
        value = int(value_raw)
        if value <= 0:
            raise ValueError()
    except:
        return render_template(
            'main.html',
            error="Invalid quantity.",
            previous_bomb=bomb,
            previous_value=value_raw
        )

    # valida bomb
    if bomb not in library_bombs:
        return render_template(
            'main.html',
            error="Invalid bomb type.",
            previous_bomb=bomb,
            previous_value=value_raw
        )

    # calcula recursos
    resources, gunpowder = calculate_bomb_resources(bomb, value)

    return render_template(
        'result.html',
        bomb=bomb,
        value=value,
        resources=resources,
        gunpowder=gunpowder
    )


# 4) SUPORTE
@app.route('/support', methods=['GET', 'POST'])
def support():

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        msg = Message(
            subject=f"Mensagem de suporte de {name}",
            recipients=['egobebygu2@gmail.com']
        )
        msg.body = f"De: {name} <{email}>\n\n{message}"

        mail.send(msg)

        return render_template('support.html', success=True)

    return render_template('support.html')


# 5) DOAÇÃO
@app.route('/donation')
def donation():
    return render_template('donation.html')


# -----------------------------
# RUN
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)