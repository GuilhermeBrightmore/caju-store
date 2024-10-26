from flask import Flask, request, redirect, render_template, url_for, make_response

app = Flask(__name__)

items = {
    "1": {"Preco": 10, "Nome": "Yogurt", "MCC": "Mercado"},
    "2": {"Preco": 7, "Nome": "Coca-Cola", "MCC": "Mercado"},
    "3": {"Preco": 40, "Nome":"File a parmegiana", "MCC": "Refeicao"},
    "4": {"Preco": 5, "Nome": "Video-Game", "MCC":"Livre"}
}

conta = {
    "1": {"Nome": "Guilherme", "Senha": "cajumecontrata", "Mercado": 50, "Refeicao": 100, "Livre": 1000},
    "2": {"Nome": "Rogerio", "Senha": "cajumecontrata2", "Mercado": 40, "Refeicao": 200, "Livre": 900},
    "3": {"Nome": "Lucas Perez", "Senha": "cajumecontrata3", "Mercado": 60, "Refeicao":150, "Livre": 900}
}

transacoes = {

}

mcc_types = ['Mercado', 'Refeicao', 'Livre']

@app.route("/")
def index():
    return redirect(url_for("loja"))

@app.route("/pagamento/<accid>/<item>") # Accid = Id da conta , Item = Id do item comprado
def pagamento(accid, item):
    for mcc in mcc_types:
        if accid in conta and item in items:
            tipo = items[item]["MCC"]
            if tipo == mcc:
                if conta[accid][mcc] != None:
                    if conta[accid][mcc] < int(items[item]["Preco"]):
                        return render_template('deuruim.html')
                    else:
                        conta[accid][mcc] -= items[item]["Preco"]
                        transacoes[f"{len(transacoes) +1}"] = {"MCC": mcc, "accid" : f"{accid}", "Preco": items[item]["Preco"], "Nome": items[item]["Nome"]}
                        return render_template('pago.html')
        
        
            
@app.route("/loja", methods = ['POST', 'GET'])
def loja():
    print(request.cookies.get('accid'))
    if request.cookies.get('accid') == '' or request.cookies.get('accid') == None:
        return redirect(url_for('login'))
    else:
        accid = request.cookies.get('accid')
        return render_template('loja.html', items=items, accid=accid, contas = conta)

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['userpass']
        for usuarioid in conta:
            if conta[usuarioid]["Nome"] == username:
                if conta[usuarioid]['Senha'] == senha:
                    response = make_response(redirect(url_for("loja")))
                    response.set_cookie('username', username)
                    response.set_cookie('accid', f'{usuarioid}')
                    return response
    return render_template("login.html")

@app.route('/banco')
def banco():
    print(request.cookies.get('accid'))
    if request.cookies.get('accid') == '' or request.cookies.get('accid') == None:
        return redirect(url_for('login'))
    else:
        return render_template('banco.html',contas = conta, transacoes=transacoes, accid = request.cookies.get('accid'), items=items)
    
@app.route('/sair')
def sair():
    response = make_response(redirect(url_for("login")))
    for cookies in request.cookies:
        response.set_cookie(cookies, '', expires=0)
    return response


if __name__ == "__main__":
    app.run(debug=True)