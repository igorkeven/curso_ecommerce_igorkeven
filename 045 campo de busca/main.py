

from flask import Flask, render_template,request,redirect,flash,session,url_for
import json
import os
from datetime import date, time, datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'igorkeven'


@app.route("/")
def index():
    with open('vendedor.json') as vendedor_json:
        listaDeVendedor = json.load(vendedor_json)
    with open('clientes.json') as cliente_json:
        listaDeClientes = json.load(cliente_json)
    if 'cliente' in session:
        logado = True
        usuarioLogado = session['cliente']
    
    else:
        logado = False
        usuarioLogado = ''
    produtos_destaque = []
    for vendedor in listaDeVendedor:
        if vendedor['produtos']:
            for produto, dados in vendedor['produtos'].items():
                produtos_destaque.append(dados['quantidade_vendida'])
    quantidade_ordenada = sorted(produtos_destaque, reverse=True)
    quantidades_selecionadas = quantidade_ordenada[:3]


    return render_template('home.html',quantidades_selecionadas=quantidades_selecionadas,usuarioLogado=usuarioLogado,logado=logado, listaDeClientes=listaDeClientes, listaDeVendedor=listaDeVendedor)





@app.route('/sair')
def sair():
    session.clear()
    return redirect('/')

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
    if 'cliente' in session:
        del session['cliente']
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

# ------------------------------------------------------------------------------------------------

#--------------------- Pagina do Cliente ---------------------------------------------------------------
@app.route('/cliente')
def cliente():
    if 'cliente' in session:
        with open('vendedor.json') as vendedor_json:
            listaVendedores = json.load(vendedor_json)

        with open('clientes.json') as cliente_json:
            listaDeClientes = json.load(cliente_json)
            for usuario in listaDeClientes:
                if usuario['email'] == session['cliente']:
                    foto = usuario['foto']
                    nome = usuario['nome']
                    email = usuario['email']
                    dados_cliente = usuario
                    valor_pagar_vendedor = {}
                    for produto, dados in usuario['carrinho'].items() :
                        if dados['email_vendedor'] not in valor_pagar_vendedor:
                            valor_pagar_vendedor[dados['email_vendedor']] = dados['preco'] * dados['quantidade']
                        else:
                            valor_pagar_vendedor[dados['email_vendedor']] += dados['preco'] * dados['quantidade']




                    return render_template('cliente.html',valor_pagar_vendedor=valor_pagar_vendedor,listaVendedores=listaVendedores,dados_cliente=dados_cliente, foto=foto, nome=nome, email=email)
    else:
        flash('Necessario fazer login.')
        return redirect('/loginCliente')
# ---------------------------------------------------------------------------------------------------------------


@app.route("/vendedor")
def vendedor():
    if 'vendedor' in session:
        with open('vendedor.json') as vendedor_json:
            listaVendedores = json.load(vendedor_json)
            for vendedor in listaVendedores:
                if vendedor['email'] == session['vendedor']:
                    foto = vendedor['foto']
                    nome = vendedor['nome']
                    email = vendedor['email']
                    return render_template('vendedor.html' , foto=foto, nome=nome, email=email, produtos=vendedor['produtos'])
    else:
        flash('Necessario fazer login.')
        return redirect('/loginVendedor')



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
    


@app.route('/enviarFoto', methods=['POST'])
def enviarFoto():
    foto = request.files.get('foto')
    emailUsuario = request.form.get('emailUsuario')
    rota = request.form.get('rota')

    nome_arquivo = f"Foto_perfil_{emailUsuario}.{foto.filename.split('.')[-1] }"
    foto.save(os.path.join('static/fotoperfil', nome_arquivo))
    if rota == '/cliente':
        with open('clientes.json') as cliente_json:
            listaclientes = json.load(cliente_json)
            for cliente in listaclientes:
                if cliente['email'] == emailUsuario:
                    cliente['foto'] = nome_arquivo
                    with open('clientes.json', 'w') as novoCliente:
                        json.dump(listaclientes, novoCliente, indent=4)
    else:
        with open('vendedor.json') as vendedor_json:
            listavendedor = json.load(vendedor_json)
            for vendedor in listavendedor:
                if vendedor['email'] == emailUsuario:
                    vendedor['foto'] = nome_arquivo
                    with open('vendedor.json', 'w') as novovendedor:
                        json.dump(listavendedor, novovendedor, indent=4)
    return redirect(rota)


