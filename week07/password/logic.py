import random
import string

def generate_password(length_str, use_upper=False, use_digits=False, use_special=False):
    # 1. 입력값 검증
    if not length_str:
        return "길이를 입력해주세요"

    if length_str != length_str.strip() or not length_str.isdigit():
        return "숫자만 입력해주세요"

    length = int(length_str)

    # 2. 길이 범위 검증
    if length < 4 or length > 32:
        return "4~32 사이로 입력해주세요"

    # 3. 비밀번호 생성 준비
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase if use_upper else ""
    digits = string.digits if use_digits else ""
    special = "!@#$%^&*" if use_special else ""

    all_chars = lowercase + uppercase + digits + special
    
    # 사용 가능한 문자가 소문자만 있는 경우 (모두 체크 해제 시)
    # 규칙: 소문자는 항상 들어간다.
    
    password = []
    
    # 각 필수 문자를 최소 하나씩 보장
    if use_upper:
        password.append(random.choice(uppercase))
    if use_digits:
        password.append(random.choice(digits))
    if use_special:
        password.append(random.choice(special))
    
    # 소문자는 항상 필수
    password.append(random.choice(lowercase))
    
    # 나머지 길이를 채움
    remaining_length = length - len(password)
    for _ in range(remaining_length):
        password.append(random.choice(all_chars))
    
    # 섞기
    random.shuffle(password)
    
    return "".join(password)