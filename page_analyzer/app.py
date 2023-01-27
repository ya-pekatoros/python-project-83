from flask import (
    Flask,
    render_template,
    flash,
    get_flashed_messages,
    redirect,
    request,
    url_for,
)
import psycopg2
import os
from dotenv import load_dotenv
import datetime
from page_analyzer.url_validator import url_parser

load_dotenv()

server_config = {
    'SECRET_KEY': os.getenv('SECRET_KEY'),
    'DATABASE_URL': os.getenv('DATABASE_DEV_URL'),
}


def create_app(config_dict):
    app = Flask(__name__)
    for parameter in config_dict:
        app.config[parameter] = config_dict[parameter]
    return app


app = create_app(server_config)


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        '/index.html',
        messages=messages,
    )


@app.route('/', methods=['POST'])
def add_url():
    url = request.form['url']
    url_parsed = url_parser(url)
    if url_parsed['result'] is False:
        flash(url_parsed['message'], 'danger')
        return redirect(url_for('index'))
    today = datetime.date.today().isoformat()
    with psycopg2.connect(app.config['DATABASE_URL']) as conn:
        with conn.cursor() as curs:
            curs.execute("SELECT name FROM urls WHERE name = %s", (url_parsed['message'],))
            if curs.fetchone() == (url_parsed['message'],):
                flash('Страница уже существует', 'info')
                return redirect(url_for('index'))
            curs.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s)',
                         (url_parsed['message'], today))
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('index'))


@app.route('/urls')
def show_urls():
    with psycopg2.connect(app.config['DATABASE_URL']) as conn:
        with conn.cursor() as curs:
            curs.execute("SELECT id, name, TO_CHAR(created_at, 'DD-MM-YYYY') FROM urls ORDER BY id DESC LIMIT 30")
            result = curs.fetchall()

    return render_template(
        '/urls.html',
        data=result,
    )


@app.route('/urls/<id>')
def show_url(id):
    with psycopg2.connect(app.config['DATABASE_URL']) as conn:
        with conn.cursor() as curs:
            curs.execute("SELECT id, name, TO_CHAR(created_at, 'DD-MM-YYYY') FROM urls WHERE id = %s", (id,))
            result = curs.fetchone()
    (id, name, created_at) = result
    return render_template(
        '/url.html',
        id=id,
        name=name,
        created_at=created_at
    )
