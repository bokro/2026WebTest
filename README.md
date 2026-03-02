# 웹사이트 자동화 테스트 도구

> QA 자동화 테스트를 위한 포트폴리오 프로젝트

## 📋 프로젝트 개요

웹사이트의 UI 요소를 자동으로 테스트하고, 로그인 기능을 자동화하는 Python 기반의 QA 자동화 도구입니다. Selenium WebDriver를 활용하여 실제 브라우저 환경에서 테스트를 수행하며, 사용자 친화적인 GUI를 제공합니다.

### 🎯 주요 기능

1. **버튼 자동 테스트**
   - 웹페이지 내 모든 클릭 가능한 버튼 자동 탐지
   - 각 버튼의 클릭 가능 여부 검증
   - 테스트 결과 실시간 로깅 및 리포트 생성

2. **자동 로그인 테스트**
   - CSS 선택자 기반 로그인 필드 자동 탐지
   - 암호화된 계정 정보 관리 (Fernet 암호화)
   - 다중 계정 저장 및 관리
   - 로그인 성공/실패 자동 검증
   ※ 보안을 위해 테스트에 사용한 계정정보 및 키 값은 삭제

3. **브라우저 지원**
   - Chrome, Edge 브라우저 지원
   - Headless 모드 지원 (백그라운드 실행)

---

## 🏗️ 프로젝트 구조

```
2026WebTest/
├── main.py                    # 메인 진입점
├── ui.py                      # 메인 GUI 인터페이스
├── button_tester.py           # 버튼 테스트 핵심 로직
├── loginModule/               # 로그인 자동화 모듈
│   ├── __init__.py
│   ├── login_ui.py           # 로그인 탭 UI
│   ├── login_executor.py     # 로그인 실행 로직
│   ├── field_detector.py     # CSS 선택자 관리
│   ├── credential_manager.py # 암호화된 계정 정보 관리
│   ├── driver_manager.py     # WebDriver 공통 관리
│   └── data/                 # 암호화된 데이터 저장소
└── webdriverset/             # WebDriver 파일 저장소
    ├── chromedriver.exe
    └── msedgedriver.exe
```

---

## 🔧 기술 스택

### 핵심 라이브러리
- **Selenium WebDriver**: 브라우저 자동화
- **Tkinter**: GUI 인터페이스
- **Cryptography (Fernet)**: 계정 정보 암호화
- **Threading**: 비동기 테스트 실행

### 개발 환경
- Python 3.8+
- Windows OS 최적화

---

## 📦 설치 및 실행

### 1. 필수 패키지 설치

```bash
pip install selenium cryptography
```

### 2. WebDriver 준비

**방법 1: 자동 설정 (권장)**
- 프로그램 실행 시 ChromeDriver Manager가 자동으로 설치

**방법 2: 수동 설정**
```bash
# Chrome WebDriver 다운로드
https://chromedriver.chromium.org/

# Edge WebDriver 다운로드
https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

# webdriverset/ 폴더에 저장
```

### 3. 프로그램 실행

```bash
python main.py
```

---

## 🎮 사용 가이드

### 버튼 테스트 기능

1. **URL 입력**: 테스트할 웹사이트 주소 입력
2. **브라우저 선택**: Chrome 또는 Edge 선택
3. **모드 선택**: 
   - 일반 모드: 브라우저 창이 표시됨
   - Headless 모드: 백그라운드 실행
4. **테스트 시작**: "테스트 시작" 버튼 클릭
5. **결과 확인**: 실시간 로그 및 최종 결과 확인

#### 테스트 결과 항목
```
✓ 클릭 성공: 정상적으로 클릭된 버튼
✗ 클릭 실패: 클릭 불가능한 버튼
⚠ 오류: 예외가 발생한 버튼
```

### 자동 로그인 기능

#### 1단계: 로그인 필드 탐지

```python
# CSS 선택자 예시
ID 필드: input[name="username"]
비밀번호 필드: input[type="password"]
제출 버튼: button[type="submit"]
```