@app.route("/novaSenha", methods=['POST'])
def novaSenha():
    novasenha = request.form.get('novaSenha')
    emailUsuario = request.form.get('emailUsuario')

    if 'cliente' in session:
        with open('clientes.json') as cliente_json:
            listaDeClientes = json.load(cliente_json)
            for usuario in listaDeClientes:
                if usuario['email'] == emailUsuario:
                    usuario['senha'] = novasenha
        with open('clientes.json', 'w') as cliente_json:
            json.dump(listaDeClientes, cliente_json, indent=4)
        flash(f'Senha alterada com sucesso, a nova senha é {novasenha}')
        return redirect('/cliente')

    if 'vendedor' in session:
        with open('vendedor.json') as vendedor_json:
            listaDevendedor = json.load(vendedor_json)
            for usuario in listaDevendedor:
                if usuario['email'] == emailUsuario:
                    usuario['senha'] = novasenha
        with open('vendedor.json', 'w') as vendedor_json:
            json.dump(listaDevendedor, vendedor_json, indent=4)
        flash(f'Senha alterada com sucesso, a nova senha é {novasenha}')
        return redirect('/vendedor')
 
@app.route('/apagar_conta', methods=['POST'])
def apagar_conta():
    emailUsuario = request.form.get("emailUsuario")

    if 'cliente' in session:
        with open('clientes.json') as cliente_json:
            listaClientes = json.load(cliente_json)
            for cliente in listaClientes:
                if cliente['email'] == emailUsuario:
                    listaClientes.remove(cliente)
                    del session['cliente']
        with open('clientes.json', 'w') as cliente_novo:
            json.dump(listaClientes, cliente_novo, indent=4 )
    if 'vendedor' in session:
        with open('vendedor.json') as vendedor_json:
            listaVendedores = json.load(vendedor_json)
            for vendedor in listaVendedores:
                if vendedor['email'] == emailUsuario:
                    listaVendedores.remove(vendedor)
                    del session['vendedor']
        with open('vendedor.json', 'w') as vendedor_novo:
            json.dump(listaVendedores, vendedor_novo, indent=4)



    return redirect('/')


@app.route("/novo_produto", methods=['POST'])
def novo_produto():

    foto = request.files.get("foto")
    nome_produto = request.form.get("nome")
    preco = request.form.get("preco")
    descricao = request.form.get("descricao")
    emailUsuario =  request.form.get("emailUsuario")

    with open('vendedor.json') as vendedor_json:
        listaVendedores = json.load(vendedor_json)
        for vendedor in listaVendedores:
            if emailUsuario == vendedor['email']:
                nome_arquivo = f"foto_produto{vendedor['email']}_{nome_produto}.{foto.filename.split('.')[-1]}"
                foto.save(os.path.join('static/produtos', nome_arquivo))
                vendedor['produtos'][nome_produto] = {
                    "imagem": nome_arquivo,
                    "descricao": descricao,
                    "preco": float(preco),
                    "quantidade_vendida": 0
                }
    with open('vendedor.json', 'w') as vendedor_novo:
        json.dump(listaVendedores, vendedor_novo, indent=4)



    return redirect('/vendedor')




@app.route('/editar_produto', methods=['POST'])
def editar_produto():
    nome = request.form.get('editar_nome')
    preco = request.form.get('editar_preco')
    descricao = request.form.get('editar_descricao')
    emailUsuario = request.form.get('emailUsuario')
    nomeAntigo = request.form.get('nomeAntigo')

    with open('vendedor.json') as vendedor_json:
        listaVendedores = json.load(vendedor_json)
        for vendedor in listaVendedores:
            if emailUsuario == vendedor['email']:

                vendedor['produtos'][nome] = {
                    "imagem": vendedor['produtos'][nomeAntigo]['imagem'],
                    "descricao": descricao,
                    "preco": float(preco),
                    "quantidade_vendida": vendedor['produtos'][nomeAntigo]['quantidade_vendida']
                }

                if nome != nomeAntigo:
                    vendedor['produtos'].pop(nomeAntigo)

                break

    with open('vendedor.json', 'w') as vendedor_novo:
        json.dump(listaVendedores, vendedor_novo, indent=4)






    return redirect('/vendedor')


# ---------------------------------------------------------------------------------------

# ----------------------------excluir produto-----------------------------------------------------------

