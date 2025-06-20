# 웹 브라우저를 자동 조작할 수 있게 해주는 라이브러리
from selenium import webdriver
# 웹 페이지의 선택자를 지정하는 클래스
from selenium.webdriver.common.by import By
# 웹 브라우저 옵션을 설정하는 클래스 (창 없이 실행하기, gpu 사용하지 않기 등)
from selenium.webdriver.chrome.options import Options
# 웹 페이지 로딩 대기 시간 설정
import time
# 경고 메시지 무시
import warnings
warnings.filterwarnings("ignore")
# 데이터 분석을 위한 라이브러리
import pandas as pd

# keyword를 검색해서 뉴스 제목을 가져오는 함수
def crawl_naver_news_with_selenium(keyword, max_page=5):
    # 웹 브라우저 옵션 설정을 위한 객체 생성
    options = Options()
    options.add_argument('--headless') # 브라우저 창을 띄우지 않고 백그라운드에서 실행

    # Linux/Chrome/Docker 환경에서 사용할 때 충돌을 막기 위한 옵션
    options.add_argument('--no-sandbox') # 브라우저 실행 환경 설정
    options.add_argument('--disable-dev-shm-usage') # 메모리 공유 사용 안 함

    # 웹 브라우저 실행 - 위에서 설정한 옵션을 반영해서 브라우저를 실행하는 객체 driver 생성
    driver = webdriver.Chrome(options=options)

    results = []
    for page in range(1, max_page + 1):
        # url을 동적으로 생성
        url = f"https://search.naver.com/search.naver?where=news&query={keyword}&start={(page - 1) * 10 + 1}"

        # 브라우저를 열고 해당 url에 접속
        driver.get(url)

        # 페이지가 완전히 로드될 때까지 2초간 대기 - JS로 만들어지는 콘텐츠가 많으므로 필수 과정
        time.sleep(2)

        # 뉴스 제목을 찾기 위한 선택자 지정
        titles = driver.find_elements(By.CSS_SELECTOR, ".sds-comps-text-type-headline1")

        # 뉴스 제목과 링크 출력
        # 몇 번째인지(i)
        # 텍스트 내용(title.text)
        # 링크 주소(title.get_attribute('href'))
        for i, title in enumerate(titles, 1):
            results.append({
                "제목": title.text,
            })
            print(f"\"{title.text}\"")

    # 브라우저를 닫고 Selenium 세션 종료
    driver.quit()

    # 결과를 DataFrame으로 변환 후 csv로 저장
    df = pd.DataFrame(results)
    df.to_csv(f"{keyword}_news.csv", index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    crawl_naver_news_with_selenium("크래프톤 정글", max_page=3)
