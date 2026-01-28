"""
WebDriver 설정 공통 모듈
Chrome, Edge 브라우저의 WebDriver 초기화와 자동화 탐지 우회 기능 제공
"""

from selenium import webdriver
import os


class DriverManager:
    """WebDriver 설정 공통 관리 클래스"""
    
    # WebDriver 기본 경로 설정
    WEBDRIVER_PATH = "./webdriverset"
    
    @staticmethod
    def setup_driver(browser="chrome", driver_path=None, headless=False):
        """
        WebDriver 설정
        
        Args:
            browser: 브라우저 종류 ("chrome" 또는 "edge")
            driver_path: WebDriver 경로 (미지정 시 기본 경로 사용)
            headless: 백그라운드 모드 여부
        
        Returns:
            WebDriver 인스턴스
        
        Raises:
            Exception: 지원하지 않는 브라우저 또는 WebDriver 초기화 실패
        """
        browser = browser.lower()
        
        if browser not in ["chrome", "edge"]:
            raise Exception(f"지원하지 않는 브라우저: {browser}")
        
        # driver_path가 폴더 경로인 경우 실제 드라이버 파일 경로로 변환
        if driver_path:
            driver_path = DriverManager._resolve_driver_path(browser, driver_path)
        
        # driver_path가 없으면 기본 경로에서 자동으로 찾기
        if not driver_path:
            driver_path = DriverManager._get_default_driver_path(browser)
        
        # 옵션 설정
        options = DriverManager._get_options(browser, headless)
        
        try:
            # WebDriver 초기화
            driver = DriverManager._create_driver(browser, driver_path, options)
            
            # WebDriver 속성 숨기기 (자동화 탐지 우회)
            DriverManager._hide_webdriver(driver)
            
            return driver
        except Exception as e:
            raise Exception(f"{browser.upper()} WebDriver 초기화 실패: {str(e)}")
    
    @staticmethod
    def _resolve_driver_path(browser, driver_path):
        """
        드라이버 경로 해석 (폴더 경로 또는 파일 경로)
        
        Args:
            browser: 브라우저 종류
            driver_path: 드라이버 경로 (폴더 또는 파일)
        
        Returns:
            드라이버 파일의 절대 경로
        """
        # 이미 파일 경로인 경우 (chromedriver.exe 또는 msedgedriver.exe로 끝나는 경우)
        if driver_path.endswith('chromedriver.exe') or driver_path.endswith('msedgedriver.exe'):
            return driver_path
        
        # 폴더 경로인 경우 파일 경로로 변환
        if os.path.isdir(driver_path):
            if browser == "chrome":
                driver_file = os.path.join(driver_path, "chromedriver.exe")
            else:  # edge
                driver_file = os.path.join(driver_path, "msedgedriver.exe")
            
            if os.path.exists(driver_file):
                return driver_file
        
        # 그 외 경우 원래 경로 반환
        return driver_path
    
    @staticmethod
    def _get_default_driver_path(browser):
        """기본 WebDriver 경로 반환"""
        if browser == "chrome":
            driver_name = "chromedriver.exe"
        else:  # edge
            driver_name = "msedgedriver.exe"
        
        # 상대경로와 절대경로 모두 시도
        relative_path = os.path.join(DriverManager.WEBDRIVER_PATH, driver_name)
        
        if os.path.exists(relative_path):
            print(f"WebDriver 찾음: {relative_path}")
            return relative_path
        
        # 상대경로가 없으면 현재 디렉토리 기준으로 재계산
        script_dir = os.path.dirname(os.path.abspath(__file__))
        absolute_path = os.path.join(script_dir, "..", DriverManager.WEBDRIVER_PATH, driver_name)
        
        if os.path.exists(absolute_path):
            print(f"WebDriver 찾음: {absolute_path}")
            return absolute_path
        
        print(f"경고: WebDriver를 찾을 수 없음. 상대경로: {relative_path}, 절대경로: {absolute_path}")
        # 경로를 찾을 수 없으면 기본값 반환 (Selenium이 PATH에서 찾도록)
        return relative_path
    
    @staticmethod
    def _get_options(browser, headless):
        """브라우저 옵션 설정"""
        if browser == "chrome":
            options = webdriver.ChromeOptions()
        else:
            options = webdriver.EdgeOptions()
        
        # 자동화 테스트 탐지 우회
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        if headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--window-size=1920,1080')
        else:
            options.add_argument('--start-maximized')
        
        return options
    
    @staticmethod
    def _create_driver(browser, driver_path, options):
        """WebDriver 인스턴스 생성"""
        try:
            if browser == "chrome":
                if driver_path and os.path.exists(driver_path):
                    return webdriver.Chrome(driver_path, options=options)
                else:
                    return webdriver.Chrome(options=options)
            else:  # edge
                if driver_path and os.path.exists(driver_path):
                    return webdriver.Edge(driver_path, options=options)
                else:
                    return webdriver.Edge(options=options)
        except Exception as e:
            print(f"드라이버 경로: {driver_path}")
            print(f"경로 존재 여부: {os.path.exists(driver_path) if driver_path else 'N/A'}")
            raise
    
    @staticmethod
    def _hide_webdriver(driver):
        """WebDriver 속성 숨기기 (자동화 탐지 우회)"""
        try:
            # CDP 명령 사용 시도
            driver.execute_cdp_command('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => false,
                    });
                '''
            })
        except:
            # CDP 미지원 시 execute_script 사용
            try:
                driver.execute_script('''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => false,
                    });
                ''')
            except:
                pass  # 둘 다 실패해도 계속 진행