@app.route('/excluir_produto', methods=['POST'])
def excluir_produto():
    nomeProduto = request.form.get('nomeProduto')
    emailUsuario = request.form.get('emailUsuario')
    with open('vendedor.json') as vendedor_json:
        listaVendedores = json.load(vendedor_json)
        for vendedor in listaVendedores:
            if emailUsuario == vendedor['email']:
                imagemProduto = vendedor['produtos'][nomeProduto]['imagem']
                os.remove(os.path.join('static/produtos', imagemProduto))

                del vendedor['produtos'][nomeProduto]

    with open('vendedor.json', 'w') as vendedor_novo:
        json.dump(listaVendedores, vendedor_novo, indent=4)

    
    return redirect('/vendedor')

# ---------------------------------------------------------------------------------------




# --------------------------adicionar no carrinho-------------------------------------------------------------

@app.route('/adicionarCarrinho', methods=['POST'])
def adicionarCarrinho():
    nome_produto = request.form.get('nome_produto')
    imagem_produto = request.form.get('imagem_produto')
    preco_produto = float(request.form.get('preco_produto'))
    descricao_produto = request.form.get('descricao_produto')
    email_vendedor = request.form.get('email_vendedor')
    pagina_retorno = request.form.get('pagina_retorno')

    with open('clientes.json') as cliente_json:
        listaClientes = json.load(cliente_json)
        for cliente in listaClientes:
            if cliente['email'] == session['cliente']:
                if nome_produto in cliente['carrinho']:
                    cliente['carrinho'][nome_produto]['quantidade'] += 1
                else:
                    cliente['carrinho'][nome_produto] = {
                        "imagem": imagem_produto,
                        "descricao": descricao_produto,
                        "preco": preco_produto,
                        "email_vendedor": email_vendedor,
                        "quantidade": 1
                    }
                total_preco = sum([produto['preco'] * produto['quantidade'] for produto in cliente['carrinho'].values()])
                cliente['total_preco'] = total_preco
                with open('clientes.json', 'w') as cliente_json:
                    json.dump(listaClientes, cliente_json, indent=4)
                break



    return redirect(pagina_retorno)

# ---------------------------------------------------------------------------------------


# -----------------------remover do carrinho----------------------------------------------------------------

@app.route('/remover_carrinho' , methods=['POST'])
def remover_carrinho():
    nome_produto = request.form.get('nome_produto')
    pagina_retorno = request.form.get('pagina_retorno')
    with open('clientes.json') as cliente_json:
        listaClientes = json.load(cliente_json)
        for cliente in listaClientes:
            if cliente['email'] == session['cliente']:
                cliente['total_preco'] -= cliente['carrinho'][nome_produto]['preco']

                if cliente['carrinho'][nome_produto]['quantidade'] > 1:
                    cliente['carrinho'][nome_produto]['quantidade'] -= 1
                else:
                    del cliente['carrinho'][nome_produto]
                with open('clientes.json', 'w') as cliente_json:
                    json.dump(listaClientes, cliente_json, indent=4)
                break




    return redirect(pagina_retorno)

# ---------------------------------------------------------------------------------------

#------------- finalização de compra --------------------------------------
@app.route('/finalizar_compra', methods=['POST'])
def finalizar_compra():
    emailUsuario = request.form.get('emailUsuario')
    with open('clientes.json') as cliente_json:
        listaClientes = json.load(cliente_json)
        for cliente in listaClientes:
            if cliente['email'] == emailUsuario:
                if len(cliente['historico']) > 0:
                    novo = [{
                        "compras_finalizadas": cliente['carrinho'],
                        "compra_feita_em": datetime.today().strftime("%d-%m-%y %H:%M:%S")
                    }]
                    cliente['historico'] = novo +  cliente['historico']
                else:
                    cliente['historico'] = [{
                        "compras_finalizadas": cliente['carrinho'],
                        "compra_feita_em": datetime.today().strftime("%d-%m-%y %H:%M:%S")
                    }]
                with open('vendedor.json') as vendedor_json:
                    listaVendedores = json.load(vendedor_json)
                    for vendedor in listaVendedores:
                        for nome_produto, dados in cliente['carrinho'].items():
                            if dados['email_vendedor'] == vendedor['email']:
                                vendedor['produtos'][nome_produto]['quantidade_vendida'] += dados['quantidade']
                cliente['carrinho'] = {}
                cliente['total_preco'] = 0.0

                with open('clientes.json', 'w') as cliente_json:
                    json.dump(listaClientes, cliente_json, indent=4)
                with open('vendedor.json', 'w') as vendedor_novo:
                    json.dump(listaVendedores, vendedor_novo, indent=4)




    return redirect('/cliente')




#-----------------------------------------------------------------------------









if __name__ in '__main__':
    app.run( debug=True )