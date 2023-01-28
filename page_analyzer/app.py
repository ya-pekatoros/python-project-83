from flask import (
    Flask,
    render_template,
    flash,
    get_flashed_messages,
    redirect,
    request,
    url_for,
    session,
)
import psycopg2
import os
from dotenv import load_dotenv
import datetime
from page_analyzer.url_validator import url_parser
from page_analyzer import make_external_req


load_dotenv()


server_config = {
    'SECRET_KEY': os.getenv('SECRET_KEY'),
    'DATABASE_URL': os.getenv('DATABASE_DEV_URL')
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
        messages=messages
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
            curs.execute("SELECT id, name FROM urls WHERE name = %s", (url_parsed['message'],))
            db_answer = curs.fetchone()
            if db_answer:
                (result_id, name, *_) = db_answer  # I am not waiting more then 2 values here, but
                if name == url_parsed['message']:  # I need unpuck it all for tests
                    flash('Страница уже существует', 'info')
                    return redirect(url_for('show_url', id=result_id))
            curs.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s)',
                         (url_parsed['message'], today))
            curs.execute("SELECT id FROM urls WHERE name = %s", (url_parsed['message'],))
            (result_id, *_) = curs.fetchone()
    flash('Страница успешно добавлена', 'success')
    session['name'] = url_parsed['message']
    return redirect(url_for('check_url', id=result_id))


@app.route('/urls')
def show_urls():
    with psycopg2.connect(app.config['DATABASE_URL']) as conn:
        with conn.cursor() as curs:
            curs.execute("SELECT urls.id, urls.name, TO_CHAR(url_checks.created_at, 'DD-MM-YYYY'), "
                         "url_checks.status_code FROM urls JOIN url_checks ON urls.id = url_checks.url_id "
                         "GROUP BY urls.id, urls.name, url_checks.created_at, url_checks.status_code "
                         "ORDER BY urls.id DESC, url_checks.created_at DESC LIMIT 30")
            result = curs.fetchall()

    return render_template(
        '/urls.html',
        data=result,
    )


@app.route('/urls/<id>')
def show_url(id):
    messages = get_flashed_messages(with_categories=True)
    with psycopg2.connect(app.config['DATABASE_URL']) as conn:
        with conn.cursor() as curs:
            curs.execute("SELECT id, name, TO_CHAR(created_at, 'DD-MM-YYYY') FROM urls WHERE id = %s", (id,))
            result_url = curs.fetchone()
            curs.execute("SELECT id, url_id, status_code, h1, title, description, "
                         "TO_CHAR(created_at, 'DD-MM-YYYY') FROM url_checks WHERE url_id = %s "
                         "ORDER BY id DESC LIMIT 30", (id,))
            result_checks = curs.fetchall()
    (url_id, name, created_at) = result_url
    return render_template(
        '/url.html',
        url_id=url_id,
        name=name,
        created_at=created_at,
        result_checks=result_checks,
        messages=messages
    )


@app.route('/urls/<id>/checks', methods=['GET', 'POST'])
def check_url(id):
    if request.method == 'POST':
        url = request.form['name']
        session['name'] = url
    else:
        url = session['name']
    today = datetime.date.today().isoformat()
    check_result = make_external_req(url)
    if check_result['message']:
        flash(check_result['message'], 'danger')
        return redirect(url_for('show_url', id=id))
    with psycopg2.connect(app.config['DATABASE_URL']) as conn:
        with conn.cursor() as curs:
            curs.execute('INSERT INTO url_checks (url_id, status_code, created_at) '
                         'VALUES (%s, %s, %s)', (id, str(check_result['status_code']), today))
    return redirect(url_for('show_url', id=id))
