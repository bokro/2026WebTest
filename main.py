"""
웹사이트 버튼 테스트 메인 프로그램
사용자 입력을 받아 ButtonTester를 실행하는 메인 진입점
"""

import selenium
from button_tester import ButtonTester


def print_header():
    """프로그램 헤더 출력"""
    print("웹사이트 버튼 테스트 프로그램")
    print("="*80)


def check_selenium_version():
    """Selenium 버전 확인 및 출력"""
    try:
        selenium_version = selenium.__version__
        print(f"Selenium 버전: {selenium_version}")
    except AttributeError:
        print("Selenium 버전을 확인할 수 없습니다.")
    print("="*80)


def get_test_url():
    """사용자로부터 테스트할 URL 입력받기"""
    default_url = "https://example.com"
    user_url = input(f"테스트할 URL을 입력하세요 (기본값: {default_url}): ").strip()
    return user_url if user_url else default_url


def get_headless_mode():
    """백그라운드 모드 실행 여부 확인"""
    headless_input = input("백그라운드 모드로 실행하시겠습니까? (y/n, 기본값: n): ").strip().lower()
    return headless_input in ['y', 'yes', '예']


def get_driver_path():
    """ChromeDriver 경로 입력받기 (선택사항)"""
    driver_path = input("ChromeDriver 경로를 입력하세요 (Enter=자동 감지): ").strip()
    return driver_path if driver_path else None


def main():
    """메인 실행 함수"""
    # ========== 설정 구역 (여기서 직접 수정 가능) ==========
    # ChromeDriver 경로 (None이면 자동 감지)
    DRIVER_PATH = "./chromedriver-win64/chromedriver.exe"  # 예: "C:/chromedriver/chromedriver.exe" 또는 "./chromedriver.exe"
    
    # 기본 URL (사용자 입력 받을 때 기본값)
    DEFAULT_URL = "https://example.com"
    
    # 백그라운드 모드 (True: 브라우저 창 안 보임, False: 브라우저 창 보임)
    HEADLESS_MODE = False
    # ====================================================
    
    # 헤더 출력
    print_header()
    
    # Selenium 버전 확인
    check_selenium_version()
    
    # URL 입력 받기 (DEFAULT_URL 사용)
    user_url = input(f"테스트할 URL을 입력하세요 (기본값: {DEFAULT_URL}): ").strip()
    test_url = user_url if user_url else DEFAULT_URL
    
    # 실행 모드 선택 (HEADLESS_MODE 기본값 표시)
    mode_text = "y" if HEADLESS_MODE else "n"
    headless_input = input(f"백그라운드 모드로 실행하시겠습니까? (y/n, 기본값: {mode_text}): ").strip().lower()
    if headless_input:
        headless_mode = headless_input in ['y', 'yes', '예']
    else:
        headless_mode = HEADLESS_MODE
    
    # ChromeDriver 경로 (DRIVER_PATH 사용, 필요시 입력받기)
    if DRIVER_PATH:
        print(f"설정된 ChromeDriver 경로: {DRIVER_PATH}")
        driver_path = DRIVER_PATH
    else:
        driver_input = input("ChromeDriver 경로를 입력하세요 (Enter=자동 감지): ").strip()
        driver_path = driver_input if driver_input else None
    
    # 테스트 실행
    print()  # 빈 줄 추가
    tester = ButtonTester(test_url, driver_path=driver_path, headless=headless_mode)
    tester.run_test()
    
    print("\n테스트 완료!")


if __name__ == "__main__":
    main()