**CSS 선택자 작성 팁**
```css
# ID로 선택
#username

# Class로 선택
.login-input

# Attribute로 선택
input[name="email"]
input[type="password"]

# 복합 선택자
form.login-form input[type="text"]
```

#### 2단계: 계정 정보 관리

1. 계정 추가: ID와 패스워드 입력 후 저장
2. 자동 암호화: Fernet 알고리즘으로 안전하게 저장
3. 계정 선택: 드롭다운에서 테스트할 계정 선택

#### 3단계: 로그인 테스트 실행

1. URL 입력
2. 필드 선택자 설정
3. 계정 선택
4. 로그인 테스트 시작
5. 결과 확인

---

## 🔍 핵심 모듈 설명

### 1. ButtonTester (`button_tester.py`)

버튼 테스트의 핵심 로직을 담당하는 클래스입니다.

```python
class ButtonTester:
    def __init__(self, url, driver_path=None, headless=False, browser="chrome"):
        """버튼 테스트 초기화"""
        
    def find_all_buttons(self):
        """페이지에서 모든 버튼 요소 탐지"""
        # <button>, <input type="button">, role="button" 등 탐지
        
    def test_all_buttons(self):
        """모든 버튼 클릭 테스트 실행"""
        # 각 버튼에 대해 클릭 가능 여부 검증
```

**주요 기능**
- XPath 기반 버튼 탐지: `//button`, `//input[@type='button']`, `//*[@role='button']`
- 중복 제거: 동일한 위치의 버튼 필터링
- 예외 처리: `StaleElementReferenceException`, `ElementClickInterceptedException` 등
- 상세 로깅: 각 버튼의 테스트 결과 기록

### 2. LoginExecutor (`loginModule/login_executor.py`)

로그인 프로세스를 실행하는 클래스입니다.

```python
class LoginExecutor:
    def execute_login(self, id_value, password, field_detector):
        """로그인 실행"""
        # 1. 필드 탐지
        # 2. 값 입력
        # 3. 제출
        # 4. 결과 검증
```

**로그인 검증 메커니즘**
1. URL 변경 확인 (리다이렉션)
2. 오류 메시지 존재 여부 확인
3. 성공 지표 요소 확인 (예: 로그아웃 버튼)

### 3. CredentialManager (`loginModule/credential_manager.py`)

암호화된 계정 정보 관리 클래스입니다.

```python
class CredentialManager:
    def __init__(self, data_dir="loginModule/data"):
        """Fernet 암호화 초기화"""
        
    def save_credential(self, name, id_value, password):
        """계정 정보 암호화 저장"""
        
    def get_all_credentials(self):
        """저장된 모든 계정 조회"""
```

**보안 기능**
- Fernet 대칭키 암호화
- 암호화 키는 별도 파일로 관리 (`encryption.key`)
- 계정 정보는 JSON 형태로 암호화되어 저장 (`credentials.json`)

### 4. DriverManager (`loginModule/driver_manager.py`)

WebDriver 초기화 및 설정을 담당하는 공통 모듈입니다.

```python
class DriverManager:
    @staticmethod
    def setup_driver(browser="chrome", driver_path=None, headless=False):
        """WebDriver 설정 및 자동화 탐지 우회"""
```

**주요 설정**
```python
# Chrome Options
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# User-Agent 설정
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."
options.add_argument(f'user-agent={user_agent}')

# Headless 모드
if headless:
    options.add_argument('--headless')
```

### 5. FieldDetector (`loginModule/field_detector.py`)

CSS 선택자 정보를 관리하고 예시를 제공하는 클래스입니다.

```python
class FieldDetector:
    def validate_selectors(self):
        """선택자 유효성 검증"""
        
    def get_css_selector_examples(self):
        """CSS 선택자 사용 예시 제공"""
```

---

## 🧪 테스트 시나리오 예시

### 시나리오 1: 공개 웹사이트 버튼 테스트

