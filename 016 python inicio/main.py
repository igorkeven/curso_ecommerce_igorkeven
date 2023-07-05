

from flask import Flask, render_template,request,redirect,flash,session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'igorkeven'


@app.route("/")
def index():

    return render_template('home.html')





@app.route('/loginCliente')
def loginCliente():

    return render_template('loginCliente.html')


















if __name__ in '__main__':
    app.run( debug=True )