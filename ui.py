"""
웹사이트 테스트 메인 GUI 프로그램
탭 구조로 버튼 테스트와 자동 로그인 기능을 제공
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import gc
from button_tester import ButtonTester
from loginModule.login_ui import LoginUI


class ButtonTestUI:
    """버튼 테스트 탭 UI"""
    
    def __init__(self, parent_frame):
        """
        초기화
        
        Args:
            parent_frame: 부모 프레임 (탭)
        """
        self.parent_frame = parent_frame
        self.tester = None
        self.test_thread = None
        self.is_running = False
        
        # 기본값 설정
        self.DEFAULT_URL = "https://example.com"
        self.HEADLESS_MODE = False
        
        self.setup_ui()
    
    def setup_ui(self):
        """UI 레이아웃 설정"""
        main_frame = ttk.Frame(self.parent_frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 제목
        title_label = tk.Label(
            main_frame,
            text="웹사이트 버튼 테스트",
            font=("Arial", 12, "bold"),
            fg="black"
        )
        title_label.pack(pady=10)
        
        # URL 입력 영역
        url_frame = ttk.LabelFrame(main_frame, text="테스트할 URL", padding="5")
        url_frame.pack(fill=tk.X, pady=5)
        
        url_label = tk.Label(url_frame, text="URL:", font=("Arial", 10))
        url_label.pack(side=tk.LEFT, padx=5)
        
        self.url_entry = tk.Entry(url_frame, width=70, font=("Arial", 10))
        self.url_entry.insert(0, self.DEFAULT_URL)
        self.url_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 옵션 영역
        options_frame = ttk.LabelFrame(main_frame, text="실행 옵션", padding="5")
        options_frame.pack(fill=tk.X, pady=5)
        
        # 브라우저 선택
        browser_frame = ttk.Frame(options_frame)
        browser_frame.pack(anchor=tk.W, pady=(0, 10))
        
        browser_label = tk.Label(browser_frame, text="브라우저:", font=("Arial", 10))
        browser_label.pack(side=tk.LEFT, padx=(0, 15))
        
        self.browser_var = tk.StringVar(value="chrome")
        chrome_radio = tk.Radiobutton(
            browser_frame,
            text="Chrome",
            variable=self.browser_var,
            value="chrome",
            font=("Arial", 10)
        )
        chrome_radio.pack(side=tk.LEFT, padx=(0, 15))
        
        edge_radio = tk.Radiobutton(
            browser_frame,
            text="Edge",
            variable=self.browser_var,
            value="edge",
            font=("Arial", 10)
        )
        edge_radio.pack(side=tk.LEFT)
        
        # WebDriver 경로 설정 (기본값: webdriverset 폴더)
        driver_label = tk.Label(options_frame, text="WebDriver 폴더:", font=("Arial", 10))
        driver_label.pack(anchor=tk.W, padx=5)
        
        self.driver_entry = tk.Entry(options_frame, width=70, font=("Arial", 10))
        self.driver_entry.insert(0, "./webdriverset")
        self.driver_entry.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        driver_info_label = tk.Label(
            options_frame,
            text="💡 기본값: ./webdriverset (chromedriver.exe, msedgedriver.exe 포함)",
            font=("Arial", 9),
            fg="gray"
        )
        driver_info_label.pack(anchor=tk.W, padx=5, pady=(0, 10))
        
        # 백그라운드 모드 체크박스
        self.headless_var = tk.BooleanVar(value=self.HEADLESS_MODE)
        headless_check = tk.Checkbutton(
            options_frame,
            text="백그라운드 모드 실행 (브라우저 창 숨기기)",
            variable=self.headless_var,
            font=("Arial", 10)
        )
        headless_check.pack(anchor=tk.W, padx=5)
        
        # 버튼 영역
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.start_button = ttk.Button(
            button_frame,
            text="시작",
            command=self.start_test,
            width=15
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(
            button_frame,
            text="중지",
            command=self.stop_test,
            width=15,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # 상태 표시 영역
        status_frame = ttk.LabelFrame(main_frame, text="상태", padding="5")
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = tk.Label(
            status_frame,
            text="준비됨",
            font=("Arial", 10),
            fg="blue"
        )
        self.status_label.pack(anchor=tk.W, padx=5, pady=5)
        
        # 진행률 바
        self.progress = ttk.Progressbar(
            status_frame,
            length=400,
            mode='indeterminate'
        )
        self.progress.pack(fill=tk.X, padx=5, pady=5)
        
        # 출력 영역
        output_frame = ttk.LabelFrame(main_frame, text="실행 결과", padding="5")
        output_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            width=100,
            height=15,
            font=("Courier", 9),
            wrap=tk.WORD
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.output_text.config(state=tk.DISABLED)
    
    def log_output(self, message):
        """출력 영역에 메시지 추가"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.parent_frame.update()
    
    def update_status(self, message, color="blue"):
        """상태 메시지 업데이트"""
        self.status_label.config(text=message, fg=color)
        self.parent_frame.update()
    
    def start_test(self):
        """테스트 시작"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("오류", "URL을 입력해주세요.")
            return
        
        if not url.startswith(('http://', 'https://')):
            messagebox.showerror("오류", "URL은 http:// 또는 https://로 시작해야 합니다.")
            return
        
        # webdriverset 폴더 경로 (드라이버 자동 감지)
        driver_path = self.driver_entry.get().strip()
        driver_path = driver_path if driver_path else "./webdriverset"
        
        # UI 상태 업데이트
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.url_entry.config(state=tk.DISABLED)
        self.driver_entry.config(state=tk.DISABLED)
        self.progress.start()
        
        # 출력 영역 초기화
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
        
        self.update_status("테스트 실행 중...", "green")
        self.log_output("테스트 시작")
        self.log_output(f"URL: {url}")
        self.log_output(f"브라우저: {self.browser_var.get().upper()}")
        self.log_output(f"WebDriver 경로: {driver_path}")
        self.log_output(f"백그라운드 모드: {self.headless_var.get()}")
        self.log_output("-" * 80)
        
        # 테스트를 별도 스레드에서 실행
        self.test_thread = threading.Thread(
            target=self.run_test_thread,
            args=(url, driver_path, self.headless_var.get(), self.browser_var.get()),
            daemon=True
        )
        self.test_thread.start()
    
    def run_test_thread(self, url, driver_path, headless, browser):
        """테스트 실행 스레드"""
        try:
            self.tester = ButtonTester(url, driver_path=driver_path, headless=headless, browser=browser)
            
            self.log_output("페이지 로딩 중...\n")
            self.tester.setup_driver()
            
            self.log_output("페이지 로딩 완료. 버튼 검색 중...\n")
            self.tester.driver.get(url)
            
            import time
            time.sleep(2)
            
            buttons = self.tester.find_all_buttons()
            self.log_output(f"총 {len(buttons)}개의 버튼을 찾았습니다.\n")
            self.log_output("=" * 80)
            
            for i, button in enumerate(buttons, 1):
                if not self.is_running:
                    self.log_output("\n테스트가 중지되었습니다.")
                    break
                
                self.log_output(f"\n[버튼 {i}/{len(buttons)}]")
                
                button_info = self.tester.get_button_info(button)
                self.log_output(f"  태그: {button_info.get('tag', 'N/A')}")
                self.log_output(f"  텍스트: {button_info.get('text', 'N/A')}")
                if button_info.get('id'):
                    self.log_output(f"  ID: {button_info['id']}")
                if button_info.get('class'):
                    self.log_output(f"  클래스: {button_info['class']}")
                self.log_output(f"  표시: {button_info.get('displayed', 'N/A')}")
                self.log_output(f"  활성: {button_info.get('enabled', 'N/A')}")
                
                result = self.tester.click_button(button, button_info, i)
                self.tester.button_results.append(result)
                
                if result['clicked']:
                    self.log_output(f"  ✓ 클릭 성공")
                    if result.get('url_changed'):
                        self.log_output(f"    → URL 변경됨: {result['new_url']}")
                else:
                    self.log_output(f"  ✗ 클릭 실패: {result['error']}")
                
                self.log_output("-" * 80)
            
            self.log_output("\n" + "=" * 80)
            self.log_output("테스트 결과 요약")
            self.log_output("=" * 80)
            
            total = len(self.tester.button_results)
            clicked = sum(1 for r in self.tester.button_results if r['clicked'])
            failed = total - clicked
            url_changed = sum(1 for r in self.tester.button_results if r.get('url_changed', False))
            
            self.log_output(f"총 버튼 수: {total}")
            self.log_output(f"클릭 성공: {clicked}")
            self.log_output(f"클릭 실패: {failed}")
            self.log_output(f"URL 변경: {url_changed}")
            
            if failed > 0:
                self.log_output("\n실패한 버튼 목록:")
                for result in self.tester.button_results:
                    if not result['clicked']:
                        info = result['info']
                        self.log_output(f"  - [{result['index']}] {info.get('text', 'N/A')}: {result['error']}")
            
            self.log_output("\n테스트 완료!")
            self.update_status("테스트 완료", "green")
            
        except Exception as e:
            self.log_output(f"오류 발생: {str(e)}")
            self.update_status(f"오류: {str(e)}", "red")
        finally:
            if self.tester and self.tester.driver:
                try:
                    self.tester.driver.quit()
                    self.log_output("브라우저 종료 완료")
                except:
                    pass
            
            self.cleanup_resources()
            self.is_running = False
            self.progress.stop()
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.url_entry.config(state=tk.NORMAL)
            self.driver_entry.config(state=tk.NORMAL)
    
    def stop_test(self):
        """테스트 중지"""
        if messagebox.askyesno("확인", "테스트를 중지하시겠습니까?"):
            self.is_running = False
            
            if self.tester and self.tester.driver:
                try:
                    self.tester.driver.quit()
                    self.log_output("\n브라우저를 강제 종료했습니다.")
                except:
                    pass
            
            self.cleanup_resources()
            self.update_status("중지됨", "red")
            self.progress.stop()
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.url_entry.config(state=tk.NORMAL)
            self.driver_entry.config(state=tk.NORMAL)
    
    def cleanup_resources(self):
        """리소스 정리"""
        if self.tester:
            try:
                if hasattr(self.tester, 'button_results'):
                    self.tester.button_results.clear()
            except:
                pass
            self.tester = None
        
        gc.collect()


class MainGUI:
    """메인 GUI 클래스 (탭 구조)"""
    
    def __init__(self, root):
        """
        초기화
        
        Args:
            root: 루트 윈도우
        """
        self.root = root
        self.root.title("웹사이트 테스트 도구")
        self.root.geometry("1000x750")
        self.root.resizable(True, True)
        
        self.button_test_ui = None
        self.login_ui = None
        
        self.setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """탭 UI 설정"""
        # 탭 생성
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 탭 1: 버튼 테스트
        button_test_tab = ttk.Frame(self.notebook)
        self.notebook.add(button_test_tab, text="버튼 테스트")
        self.button_test_ui = ButtonTestUI(button_test_tab)
        
        # 탭 2: 자동 로그인
        login_tab = ttk.Frame(self.notebook)
        self.notebook.add(login_tab, text="자동 로그인")
        self.login_ui = LoginUI(login_tab)
    
    def on_closing(self):
        """프로그램 종료"""
        if messagebox.askyesno("종료", "프로그램을 종료하시겠습니까?"):
            # 실행 중인 작업 정리
            if self.button_test_ui and self.button_test_ui.is_running:
                self.button_test_ui.is_running = False
                if self.button_test_ui.tester and self.button_test_ui.tester.driver:
                    try:
                        self.button_test_ui.tester.driver.quit()
                    except:
                        pass
            
            if self.login_ui and self.login_ui.is_logging_in:
                self.login_ui.is_logging_in = False
                if self.login_ui.login_executor and self.login_ui.login_executor.driver:
                    try:
                        self.login_ui.login_executor.driver.quit()
                    except:
                        pass
            
            gc.collect()
            self.root.destroy()


def main():
    """메인 함수"""
    root = tk.Tk()
    gui = MainGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
