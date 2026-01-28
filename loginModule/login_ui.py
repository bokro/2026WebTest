"""
로그인 UI 모듈
로그인 기능을 위한 사용자 인터페이스
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from loginModule.credential_manager import CredentialManager
from loginModule.field_detector import FieldDetector
from loginModule.login_executor import LoginExecutor


class LoginUI:
    """로그인 UI 클래스"""
    
    def __init__(self, parent_frame):
        """
        초기화
        
        Args:
            parent_frame: 부모 프레임 (탭)
        """
        self.parent_frame = parent_frame
        self.credential_manager = CredentialManager()
        self.field_detector = FieldDetector()
        self.login_executor = None
        self.is_logging_in = False
        
        self.setup_ui()
        self.refresh_account_list()
    
    def setup_ui(self):
        """UI 레이아웃 설정"""
        # 메인 컨테이너
        main_container = ttk.PanedWindow(self.parent_frame, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ========== 왼쪽 패널: 계정 관리 ==========
        left_frame = ttk.LabelFrame(main_container, text="계정 관리", padding="10")
        main_container.add(left_frame, weight=1)
        
        # 계정 리스트
        list_label = tk.Label(left_frame, text="저장된 계정", font=("Arial", 10, "bold"))
        list_label.pack(anchor=tk.W, pady=(0, 5))
        
        # 계정 리스트박스 (프레임으로 감싸기)
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.account_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=("Arial", 10),
            height=10
        )
        self.account_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.account_listbox.bind('<<ListboxSelect>>', self.on_account_select)
        scrollbar.config(command=self.account_listbox.yview)
        
        # 계정 추가/관리 버튼
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        add_btn = ttk.Button(
            button_frame,
            text="계정 추가",
            command=self.open_add_account_dialog
        )
        add_btn.pack(side=tk.LEFT, padx=2)
        
        edit_btn = ttk.Button(
            button_frame,
            text="편집",
            command=self.open_edit_account_dialog
        )
        edit_btn.pack(side=tk.LEFT, padx=2)
        
        delete_btn = ttk.Button(
            button_frame,
            text="삭제",
            command=self.delete_account
        )
        delete_btn.pack(side=tk.LEFT, padx=2)
        
        # 선택된 계정 정보 표시
        info_label = tk.Label(left_frame, text="계정 정보", font=("Arial", 10, "bold"))
        info_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.info_text = tk.Text(left_frame, height=6, font=("Courier", 9), wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, expand=False)
        self.info_text.config(state=tk.DISABLED)
        
        # ========== 오른쪽 패널: 로그인 실행 ==========
        right_frame = ttk.LabelFrame(main_container, text="로그인 실행", padding="10")
        main_container.add(right_frame, weight=1)
        
        # URL 입력
        url_label = tk.Label(right_frame, text="웹사이트 URL", font=("Arial", 10, "bold"))
        url_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.url_entry = tk.Entry(right_frame, font=("Arial", 10))
        self.url_entry.pack(fill=tk.X, pady=(0, 10))
        self.url_entry.insert(0, "https://")
        
        # 옵션
        option_label = tk.Label(right_frame, text="옵션", font=("Arial", 10, "bold"))
        option_label.pack(anchor=tk.W, pady=(0, 5))
        
        # 브라우저 선택
        browser_frame = ttk.Frame(right_frame)
        browser_frame.pack(anchor=tk.W, pady=(0, 5))
        
        browser_label = tk.Label(browser_frame, text="브라우저:", font=("Arial", 9))
        browser_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.browser_var = tk.StringVar(value="chrome")
        chrome_radio = tk.Radiobutton(
            browser_frame,
            text="Chrome",
            variable=self.browser_var,
            value="chrome",
            font=("Arial", 9)
        )
        chrome_radio.pack(side=tk.LEFT, padx=(0, 10))
        
        edge_radio = tk.Radiobutton(
            browser_frame,
            text="Edge",
            variable=self.browser_var,
            value="edge",
            font=("Arial", 9)
        )
        edge_radio.pack(side=tk.LEFT)
        
        self.headless_var = tk.BooleanVar(value=False)
        headless_check = tk.Checkbutton(
            right_frame,
            text="백그라운드 모드 (브라우저 창 숨기기)",
            variable=self.headless_var,
            font=("Arial", 9)
        )
        headless_check.pack(anchor=tk.W, pady=(0, 5))
        
        self.skip_submit_button_var = tk.BooleanVar(value=False)
        skip_submit_check = tk.Checkbutton(
            right_frame,
            text="제출 버튼 무시하고 Enter 키로 제출 (빠른 로그인)",
            variable=self.skip_submit_button_var,
            font=("Arial", 9)
        )
        skip_submit_check.pack(anchor=tk.W, pady=(0, 5))
        
        self.keep_browser_open_var = tk.BooleanVar(value=False)
        keep_browser_check = tk.Checkbutton(
            right_frame,
            text="로그인 후 브라우저 유지 (자동 종료 안 함)",
            variable=self.keep_browser_open_var,
            font=("Arial", 9)
        )
        keep_browser_check.pack(anchor=tk.W, pady=(0, 10))
        
        # 로그인 버튼
        login_frame = ttk.Frame(right_frame)
        login_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.login_btn = ttk.Button(
            login_frame,
            text="로그인 실행",
            command=self.execute_login
        )
        self.login_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.cancel_btn = ttk.Button(
            login_frame,
            text="중지",
            command=self.cancel_login,
            state=tk.DISABLED
        )
        self.cancel_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 상태 메시지
        self.status_label = tk.Label(
            right_frame,
            text="준비됨",
            font=("Arial", 10),
            fg="blue"
        )
        self.status_label.pack(anchor=tk.W, pady=(0, 10))
        
        # 진행률 바
        self.progress = ttk.Progressbar(
            right_frame,
            length=300,
            mode='indeterminate'
        )
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        # 결과 표시
        result_label = tk.Label(right_frame, text="로그인 결과", font=("Arial", 10, "bold"))
        result_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.result_text = scrolledtext.ScrolledText(
            right_frame,
            height=6,
            font=("Courier", 9),
            wrap=tk.WORD
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.result_text.config(state=tk.DISABLED)
    
    def refresh_account_list(self):
        """계정 리스트 새로고침"""
        self.account_listbox.delete(0, tk.END)
        accounts = self.credential_manager.get_all_credentials()
        
        for account in accounts:
            display_text = f"[{account['id']}] {account['title']}"
            self.account_listbox.insert(tk.END, display_text)
    
    def on_account_select(self, event):
        """계정 선택 이벤트"""
        selection = self.account_listbox.curselection()
        if not selection:
            return
        
        # ID 추출 (리스트에서 선택된 항목의 ID는 index + 1)
        account_id = selection[0] + 1
        
        account = self.credential_manager.get_credential_by_id(account_id)
        if account:
            # 정보 표시 (패스워드는 마스킹)
            self.info_text.config(state=tk.NORMAL)
            self.info_text.delete(1.0, tk.END)
            
            info = f"""