```python
# 테스트 대상: https://example.com
# 목표: 모든 네비게이션 및 액션 버튼 테스트

예상 결과:
✓ 홈 버튼 - 클릭 성공
✓ About 버튼 - 클릭 성공
✓ Contact 버튼 - 클릭 성공
```

### 시나리오 2: 로그인 자동화 테스트

```python
# 테스트 대상: 회원 웹사이트
# 계정: test_user@example.com / TestPass123

단계:
1. 로그인 페이지 접속
2. ID 입력 (CSS: input[name="email"])
3. 비밀번호 입력 (CSS: input[type="password"])
4. 로그인 버튼 클릭 (CSS: button.btn-login)
5. 로그인 성공 확인
```

---

## 📊 QA 역량 시연 포인트

### 1. 자동화 테스트 설계 능력
- Selenium WebDriver를 활용한 E2E 테스트 구현
- 동적 요소 탐지 및 대기 로직 구현 (WebDriverWait)
- 예외 상황 처리 (TimeoutException, StaleElementReference 등)

### 2. 테스트 도구 개발 능력
- 재사용 가능한 테스트 프레임워크 구조 설계
- 모듈화된 코드 구조 (loginModule 패키지)
- 공통 컴포넌트 추상화 (DriverManager)

### 3. 보안 의식
- 민감 정보 암호화 (Fernet)
- 계정 정보 안전한 저장 및 관리

### 4. 사용자 경험 고려
- GUI 기반 직관적인 인터페이스
- 실시간 로그 및 피드백
- 상세한 가이드 제공 (CSS 선택자 예시)

### 5. 크로스 브라우저 테스트
- Chrome, Edge 멀티 브라우저 지원
- 브라우저별 WebDriver 동적 설정

---

## 🔒 보안 고려사항

1. **계정 정보 암호화**
   - Fernet (대칭키 암호화) 사용
   - 암호화 키와 데이터 분리 저장

2. **자동화 탐지 우회**
   - navigator.webdriver 속성 제거
   - User-Agent 설정
   - Automation 플래그 비활성화

3. **데이터 저장**
   - 로컬에만 저장 (외부 전송 없음)
   - `loginModule/data/` 디렉토리에 격리

---

## 🐛 문제 해결 가이드

### 일반적인 오류와 해결방법

**1. WebDriver 오류**
```
selenium.common.exceptions.WebDriverException: 'chromedriver' executable needs to be in PATH
```
해결: WebDriver를 `webdriverset/` 폴더에 저장하거나 경로 직접 지정

**2. 요소 찾기 실패**
```
selenium.common.exceptions.NoSuchElementException
```
해결: CSS 선택자 확인 및 WebDriverWait 사용

**3. 암호화 키 오류**
```
cryptography.fernet.InvalidToken
```
해결: `loginModule/data/` 폴더의 `encryption.key` 및 `credentials.json` 삭제 후 재생성

---

## 🚀 향후 개선 계획

### 단기 목표
- [ ] 테스트 결과 Excel/CSV 내보내기
- [ ] 스크린샷 자동 캡처 기능
- [ ] 테스트 시나리오 저장/불러오기

### 중기 목표
- [ ] 다양한 Assertion 추가 (텍스트, 속성 검증)
- [ ] Firefox, Safari 브라우저 지원
- [ ] 병렬 테스트 실행

### 장기 목표
- [ ] CI/CD 파이프라인 통합
- [ ] 웹 기반 대시보드
- [ ] 테스트 스크립트 레코딩 기능

---

## 📝 라이선스

이 프로젝트는 교육 및 포트폴리오 목적으로 작성되었습니다.

---

## 🎓 학습 참고 자료

### Selenium 공식 문서
- https://www.selenium.dev/documentation/

### CSS 선택자 학습
- https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors

### Cryptography 라이브러리
- https://cryptography.io/en/latest/

---

**마지막 업데이트**: 2026년 1월 29일
