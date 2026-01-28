"""
필드 정보 관리 모듈
로그인 필드 선택자 정보를 저장/관리
"""


class FieldDetector:
    """로그인 필드 선택자 관리 클래스"""
    
    def __init__(self):
        """초기화"""
        self.id_field_selector = ""
        self.password_field_selector = ""
        self.submit_button_selector = "button[type='submit']"  # 기본값
    
    def validate_selectors(self):
        """
        선택자 유효성 검증
        
        Returns:
            tuple: (bool, str) - (유효 여부, 메시지)
        """
        if not self.id_field_selector.strip():
            return False, "ID 필드 선택자를 입력해주세요."
        
        if not self.password_field_selector.strip():
            return False, "패스워드 필드 선택자를 입력해주세요."
        
        if not self.submit_button_selector.strip():
            return False, "제출 버튼 선택자를 입력해주세요."
        
        return True, "유효한 선택자입니다."
    
    def get_css_selector_examples(self):
        """
        CSS 선택자 사용 예시 반환
        
        Returns:
            str: 예시 텍스트
        """
        examples = """
╔════════════════════════════════════════════════════════════════════════╗
║              CSS 선택자 사용 방법 및 실제 예시                           ║
╚════════════════════════════════════════════════════════════════════════╝

【 기본 선택자 문법 】

1. ID로 선택 (#)
   선택자: #username
   HTML: <input id="username" type="text">

2. CLASS로 선택 (.)
   선택자: .login-input
   HTML: <input class="login-input" type="text">

3. 속성으로 선택 ([])
   선택자: input[name='id']
   HTML: <input name="id" type="text">

4. 태그+속성 조합
   선택자: input[type='text']
   HTML: <input type="text">


【 실제 웹사이트 예시 】

【 네이버 (naver.com) 】
  ID필드:        input[name='id']
  패스워드필드:   input[name='pw']
  제출버튼:      button[type='submit']

【 카카오 (kakao.com) 】
  ID필드:        input[name='email']
  패스워드필드:   input[type='password']
  제출버튼:      button.btn-login

【 GitHub (github.com) 】
  ID필드:        input#login_field
  패스워드필드:   input#password
  제출버튼:      input[type='submit']

【 Gmail (gmail.com) 】
  ID필드:        input[type='email']
  패스워드필드:   input[type='password']
  제출버튼:      button[type='submit']

【 Twitter/X (twitter.com) 】
  ID필드:        input[autocomplete='username']
  패스워드필드:   input[autocomplete='current-password']
  제출버튼:      button[data-testid='octa-loginButton']


【 선택자 찾는 방법 】

1. 브라우저 개발자 도구 열기
   - Windows/Linux: F12 또는 Ctrl+Shift+I
   - Mac: Command+Option+I

2. Elements/Inspector 탭에서 요소 검사
   - 로그인 창의 ID 입력 필드 우클릭
   - "검사" 또는 "Inspect" 선택

3. HTML 코드에서 확인
   예:
   <input type="text" id="username" name="username" class="form-input">
   
   사용 가능한 선택자:
   - #username       (ID 사용)
   - input#username  (태그+ID)
   - [name='username'] (속성 사용)
   - .form-input     (클래스 사용)

4. 선택자 테스트 (개발자 도구 Console)
   document.querySelector('입력한선택자')
   - 요소가 나타나면 올바른 선택자
   - null이면 잘못된 선택자


【 자주 사용하는 패턴 】

ID 필드:
  ✓ input[name='id']
  ✓ input[name='username']
  ✓ input[name='email']
  ✓ input[name='account']
  ✓ input[type='text']
  ✓ #login_id
  ✓ #username

패스워드 필드:
  ✓ input[type='password']
  ✓ input[name='password']
  ✓ input[name='pwd']
  ✓ input[name='passwd']
  ✓ #password
  ✓ #pw

제출 버튼:
  ✓ button[type='submit']
  ✓ input[type='submit']
  ✓ button.login-btn
  ✓ button#login
  ✓ button[data-action='login']


【 주의사항 】

⚠ 선택자는 정확해야 함
  ✓ 올바름: input[name='id']
  ✗ 틀림: input[name=id]  (따옴표 필요)

⚠ 공백 주의
  - 입력할 때 공백이 없어야 함
  - 예: input[name='id'] (O)
  - 예: input[name='id'] (X)

⚠ 대소문자 구분
  - HTML 속성값은 대소문자를 구분할 수 있음
  - 정확하게 입력해야 함


【 어려우면 이렇게 하세요! 】

1. ID 필드에 "input[type='text']" 입력
   (첫 번째 text 입력 필드를 선택)

2. 패스워드 필드에 "input[type='password']" 입력
   (패스워드 필드는 보통 type='password')

3. 제출 버튼에 "button[type='submit']" 입력
   (표준 제출 버튼)

이 세 가지만으로도 대부분의 웹사이트에서 작동합니다!
        """
        return examples.strip()
    
    def set_selectors(self, id_field, password_field, submit_button="button[type='submit']"):
        """
        선택자 설정
        
        Args:
            id_field: ID 필드 CSS 선택자
            password_field: 패스워드 필드 CSS 선택자
            submit_button: 제출 버튼 CSS 선택자
        """
        self.id_field_selector = id_field.strip()
        self.password_field_selector = password_field.strip()
        self.submit_button_selector = submit_button.strip()
    
    def get_selectors(self):
        """
        현재 선택자 반환
        
        Returns:
            dict: 선택자 정보
        """
        return {
            "id_field": self.id_field_selector,
            "password_field": self.password_field_selector,
            "submit_button": self.submit_button_selector
        }
