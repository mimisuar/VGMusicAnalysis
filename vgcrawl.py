from bs4 import BeautifulSoup
import requests

base_url = "http://vgmusic.com"

r = requests.get(base_url)
if r.status_code == requests.codes.ok:
    html_doc = BeautifulSoup(r.text, "html.parser")

    for link in html_doc.find_all("a"):
        if "console" in link["href"]:
            console_name = str(link.string).lower().replace(" ", "")
            # crawl through the music now :)
            console_url = base_url + str(link["href"])[1:]
            sub_r = requests.get(console_url)
            if sub_r.status_code == requests.codes.ok:
                console_doc = BeautifulSoup(sub_r.text, "html.parser")

                for sub_link in console_doc.find_all("a"):
                    name = sub_link.get("name")
                    if name:
                        print("GAME NAME:" + name)
        
else:
    r.raise_for_status()