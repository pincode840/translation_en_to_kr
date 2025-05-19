import os
import re
import time
from googletrans import Translator

# 번역기 초기화
translator = Translator()

# 대상 디렉토리 설정
directory = r"C:\Files"

# 모든 파일(.rpy) 찾기
for filename in os.listdir(directory):
    if filename.endswith(".rpy"):
        file_path = os.path.join(directory, filename)
        
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # 문자열 패턴 찾기 (큰따옴표 안의 문장)
        def translate_match(match):
            original_text = match.group(1).strip()

            # === 예외 조건 ===
            if (
                re.fullmatch(r"\{/?[a-zA-Z]+\}", original_text) or  # {/i}, {b}
                re.fullmatch(r"\([a-zA-Z\s]+\)", original_text) or  # (whispers)
                re.fullmatch(r"[a-zA-Z]+", original_text) or        # 단어 하나
                re.search(r"\.(png|jpg|jpeg|gif|webp|mp3|ogg|wav)", original_text) or  # 확장자 포함 문자열
                re.search(r"[\\/]", original_text)  # 슬래시 포함 (경로처럼 보일 때)
            ):
                return match.group(0)

            try:
                time.sleep(0.1)  # API 요청 제한 방지
                translated_text = translator.translate(original_text, src="en", dest="ko").text
                if translated_text:
                    return f'"{translated_text}"'
            except Exception as e:
                print(f"Error translating: {original_text} - {e}")

            return match.group(0)  # 번역 실패 시 원문 유지

        # 번역 적용
        updated_content = re.sub(r'"(.*?)"', translate_match, content)

        # 변경된 내용 저장
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(updated_content)

        print(f"Translated: {filename}")
