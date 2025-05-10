import os
import chardet

def convert_to_utf8(filepath):
    # 파일의 원래 인코딩 감지
    with open(filepath, 'rb') as f:
        raw = f.read()
        result = chardet.detect(raw)
        encoding = result['encoding']
    # 감지된 인코딩으로 읽어서 UTF-8로 저장
    with open(filepath, 'r', encoding=encoding, errors='ignore') as f:
        content = f.read()
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

root_dir = r"E:\4.1.2.8_GetWater\Assets"

for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.cs'):
            try:
                convert_to_utf8(os.path.join(subdir, file))
                print(f"{file} 변환 완료")
            except Exception as e:
                print(f"{file} 변환 실패: {e}")