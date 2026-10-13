import random
import string

def generate_password(length_str, use_upper=False, use_digits=False, use_special=False):
    # 1. 입력값 검증
    if not length_str:
        return "길이를 입력해주세요"
    
    # 공백 포함 여부 확인 (앞뒤 공백이 포함되어 있으면 "숫자만 입력해주세요" 반환)
    # 주의: input().strip()을 미리 하면 안 됨. raw string을 받아야 함.
    if length_str != length_str.strip():
         return "숫자만 입력해주세요"

    try:
        # 정수인지 확인 (소수 포함 시 ValueError가 나거나 int 변환 실패)
        # 하지만 "5.5" 같은 경우 int("5.5")는 ValueError를 던짐.
        # "문자, 소수 포함" 일 때 "숫자만 입력해주세요"라고 해야 함.
        # float()로 변환했을 때 정수가 아니면 소수임.
        val = float(length_str)
        if not val.is_integer():
            return "숫자만 입력해주세요"
        length = int(val)
    except ValueError:
        return "숫자만 입력해주세요"

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