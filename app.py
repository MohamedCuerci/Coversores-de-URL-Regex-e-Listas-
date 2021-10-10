import db
from flask import Flask, abort
from converters import RegexConverter, ListConvert

app = Flask(__name__)
#o nome usado entre [] é o msm usado antes dos items
#q no caso é <regex("a.*"):name>
app.url_map.converters['regex'] = RegexConverter

app.url_map.converters['list'] = ListConvert



@app.route('/')
def index():
    html = ['<ul>']
    for username, user in db.users.item():
        html.append(
            f"<il><a href='/user/{username}'>{user['name']}</a></li>"
        )
    html.append('</ul>')
    return '/n'.join(html)

@app.route('/user/<list:usernames>/', endpoint='user')
def profile(usernames):
    html = ''
    #set é um conjunto que não permite duplicidade
    for username in set(usernames):
        user = db.users.get(username, {})

        if user:
            html += f'''
                <h1>{user['name']}</h1>
                <img src="{user['image']}"/><br/>
                telefone: {user['tel']} <br/>
                #<a href="/">Voltar</a>
                <hr />
        '''

    return html or abort(404, 'Usuario não encontrado')


app.add_url_rule('/user/<username>/', view_func=profile, endpoint='user')


#indicando qual tipo de dado na rota para evitar erros
@app.route('/user/<username>/<int:quote_id>/')
def quotes(username, quote_id):
    user = db.users.get(username, {})
    quote = user.get('quotes').get(quote_id)
    if user and quote:
        return f'''
            <h1>{user['name']}</h1>
            <img src="{user['image']}"/><br/>
            <p><q>{quote}</q></p>
            <hr />
            '''
    else:
        return abort(404, 'Usuario ou citação não encontrada')


#o path serve para aceitar qualquer caminho q venha depois
#independente de quantos forem.
@app.route('/file/<path:filename>/')
def filepath(filename):
    return f'Argumento recebido: {filename}'


#tratamento para procurar algum dado que tenha como inicial a letra A
@app.route('/reg/<regex("a.*"):name>/')
def reg(name):
    return f'Argumento iniciado com a letra a: {name}'



app.run()










