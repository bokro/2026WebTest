"""
버튼 테스트 클래스 모듈
웹사이트의 모든 버튼을 찾아서 클릭 테스트를 수행하는 기능 제공
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
import time
from loginModule.driver_manager import DriverManager


class ButtonTester:
    def __init__(self, url, driver_path=None, headless=False, browser="chrome"):
        """
        웹사이트의 모든 버튼을 테스트하는 클래스
        
        Args:
            url: 테스트할 웹사이트 URL
            driver_path: WebDriver 경로
            headless: 백그라운드 모드 실행 여부 (True: 브라우저 창 안 보임, False: 브라우저 창 보임)
            browser: 브라우저 종류 ("chrome" 또는 "edge")
        """
        self.url = url
        self.driver = None
        self.button_results = []
        self.headless = headless
        self.driver_path = driver_path
        self.browser = browser.lower()
        
    def setup_driver(self):
        """WebDriver 설정"""
        self.driver = DriverManager.setup_driver(
            browser=self.browser,
            driver_path=self.driver_path,
            headless=self.headless
        )
        
        if self.headless:
            print(f"백그라운드 모드로 {self.browser.upper()} 실행 중... (브라우저 창이 보이지 않습니다)")
        else:
            print(f"일반 모드로 {self.browser.upper()} 실행 중... (브라우저 창이 표시됩니다)")
        
        if self.driver_path:
            print(f"WebDriver 경로: {self.driver_path}")
    
    def find_all_buttons(self):
        """페이지에서 모든 버튼 요소 찾기"""
        buttons = []
        
        # button 태그로 찾기
        button_elements = self.driver.find_elements(By.TAG_NAME, "button")
        buttons.extend(button_elements)
        
        # input type="button", "submit", "reset" 찾기
        input_buttons = self.driver.find_elements(By.CSS_SELECTOR, 
            "input[type='button'], input[type='submit'], input[type='reset']")
        buttons.extend(input_buttons)
        
        # role="button"인 요소 찾기
        role_buttons = self.driver.find_elements(By.CSS_SELECTOR, "[role='button']")
        buttons.extend(role_buttons)
        
        # a 태그 중 버튼처럼 생긴 것들 찾기
        link_buttons = self.driver.find_elements(By.CSS_SELECTOR, 
            "a.btn, a.button, a[class*='button']")
        buttons.extend(link_buttons)
        
        # 중복 제거
        unique_buttons = []
        seen = set()
        for btn in buttons:
            try:
                # 요소의 고유 식별자로 중복 체크
                btn_id = id(btn)
                if btn_id not in seen:
                    seen.add(btn_id)
                    unique_buttons.append(btn)
            except StaleElementReferenceException:
                continue
                
        return unique_buttons
    
    def get_button_info(self, button):
        """버튼 정보 추출"""
        try:
            tag_name = button.tag_name
            text = button.text.strip()
            button_id = button.get_attribute('id')
            button_class = button.get_attribute('class')
            button_name = button.get_attribute('name')
            button_type = button.get_attribute('type')
            is_displayed = button.is_displayed()
            is_enabled = button.is_enabled()
            
            info = {
                'tag': tag_name,
                'text': text if text else '(텍스트 없음)',
                'id': button_id,
                'class': button_class,
                'name': button_name,
                'type': button_type,
                'displayed': is_displayed,
                'enabled': is_enabled
            }
            return info
        except Exception as e:
            return {'error': str(e)}
    
    def click_button(self, button, button_info, index):
        """버튼 클릭 시도"""
        result = {
            'index': index,
            'info': button_info,
            'clicked': False,
            'error': None
        }
        
        try:
            # 버튼이 보이고 활성화되어 있는지 확인
            if not button_info.get('displayed', False):
                result['error'] = '버튼이 화면에 보이지 않음'
                return result
                
            if not button_info.get('enabled', False):
                result['error'] = '버튼이 비활성화됨'
                return result
            
            # 스크롤하여 버튼이 보이도록
            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(0.3)
            
            # 클릭 시도
            original_url = self.driver.current_url
            button.click()
            time.sleep(1)  # 클릭 후 페이지 반응 대기
            
            new_url = self.driver.current_url
            result['clicked'] = True
            result['url_changed'] = original_url != new_url
            result['new_url'] = new_url if original_url != new_url else None
            
            # 원래 페이지로 돌아가기 (URL이 변경된 경우)
            if original_url != new_url:
                self.driver.back()
                time.sleep(1)
                
        except ElementClickInterceptedException:
            result['error'] = '다른 요소에 가려져 클릭 불가'
        except StaleElementReferenceException:
            result['error'] = '요소가 더 이상 존재하지 않음'
        except Exception as e:
            result['error'] = f'클릭 실패: {str(e)}'
            
        return result
    
    def run_test(self):
        """테스트 실행"""
        print(f"테스트 시작: {self.url}\n")
        
        try:
            # WebDriver 설정
            self.setup_driver()
            
            # 페이지 로드
            print("페이지 로딩 중...")
            self.driver.get(self.url)
            time.sleep(2)  # 페이지 완전히 로드될 때까지 대기
            
            # 버튼 찾기
            print("버튼 검색 중...\n")
            buttons = self.find_all_buttons()
            print(f"총 {len(buttons)}개의 버튼을 찾았습니다.\n")
            print("="*80)
            
            # 각 버튼에 대해 정보 수집 및 클릭 테스트
            for i, button in enumerate(buttons, 1):
                print(f"\n[버튼 {i}/{len(buttons)}]")
                
                # 버튼 정보 가져오기
                button_info = self.get_button_info(button)
                print(f"  태그: {button_info.get('tag', 'N/A')}")
                print(f"  텍스트: {button_info.get('text', 'N/A')}")
                if button_info.get('id'):
                    print(f"  ID: {button_info['id']}")
                if button_info.get('class'):
                    print(f"  클래스: {button_info['class']}")
                print(f"  표시: {button_info.get('displayed', 'N/A')}")
                print(f"  활성: {button_info.get('enabled', 'N/A')}")
                
                # 클릭 시도
                result = self.click_button(button, button_info, i)
                self.button_results.append(result)
                
                if result['clicked']:
                    print(f"  ✓ 클릭 성공")
                    if result.get('url_changed'):
                        print(f"    → URL 변경됨: {result['new_url']}")
                else:
                    print(f"  ✗ 클릭 실패: {result['error']}")
                
                print("-"*80)
                
            # 결과 요약
            self.print_summary()
            
        except Exception as e:
            print(f"테스트 중 오류 발생: {str(e)}")
        finally:
            if self.driver:
                print("\n브라우저를 닫는 중...")
                self.driver.quit()
    
    def print_summary(self):
        """테스트 결과 요약"""
        print("\n" + "="*80)
        print("테스트 결과 요약")
        print("="*80)
        
        total = len(self.button_results)
        clicked = sum(1 for r in self.button_results if r['clicked'])
        failed = total - clicked
        url_changed = sum(1 for r in self.button_results if r.get('url_changed', False))
        
        print(f"총 버튼 수: {total}")
        print(f"클릭 성공: {clicked}")
        print(f"클릭 실패: {failed}")
        print(f"URL 변경: {url_changed}")
        
        if failed > 0:
            print("\n실패한 버튼 목록:")
            for result in self.button_results:
                if not result['clicked']:
                    info = result['info']
                    print(f"  - [{result['index']}] {info.get('text', 'N/A')}: {result['error']}")
