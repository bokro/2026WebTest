"""
계정 정보 관리 모듈
ID와 패스워드를 암호화하여 저장/관리
"""

import json
import os
from cryptography.fernet import Fernet
from pathlib import Path


class CredentialManager:
    """암호화된 계정 정보 관리 클래스"""
    
    def __init__(self, data_dir="loginModule/data"):
        """
        초기화
        
        Args:
            data_dir: 데이터 저장 디렉토리
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.key_file = self.data_dir / "encryption.key"
        self.credentials_file = self.data_dir / "credentials.json"
        
        # 암호화 키 로드 또는 생성
        self.cipher_suite = self._setup_encryption()
    
    def _setup_encryption(self):
        """암호화 키 설정"""
        if self.key_file.exists():
            with open(self.key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
        
        return Fernet(key)
    
    def _load_credentials(self):
        """저장된 계정 정보 로드"""
        if self.credentials_file.exists():
            with open(self.credentials_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"accounts": []}
    
    def _save_credentials(self, credentials):
        """계정 정보 저장"""
        with open(self.credentials_file, 'w', encoding='utf-8') as f:
            json.dump(credentials, f, ensure_ascii=False, indent=2)
    
    def _encrypt(self, text):
        """텍스트 암호화"""
        return self.cipher_suite.encrypt(text.encode()).decode()
    
    def _decrypt(self, encrypted_text):
        """텍스트 복호화"""
        return self.cipher_suite.decrypt(encrypted_text.encode()).decode()
    
    def add_credential(self, title, site_url, username, password):
        """
        새로운 계정 추가
        
        Args:
            title: 계정 타이틀 (예: "네이버", "구글")
            site_url: 웹사이트 URL
            username: 사용자명/ID
            password: 패스워드
        
        Returns:
            bool: 성공 여부
        """
        try:
            credentials = self._load_credentials()
            
            # ID 필드 태그 정보 저장 필요
            new_account = {
                "id": len(credentials["accounts"]) + 1,
                "title": title,
                "site_url": site_url,
                "username": username,
                "password_encrypted": self._encrypt(password),
                "id_field_selector": "",      # 나중에 설정
                "password_field_selector": "", # 나중에 설정
                "submit_button_selector": ""   # 나중에 설정
            }
            
            credentials["accounts"].append(new_account)
            self._save_credentials(credentials)
            return True
        except Exception as e:
            print(f"계정 추가 실패: {str(e)}")
            return False
    
    def get_all_credentials(self):
        """
        모든 계정 정보 조회 (ID와 타이틀만)
        
        Returns:
            list: [{"id": 1, "title": "네이버"}, ...]
        """
        credentials = self._load_credentials()
        return [{"id": acc["id"], "title": acc["title"]} 
                for acc in credentials["accounts"]]
    
    def get_credential_by_id(self, account_id):
        """
        ID로 계정 정보 조회 (복호화)
        
        Args:
            account_id: 계정 ID
        
        Returns:
            dict: 계정 정보 (암호화 해제됨)
        """
        credentials = self._load_credentials()
        
        for account in credentials["accounts"]:
            if account["id"] == account_id:
                account_copy = account.copy()
                account_copy["password"] = self._decrypt(account["password_encrypted"])
                del account_copy["password_encrypted"]
                return account_copy
        
        return None
    
    def update_credential(self, account_id, title=None, password=None, 
                         id_field=None, password_field=None, submit_button=None):
        """
        계정 정보 수정
        
        Args:
            account_id: 계정 ID
            title: 타이틀
            password: 패스워드
            id_field: ID 필드 선택자
            password_field: 패스워드 필드 선택자
            submit_button: 제출 버튼 선택자
        
        Returns:
            bool: 성공 여부
        """
        try:
            credentials = self._load_credentials()
            
            for account in credentials["accounts"]:
                if account["id"] == account_id:
                    if title:
                        account["title"] = title
                    if password:
                        account["password_encrypted"] = self._encrypt(password)
                    if id_field:
                        account["id_field_selector"] = id_field
                    if password_field:
                        account["password_field_selector"] = password_field
                    if submit_button:
                        account["submit_button_selector"] = submit_button
                    
                    self._save_credentials(credentials)
                    return True
            
            return False
        except Exception as e:
            print(f"계정 수정 실패: {str(e)}")
            return False
    
    def delete_credential(self, account_id):
        """
        계정 삭제
        
        Args:
            account_id: 계정 ID
        
        Returns:
            bool: 성공 여부
        """
        try:
            credentials = self._load_credentials()
            
            credentials["accounts"] = [
                acc for acc in credentials["accounts"] 
                if acc["id"] != account_id
            ]
            
            # ID 재정렬
            for i, account in enumerate(credentials["accounts"], 1):
                account["id"] = i
            
            self._save_credentials(credentials)
            return True
        except Exception as e:
            print(f"계정 삭제 실패: {str(e)}")
            return False
    
    def get_username_by_id(self, account_id):
        """
        계정 ID로 사용자명 조회 (UI 노출용)
        
        Args:
            account_id: 계정 ID
        
        Returns:
            str: 사용자명
        """
        account = self.get_credential_by_id(account_id)
        return account["username"] if account else None
