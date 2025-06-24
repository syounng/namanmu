import warnings
warnings.filterwarnings("ignore")

import requests
from bs4 import BeautifulSoup

def crawl_naver_news(keyword, page=1):
    url = f"https://search.naver.com/search.naver?where=news&query={keyword}&start={(page - 1) * 10 + 1}"
    headers = {"User-Agent": "Mozilla/5.0"}
    # url = "https://search.naver.com/search.naver?where=news&query=치킨&start=1"
    # headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # print(soup.prettify()[:10000])

    results = []

    articles = soup.select('.sds-comps-text')

    # print("--------articles: ", articles)

    for article in articles:
        a_tag = article.select_one("a")
        if a_tag and "href" in a_tag.attrs:
            title = a_tag.get_text(strip=True)
            link = a_tag["href"]
            results.append((title, link))

    return results

# 테스트
if __name__ == "__main__":
    keyword = "chicken"
    news_list = crawl_naver_news(keyword)

    for i, (title, link) in enumerate(news_list, 1):
        print(f"{i}. {title}\n{link}")
