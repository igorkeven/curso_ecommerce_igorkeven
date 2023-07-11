

from flask import Flask, render_template,request,redirect,flash,session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'igorkeven'


@app.route("/")
def index():

    return render_template('home.html')





@app.route('/loginCliente')
def loginCliente():

    return render_template('loginCliente.html')


@app.route("/acessoCliente", methods=['POST'])
def acessoCliente():
    email = request.form.get('emailCliente')
    senha = request.form.get('senhaCliente')

    if email == 'igor@igor.com' and senha == '123':
        return redirect('/cliente')
    else:
        return redirect('/loginCliente')


@app.route('/cliente')
def cliente():


    return render_template('cliente.html')













if __name__ in '__main__':
    app.run( debug=True )