

from flask import Flask, render_template,request,redirect,flash,session
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'igorkeven'


@app.route("/")
def index():

    return render_template('home.html')


@app.route('/loginVendedor')
def loginVendedor():

    return render_template('loginVendedor.html')

@app.route("/acessoVendedor" , methods=['POST'])
def acessoVendedor():
    email = request.form.get('emailvendedor')
    senha = request.form.get('senhavendedor')
    with open('vendedor.json') as vendedor_json:
        listaDeVendedor = json.load(vendedor_json)
        cont = 0
        for usuario in listaDeVendedor:
            cont += 1 
            
            if email == usuario['email']   and senha == usuario['senha'] :
                session['vendedor'] = email
                if 'cliente' in session:
                    del session['cliente']
                return redirect('/vendedor')
            if cont >= len(listaDeVendedor):
                flash('Email ou senha incorretos.')
                return redirect('/loginVendedor')




@app.route('/loginCliente')
def loginCliente():

    return render_template('loginCliente.html')


@app.route("/acessoCliente", methods=['POST'])
def acessoCliente():
    email = request.form.get('emailCliente')
    senha = request.form.get('senhaCliente')
    with open('clientes.json') as cliente_json:
        listaDeClientes = json.load(cliente_json)
        cont = 0
        for usuario in listaDeClientes:
            cont += 1 
            
            if email == usuario['email']   and senha == usuario['senha'] :
                session['cliente'] = email
                if 'vendedor' in session:
                    del session['vendedor']
                return redirect('/cliente')
            if cont >= len(listaDeClientes):
                flash('Email ou senha incorretos.')
                return redirect('/loginCliente')


@app.route('/cliente')
def cliente():
    return render_template('cliente.html')

@app.route("/vendedor")
def vendedor():
    return render_template('vendedor.html')

@app.route('/cadastrar')
def cadastrar():

    return render_template('cadastro.html')


@app.route('/cadastroCliente', methods=['POST'])
def cadastroCliente():
    email = request.form.get('emailclienter')
    nome  = request.form.get('nomecliente')
    senha  = request.form.get('senhacliente')

    with open('clientes.json') as cliente_json:
        listaDeClientes = json.load(cliente_json)
        for usuario in listaDeClientes:
            if usuario['email'] == email:
                flash('Email já cadastrado no banco de dados, se esqueceu sua senha clique em "esqueci minha senha".')
                return redirect('/loginCliente')
    user = [
        {
            "nome": nome,
            "email": email,
            "senha": senha,
            "foto": "",
            "carrinho": {},
            "total_preco": 0.0,
            "historico": {}

        }
    ]

    novalista = listaDeClientes + user

    with open('clientes.json', 'w') as cliente_json:
        json.dump(novalista, cliente_json, indent=4)


    flash(f'{nome} cadastrado com sucesso!! BOAS COMPRAS!')
    return redirect('/loginCliente')


@app.route('/cadastroVendedor' , methods=['POST'])
def cadastroVendedor():
    email = request.form.get('emailVendedor')
    nome = request.form.get('nomeVendedor')
    senha = request.form.get('pixVendedor')
    chavePIX = request.form.get('senhaVendedor')


    with open('vendedor.json') as vendedores:
        listaVendedores = json.load(vendedores)
        for vendedor in listaVendedores:
            if vendedor['email'] == email:
                flash('usuario ja cadastrado, tente fazer login ou clique em esqueci minha senha. ')
                return redirect('/loginVendedor')
    user = [
        {
            "email":email,
            "nome": nome,
            "senha":senha,
            "chavePIX":chavePIX,
            "foto":"",
            "produtos":{}
        }
    ]

    novalista = listaVendedores + user
    

    with open('vendedor.json', 'w') as vendedores_json:
        json.dump(novalista, vendedores_json , indent=4 )

    flash(f'{nome} cadastrado com sucesso!! BOAS VENDAS!')
    return redirect('/loginVendedor')
    





if __name__ in '__main__':
    app.run( debug=True )