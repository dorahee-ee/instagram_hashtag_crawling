from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import nltk

'''
<Instagram 해시태그 크롤링 및 태그가 많이 된 상위 n개의 해시태그를 내림차순으로 정렬하는 프로그램>
- 크롤링 해오는 것 : 인스타그램 해시태그
- 상위 n개의 해시태그 정렬 -> nltk 
'''
driver = webdriver.Chrome()

# 인스타그램 login하는 함수
def login(id, pw):
    # id와 pw를 입력하는 창의 요소 정보 획득
    input = driver.find_elements(By.TAG_NAME, 'input')

    # 아이디를 입력
    input[0].send_keys(id)

    # 비밀번호 입력
    input[1].send_keys(pw)

    # 엔터
    input[1].send_keys(Keys.RETURN)
    time.sleep(5)

    # 로그인 정보 저장 여부 팝업창 제거
    btn_later1 = driver.find_element(By.CLASS_NAME, '_acan._acap._acas._aj1-')
    btn_later1.click()
    time.sleep(5)

    # 알림 설정 팝업창 제거
    btn_later2 = driver.find_element(By.CLASS_NAME, '_a9--._a9_1')
    btn_later2.click()

# 인스타그램 url 가져오고, id, pw 입력 후 login
driver.get('https://instagram.com')
time.sleep(3)
email = ''  # 인스타그램 계정 or ID
pw = ''  # 비밀번호
login(email, pw)

# 검색어 입력
_keyword = input('검색어를 입력하세요 : ')
driver.get('https://www.instagram.com/explore/tags/' + _keyword + '/')
time.sleep(5)

# 첫번째 게시물 클릭
first = driver.find_elements(By.CSS_SELECTOR, 'div._aagw')[0]
first.click()
time.sleep(5)

# 해쉬태그 크롤링
results = []
count = 100 # 크롤링할 게시글 개수 (100개)
for i in range(count):
    data = driver.find_elements(By.CSS_SELECTOR, 'a._aa9_._a6hd') # 해쉬태그 정보 저장
    for j in range(len(data)):
        results.append(data[j].text.replace("#","")) # '#'없애기
    driver.find_element(By.CSS_SELECTOR, 'div._aaqg._aaqh').click() #다음 게시물로 이동

# 상위 n개의 해쉬태그 내림차순 정렬
hash_tags = []
results_str = " ".join(results) # 결과값 list to string
tokens = results_str.split(" ") # 각 단어별로 떼어 내서
text = nltk.Text(tokens) # text에 저장하고
topWord = text.vocab().most_common(10) # 해쉬태그 개수 (10개)
for word, count in topWord:
    hash_tags.append(word)

# 정렬된 해쉬태그 출력
print(hash_tags)

# Chrome Driver 종료
driver.quit()