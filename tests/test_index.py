def test_index(client):
    response = client.get('/')
    data1='Анализатор страниц'.encode("utf-8","ignore")
    data2='<p class="lead">Бесплатно проверяйте сайты на SEO пригодность</p>'.encode("utf-8","ignore")
    assert data1 in response.data
    assert data2 in response.data
    assert b'href="https://ru.hexlet.io/"' in response.data