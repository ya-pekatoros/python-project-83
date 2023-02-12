from bs4 import BeautifulSoup


def get_url_data(data):
    data = BeautifulSoup(data, 'html.parser')
    title = data.title
    title = title.string if title else None
    h1 = data.h1 if data.h1 else None
    h1 = ''.join(map(str, h1)) if h1 else None
    description = data.find("meta", attrs={"name": "description"})
    description = description.get("content", None) if description else None
    return {"title": title, "h1": h1, "description": description}
