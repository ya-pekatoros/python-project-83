from functools import reduce
from bs4 import BeautifulSoup


def get_url_data(data):
    data = BeautifulSoup(data, 'html.parser')
    title = data.title
    title = title.string[:255] if title else None
    h1 = data.h1 if data.h1 else None
    h1 = reduce(lambda text, data: text + str(data), h1, '')[:255] if h1 else None
    description = data.find("meta", attrs={"name": "description"})
    description = description.get("content", None) if description else None
    description = description[:255] if description else None
    return {"title": title, "h1": h1, "description": description}