타이틀: {account['title']}
URL: {account['site_url']}
사용자명: {account['username']}
패스워드: {'*' * len(account['password'])}

ID필드: {account['id_field_selector'] or '(미설정)'}
패스워드필드: {account['password_field_selector'] or '(미설정)'}
제출버튼: {account['submit_button_selector'] or '기본값'}
            """.strip()
            
            self.info_text.insert(1.0, info)
            self.info_text.config(state=tk.DISABLED)
            
            # URL 자동 입력
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, account['site_url'])
    
    def open_add_account_dialog(self):
        """계정 추가 대화상자"""
        dialog = tk.Toplevel(self.parent_frame)
        dialog.title("계정 추가")
        dialog.geometry("500x600")
        dialog.resizable(False, False)
        
        # 타이틀
        ttk.Label(dialog, text="계정 타이틀 (예: 네이버, 구글):", font=("Arial", 10)).pack(anchor=tk.W, padx=10, pady=(10, 0))
        title_entry = tk.Entry(dialog, font=("Arial", 10))
        title_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # URL
        ttk.Label(dialog, text="웹사이트 URL:", font=("Arial", 10)).pack(anchor=tk.W, padx=10, pady=(0, 0))
        url_entry = tk.Entry(dialog, font=("Arial", 10))
        url_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        url_entry.insert(0, "https://")
        
        # 사용자명
        ttk.Label(dialog, text="사용자명 (ID):", font=("Arial", 10)).pack(anchor=tk.W, padx=10, pady=(0, 0))
        username_entry = tk.Entry(dialog, font=("Arial", 10))
        username_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # 패스워드
        ttk.Label(dialog, text="패스워드:", font=("Arial", 10)).pack(anchor=tk.W, padx=10, pady=(0, 0))
        password_entry = tk.Entry(dialog, font=("Arial", 10), show="*")
        password_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # 필드 선택자 영역 (구분선)
        separator = ttk.Separator(dialog, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(dialog, text="필드 선택자 (개발자 도구 F12로 찾기):", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        # ID 필드 선택자
        ttk.Label(dialog, text="ID 필드 선택자:", font=("Arial", 9)).pack(anchor=tk.W, padx=10, pady=(0, 0))
        id_field_entry = tk.Entry(dialog, font=("Arial", 9))
        id_field_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        id_field_entry.insert(0, "input[name='username']")
        
        # 패스워드 필드 선택자
        ttk.Label(dialog, text="패스워드 필드 선택자:", font=("Arial", 9)).pack(anchor=tk.W, padx=10, pady=(0, 0))
        pwd_field_entry = tk.Entry(dialog, font=("Arial", 9))
        pwd_field_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        pwd_field_entry.insert(0, "input[type='password']")
        
        # 제출 버튼 선택자
        ttk.Label(dialog, text="제출 버튼 선택자 (선택사항 - 없으면 Enter 키 사용):", font=("Arial", 9)).pack(anchor=tk.W, padx=10, pady=(0, 0))
        submit_btn_entry = tk.Entry(dialog, font=("Arial", 9))
        submit_btn_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        submit_btn_entry.insert(0, "button[type='submit']")
        
        # 도움말 버튼
        help_btn = ttk.Button(
            dialog,
            text="선택자 도움말 보기",
            command=lambda: self._show_selector_help_dialog()
        )
        help_btn.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # 버튼
        def add_account():
            title = title_entry.get().strip()
            url = url_entry.get().strip()
            username = username_entry.get().strip()
            password = password_entry.get()
            id_field = id_field_entry.get().strip()
            pwd_field = pwd_field_entry.get().strip()
            submit_btn = submit_btn_entry.get().strip()
            
            if not all([title, url, username, password, id_field, pwd_field]):
                messagebox.showerror("오류", "필수 필드를 입력해주세요.\n(제출 버튼은 선택사항입니다)")
                return
            
            if self.credential_manager.add_credential(title, url, username, password):
                account_id = len(self.credential_manager.get_all_credentials())
                if self.credential_manager.update_credential(
                    account_id,
                    id_field=id_field,
                    password_field=pwd_field,
                    submit_button=submit_btn
                ):
                    messagebox.showinfo("성공", "계정이 추가되었습니다.")
                    self.refresh_account_list()
                    dialog.destroy()
                else:
                    messagebox.showerror("오류", "필드 선택자 저장에 실패했습니다.")
            else:
                messagebox.showerror("오류", "계정 추가에 실패했습니다.")
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="추가", command=add_account).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="취소", command=dialog.destroy).pack(side=tk.LEFT, padx=2)
    
    def open_edit_account_dialog(self):
        """계정 편집 대화상자"""
        selection = self.account_listbox.curselection()
        if not selection:
            messagebox.showwarning("경고", "편집할 계정을 선택해주세요.")
            return
        
        account_id = selection[0] + 1
        account = self.credential_manager.get_credential_by_id(account_id)
        
        if not account:
            messagebox.showerror("오류", "계정 정보를 불러올 수 없습니다.")
            return
        
        dialog = tk.Toplevel(self.parent_frame)
        dialog.title("계정 편집")
        dialog.geometry("500x500")
        dialog.resizable(False, False)
        
        # 타이틀
        ttk.Label(dialog, text="계정 타이틀:", font=("Arial", 10)).pack(anchor=tk.W, padx=10, pady=(10, 0))
        title_entry = tk.Entry(dialog, font=("Arial", 10))
        title_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        title_entry.insert(0, account['title'])
        
        # 패스워드
        ttk.Label(dialog, text="패스워드:", font=("Arial", 10)).pack(anchor=tk.W, padx=10, pady=(0, 0))
        password_entry = tk.Entry(dialog, font=("Arial", 10), show="*")
        password_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        password_entry.insert(0, account['password'])
        
        # ID 필드 선택자
        ttk.Label(dialog, text="ID 필드 선택자:", font=("Arial", 10)).pack(anchor=tk.W, padx=10, pady=(0, 0))
        id_field_entry = tk.Entry(dialog, font=("Arial", 10))
        id_field_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        id_field_entry.insert(0, account['id_field_selector'])
        
        # 패스워드 필드 선택자
        ttk.Label(dialog, text="패스워드 필드 선택자:", font=("Arial", 10)).pack(anchor=tk.W, padx=10, pady=(0, 0))
        pwd_field_entry = tk.Entry(dialog, font=("Arial", 10))
        pwd_field_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        pwd_field_entry.insert(0, account['password_field_selector'])
        
        # 제출 버튼 선택자
        ttk.Label(dialog, text="제출 버튼 선택자:", font=("Arial", 10)).pack(anchor=tk.W, padx=10, pady=(0, 0))
        submit_btn_entry = tk.Entry(dialog, font=("Arial", 10))
        submit_btn_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        submit_btn_entry.insert(0, account['submit_button_selector'])
        
        # 버튼
        def update_account():
            title = title_entry.get().strip()
            password = password_entry.get()
            id_field = id_field_entry.get().strip()
            pwd_field = pwd_field_entry.get().strip()
            submit_btn = submit_btn_entry.get().strip()
            
            if not all([title, password, id_field, pwd_field]):
                messagebox.showerror("오류", "필수 필드를 입력해주세요.\n(제출 버튼은 선택사항입니다)")
                return
            
            if self.credential_manager.update_credential(
                account_id,
                title=title,
                password=password,
                id_field=id_field,
                password_field=pwd_field,
                submit_button=submit_btn
            ):
                messagebox.showinfo("성공", "계정이 업데이트되었습니다.")
                self.refresh_account_list()
                self.account_listbox.select_set(account_id - 1)
                self.on_account_select(None)
                dialog.destroy()
            else:
                messagebox.showerror("오류", "계정 업데이트에 실패했습니다.")
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="수정", command=update_account).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="취소", command=dialog.destroy).pack(side=tk.LEFT, padx=2)
    
    def delete_account(self):
        """계정 삭제"""
        selection = self.account_listbox.curselection()
        if not selection:
            messagebox.showwarning("경고", "삭제할 계정을 선택해주세요.")
            return
        
        account_id = selection[0] + 1
        account = self.credential_manager.get_credential_by_id(account_id)
        
        if messagebox.askyesno("확인", f"'{account['title']}' 계정을 삭제하시겠습니까?\n\n이 작업은 되돌릴 수 없습니다."):
            if self.credential_manager.delete_credential(account_id):
                messagebox.showinfo("성공", "계정이 삭제되었습니다.")
                self.refresh_account_list()
                self.info_text.config(state=tk.NORMAL)
                self.info_text.delete(1.0, tk.END)
                self.info_text.config(state=tk.DISABLED)
            else:
                messagebox.showerror("오류", "계정 삭제에 실패했습니다.")
    
    def show_selector_help(self):
        """선택자 도움말"""
        help_text = self.field_detector.get_css_selector_examples()
        messagebox.showinfo("CSS 선택자 도움말", help_text)
    
    def _show_selector_help_dialog(self):
        """도움말을 별도 창에서 표시"""
        help_text = self.field_detector.get_css_selector_examples()
        
        help_window = tk.Toplevel(self.parent_frame)
        help_window.title("CSS 선택자 도움말")
        help_window.geometry("700x800")
        
        # 텍스트 영역
        text_frame = ttk.Frame(help_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(
            text_frame,
            font=("Courier", 9),
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD
        )
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        
        text_widget.insert(1.0, help_text)
        text_widget.config(state=tk.DISABLED)
    
    def execute_login(self):
        """로그인 실행"""
        url = self.url_entry.get().strip()
        
        # 검증
        if not url or not url.startswith(('http://', 'https://')):
            messagebox.showerror("오류", "유효한 URL을 입력해주세요.")
            return
        
        # 계정 선택 확인
        selection = self.account_listbox.curselection()
        if not selection:
            messagebox.showwarning("경고", "사용할 계정을 선택해주세요.")
            return
        
        account_id = selection[0] + 1
        account = self.credential_manager.get_credential_by_id(account_id)
        
        # 선택자 검증
        if not account['id_field_selector'] or not account['password_field_selector']:
            messagebox.showerror("오류", "계정에 ID/패스워드 필드 선택자가 설정되지 않았습니다.\n계정을 편집해서 필드 선택자를 설정해주세요.")
            return
        
        # UI 상태 업데이트
        self.is_logging_in = True
        self.login_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.progress.start()
        self.update_status("로그인 진행 중...", "green")
        
        # 별도 스레드에서 로그인 실행
        thread = threading.Thread(
            target=self._login_thread,
            args=(url, account['username'], account['password'], 
                  account['id_field_selector'], account['password_field_selector'], 
                  account['submit_button_selector'], self.skip_submit_button_var.get(),
                  self.keep_browser_open_var.get()),
            daemon=True
        )
        thread.start()
    
    def _login_thread(self, url, username, password, id_selector, pwd_selector, submit_selector, skip_submit_button, keep_browser_open):
        """로그인 스레드"""
        try:
            self.log_result("로그인 시작...")
            
            self.login_executor = LoginExecutor(
                url,
                driver_path="./webdriverset",
                headless=self.headless_var.get(),
                browser=self.browser_var.get()
            )
            
            self.log_result(f"브라우저 초기화 중... ({self.browser_var.get().upper()})")
            self.login_executor.setup_driver()
            
            self.log_result("페이지 로드 중...")
            if not self.login_executor.load_page():
                self.log_result(f"실패: {self.login_executor.login_result}")
                return
            
            self.log_result("로그인 필드 입력 중...")
            result = self.login_executor.execute_login(
                username, password, id_selector, pwd_selector, submit_selector, skip_submit_button
            )
            
            if result['success']:
                self.log_result("✓ 로그인 성공!")
                self.log_result(f"원래 URL: {result['original_url']}")
                self.log_result(f"변경된 URL: {result['final_url']}")
                self.update_status("로그인 성공", "green")
            else:
                self.log_result(f"✗ {result['message']}")
                self.log_result(f"원래 URL: {result['original_url']}")
                self.log_result(f"현재 URL: {result['final_url']}")
                self.update_status("로그인 완료 (확인 필요)", "orange")
        
        except Exception as e:
            self.log_result(f"오류: {str(e)}")
            self.update_status("오류 발생", "red")
        
        finally:
            if not keep_browser_open:
                if self.login_executor:
                    self.log_result("브라우저 종료...")
                    self.login_executor.close_driver()
            else:
                self.log_result("✓ 브라우저가 열려 있습니다. 필요시 수동으로 닫아주세요.")
                self.update_status("브라우저 유지 중", "blue")
            
            self.is_logging_in = False
            self.progress.stop()
            self.login_btn.config(state=tk.NORMAL)
            self.cancel_btn.config(state=tk.DISABLED)
    
    def cancel_login(self):
        """로그인 취소"""
        if self.login_executor and not self.keep_browser_open_var.get():
            self.login_executor.close_driver()
        
        self.is_logging_in = False
        self.progress.stop()
        self.login_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)
        
        if self.keep_browser_open_var.get():
            self.log_result("로그인이 취소되었습니다. (브라우저는 유지됩니다)")
        else:
            self.log_result("로그인이 취소되었습니다.")
        self.update_status("취소됨", "red")
    
    def log_result(self, message):
        """결과 로그 추가"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, message + "\n")
        self.result_text.see(tk.END)
        self.result_text.config(state=tk.DISABLED)
        self.parent_frame.update()
    
    def update_status(self, message, color="blue"):
        """상태 메시지 업데이트"""
        self.status_label.config(text=message, fg=color)
        self.parent_frame.update()
