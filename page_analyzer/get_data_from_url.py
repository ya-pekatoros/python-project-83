from bs4 import BeautifulSoup


def get_url_data(data):
    data = BeautifulSoup(data, 'html.parser')
    title = data.title
    if title:
        title = title.string[:255]
    h1 = data.h1
    if h1:
        h1_text = ''
        for elem in h1.contents:
            h1_text += str(elem)
        h1 = h1_text[:255]
    description = data.find("meta", attrs={"name": "description"})
    if description:
        description = description.get("content", None)
    if description:
        description = description[:255]
    return {"title": title, "h1": h1, "description": description}
