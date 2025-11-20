from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os

DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)


def configure_chrome_options():
    """Chrome WebDriver 옵션을 설정하여 자동 다운로드를 활성화합니다."""
    chrome_options = Options()
    prefs = {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False, # 다운로드 확인창 띄우지 않기
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    return chrome_options


def login_gerrit(url, username, password):
    """
    Selenium을 사용하여 Gerrit에 로그인하는 함수입니다.

    :param url: Gerrit 인스턴스의 로그인 페이지 URL
    :param username: Gerrit 사용자 이름 (또는 이메일)
    :param password: Gerrit 비밀번호
    """
    
    # WebDriver 서비스 설정 (WebDriver 실행 파일 경로를 명시해야 할 경우 아래 주석 처리된 라인 사용)
    # service = Service(executable_path='/path/to/your/chromedriver')
    # driver = webdriver.Chrome(service=service)
    
    # PATH에 WebDriver가 설정되어 있다면 아래와 같이 간단히 사용 가능
    print('1')
    options = configure_chrome_options()
    driver = webdriver.Chrome(options=options)
    print('2')
    print(driver)

    try:
        # Gerrit 로그인 페이지로 이동
        _url = f"{url}/login"
        driver.get(url)
        print(f"'{url}' 로 이동 중...")

        # 페이지가 완전히 로드될 때까지 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("페이지 로드 완료.")

        # 사용자 이름 입력 필드 찾기 (Gerrit의 실제 ID 또는 name 속성으로 변경 필요)
        # 예시: ID가 'username-field' 또는 'email-field' 라고 가정
        try:
            username_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "f_user")) 
                # 또는 By.NAME, By.CSS_SELECTOR 등을 사용
            )
            username_input.send_keys(username)
            print("사용자 이름 입력 완료.")
        except:
            print("경고: 사용자 이름 입력 필드를 찾을 수 없습니다. 셀렉터를 확인하세요.")
            return

        # 비밀번호 입력 필드 찾기 (Gerrit의 실제 ID 또는 name 속성으로 변경 필요)
        # 예시: ID가 'password-field' 라고 가정
        try:
            password_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "f_pass"))
            )
            password_input.send_keys(password)
            print("비밀번호 입력 완료.")
        except:
            print("경고: 비밀번호 입력 필드를 찾을 수 없습니다. 셀렉터를 확인하세요.")
            return

        # 로그인 버튼 클릭 (Gerrit의 실제 ID 또는 name, text 등으로 변경 필요)
        # 예시: ID가 'sign-in-button' 또는 버튼 텍스트가 'Sign In' 인 경우
        try:
            # ID로 찾기
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "b_signin"))
            )
            login_button.click()
            print("로그인 버튼 클릭 완료.")
            
            # 또는 버튼 텍스트로 찾기 (XPath 사용)
            # login_button = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, "//button[contains(span, 'Sign In')]"))
            # )
            # login_button.click()

        except:
            print("경고: 로그인 버튼을 찾을 수 없습니다. 셀렉터를 확인하세요.")
            return

        # 로그인이 성공했는지 확인하는 로직 추가 (예: 대시보드 URL로 이동했는지 확인)
        WebDriverWait(driver, 10).until(
            EC.url_contains("dashboard") # 로그인 후 이동하는 URL의 일부
        )
        print("로그인 성공! 대시보드로 이동했습니다.")
        
        # 로그인된 상태에서 추가 작업 수행 가능
        # ...
        
        time.sleep(5) # 로그인된 화면을 잠시 유지




        # 2. JSON 다운로드 URL로 이동
        projects_url = f"{url}/a/projects"
        print(f"프로젝트 데이터 URL로 이동: {projects_url}")
        driver.get(projects_url)

        # 3. 파일 다운로드 완료 대기 및 파일 경로 확인
        # 브라우저가 파일을 다운로드하는 동안 기다립니다.
        timeout = 20 # 초 단위
        start_time = time.time()
        downloaded_file = None
        
        while time.time() - start_time < timeout:
            files = os.listdir(DOWNLOAD_DIR)
            if files:
                # 가장 최근에 다운로드된 파일 (또는 유일한 파일) 선택
                # Gerrit은 보통 `projects`라는 이름의 JSON 파일을 다운로드합니다.
                # 정확한 파일명을 모른다면, 다운로드 폴더 내 첫 번째 파일을 선택할 수 있습니다.
                downloaded_file = os.path.join(DOWNLOAD_DIR, files[0])
                if not downloaded_file.endswith('.crdownload'): # Chrome 다운로드 중 임시 확장자 확인
                    break
            time.sleep(0.5)
        
        if not downloaded_file or downloaded_file.endswith('.crdownload'):
            print("파일 다운로드 시간 초과 또는 실패.")
            return

        print(f"파일 다운로드 완료: {downloaded_file}")

        # 4. 다운로드된 파일 읽기 및 JSON 처리
        with open(downloaded_file, 'r', encoding='utf-8') as f:
            json_text_with_prefix = f.read()
        
        # Gerrit JSON 접두사 제거 ("])}'\n")
        if json_text_with_prefix.startswith(")]}'"):
            json_string = json_text_with_prefix.split('\n', 1)[1]
            print("Gerrit 보안 접두사 제거 완료.")
        else:
            json_string = json_text_with_prefix

        # JSON 파싱 및 저장
        projects_data = json.loads(json_string)
        output_path = os.path.join(os.getcwd(), "gerrit_projects_downloaded.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(projects_data, f, ensure_ascii=False, indent=4)
        
        print(f"JSON 데이터가 '{output_path}'에 성공적으로 저장되었습니다.")








    except Exception as e:
        print(f"로그인 중 오류 발생: {e}")

    finally:
        # 브라우저 종료 (작업 완료 후)
        print("브라우저 종료.")
        driver.quit()

# --- 사용 예시 ---
if __name__ == "__main__":
    # TODO: 실제 Gerrit 인스턴스 정보로 변경하세요.
    GERRIT_URL = os.getenv("GERRIT_URL")
    GERRIT_USER = os.getenv("GERRIT_USER")
    GERRIT_PASSWORD = os.getenv("GERRIT_PWD")
    
    login_gerrit(GERRIT_URL, GERRIT_USER, GERRIT_PASSWORD)
