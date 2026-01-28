"""
웹사이트 테스트 메인 프로그램
GUI를 통해 버튼 테스트와 자동 로그인 기능을 실행하는 메인 진입점
"""

import tkinter as tk
from ui import MainGUI


def main():
    """메인 실행 함수 - GUI 실행"""
    root = tk.Tk()
    gui = MainGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

