"""
Unity 툴킷 메인 실행 파일

python -m unity_toolkit 명령으로 실행할 수 있도록 하는 진입점입니다.
"""

from .cli.main_cli import main_cli

if __name__ == "__main__":
    main_cli() 