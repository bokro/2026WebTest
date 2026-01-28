"""
로그인 실행 모듈
실제 웹사이트에서 로그인을 수행
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException,
    StaleElementReferenceException
)
import time
from .driver_manager import DriverManager


class LoginExecutor:
    """로그인 실행 클래스"""
    
    def __init__(self, url, driver_path=None, headless=False, browser="chrome"):
        """
        초기화
        
        Args:
            url: 로그인 웹사이트 URL
            driver_path: WebDriver 경로
            headless: 백그라운드 모드 여부
            browser: 브라우저 종류 ("chrome" 또는 "edge")
        """
        self.url = url
        self.driver_path = driver_path
        self.headless = headless
        self.browser = browser.lower()
        self.driver = None
        self.login_result = None
    
    def setup_driver(self):
        """WebDriver 설정"""
        self.driver = DriverManager.setup_driver(
            browser=self.browser,
            driver_path=self.driver_path,
            headless=self.headless
        )
    
    def load_page(self):
        """페이지 로드"""
        try:
            self.driver.get(self.url)
            time.sleep(2)
            return True
        except Exception as e:
            self.login_result = f"페이지 로드 실패: {str(e)}"
            return False
    
    def find_element_by_selector(self, selector):
        """
        CSS 선택자로 요소 찾기
        
        Args:
            selector: CSS 선택자
        
        Returns:
            WebElement 또는 None
        """
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return element
        except TimeoutException:
            return None
        except Exception as e:
            print(f"요소 찾기 실패 ({selector}): {str(e)}")
            return None
    
    def execute_login(self, username, password, id_field_selector, 
                     password_field_selector, submit_button_selector, skip_submit_button=False):
        """
        로그인 실행
        
        Args:
            username: 사용자명
            password: 패스워드
            id_field_selector: ID 필드 선택자
            password_field_selector: 패스워드 필드 선택자
            submit_button_selector: 제출 버튼 선택자
            skip_submit_button: True이면 제출 버튼을 찾지 않고 바로 Enter 키 입력
        
        Returns:
            dict: 로그인 결과
        """
        result = {
            "success": False,
            "message": "",
            "original_url": self.driver.current_url,
            "final_url": None
        }
        
        try:
            # ID 필드 찾기
            id_field = self.find_element_by_selector(id_field_selector)
            if not id_field:
                result["message"] = f"ID 필드를 찾을 수 없습니다: {id_field_selector}"
                return result
            
            # ID 입력
            id_field.clear()
            id_field.send_keys(username)
            time.sleep(0.5)
            
            # 패스워드 필드 찾기
            password_field = self.find_element_by_selector(password_field_selector)
            if not password_field:
                result["message"] = f"패스워드 필드를 찾을 수 없습니다: {password_field_selector}"
                return result
            
            # 패스워드 입력
            password_field.clear()
            password_field.send_keys(password)
            time.sleep(0.5)
            
            # 제출 방식 선택
            if skip_submit_button:
                # Enter 키로 바로 제출
                result["message"] = "Enter 키로 제출합니다."
                password_field.send_keys(Keys.RETURN)
                time.sleep(2)
            else:
                # 제출 버튼 찾기
                submit_button = self.find_element_by_selector(submit_button_selector)
                if submit_button:
                    # 제출 버튼이 있으면 클릭
                    submit_button.click()
                    time.sleep(2)
                else:
                    # 제출 버튼이 없으면 Enter 키 입력
                    result["message"] = f"제출 버튼을 찾을 수 없어 Enter 키를 사용합니다: {submit_button_selector}"
                    password_field.send_keys(Keys.RETURN)
                    time.sleep(2)
            
            # 최종 URL 확인
            final_url = self.driver.current_url
            result["final_url"] = final_url
            
            # URL이 변경되었으면 성공으로 판단
            if final_url != result["original_url"]:
                result["success"] = True
                result["message"] = "로그인 성공! URL이 변경되었습니다."
            else:
                result["message"] = "로그인 완료했으나 URL이 변경되지 않았습니다. 로그인 성공 여부를 확인해주세요."
            
            return result
            
        except StaleElementReferenceException:
            result["message"] = "요소 참조가 유효하지 않습니다. 다시 시도해주세요."
        except Exception as e:
            result["message"] = f"로그인 실패: {str(e)}"
        
        return result
    
    def close_driver(self):
        """브라우저 종료"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
