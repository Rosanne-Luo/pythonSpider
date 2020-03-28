import requests
from bs4 import BeautifulSoup
import json
from requests.exceptions import RequestException


def get_one_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 "
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    soup = BeautifulSoup(html, "lxml")
    dds = soup.find_all(name="dd")
    # 提取排名, 评分，标题，演员，上映时间

    for dd in dds:
        rank = dd.i.string
        score = dd.find(class_="integer").string.strip() + dd.find(class_="fraction").string.strip()
        title = dd.find(class_="movie-item-info").p.a.string
        actors = dd.find(class_="star").string.strip()
        time = dd.find(class_="releasetime").string

        yield {"rank": rank, "score": score, "title": title, "actors": actors, "time": time}


def write_to_file(content):
    with open("result.txt", 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False)+'\n')


def main(offset):
    url = "https://maoyan.com/board/4?offset=" + str(offset)
    html = get_one_page(url)
    results = parse_one_page(html)
    for r in results:
        write_to_file(r)


if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 10)
