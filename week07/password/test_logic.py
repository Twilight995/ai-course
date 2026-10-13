import logic
import string


def test_all():
    test_cases = [
        # (입력값, 대문자, 숫자, 특수문자, 기대 결과 타입, 빼기)
        # 타입: "msg" (문구 기대), "pwd" (비밀번호 기대)
        ("", False, False, False, "길이를 입력해주세요", False),
        ("abc", False, False, False, "숫자만 입력해주세요", False),
        ("5.5", False, False, False, "숫자만 입력해주세요", False),
        (" 10 ", False, False, False, "숫자만 입력해주세요", False),
        ("3", False, False, False, "4~32 사이로 입력해주세요", False),
        ("33", False, False, False, "4~32 사이로 입력해주세요", False),
        ("8", False, False, False, "pwd", False),  # 기대: 길이 8, 소문자만 포함
        ("12", True, True, False, "pwd", False),   # 기대: 길이 12, 소문자+대문자+숫자
        ("15", True, True, True, "pwd", False),   # 기대: 길이 15, 소문자+대문자+숫자+특수문자
        ("20", False, True, True, "pwd", False), # 기대: 길이 20, 소문자+숫자+특수문자
        ("10", True, False, True, "pwd", False),  # 기대: 길이 10, 소문자+대문자+특수문자
        ("30", True, True, True, "pwd", False),   # 기대: 길이 30, 모든 종류 포함 및 허용된 문자만
        ("4", True, True, True, "pwd", False),   # 기대: 길이 4, 소문자+대문자+숫자+특수문자
        ("32", False, False, False, "pwd", False),# 기대: 길이 32, 소문자만 포함
        ("12.0", False, False, False, "숫자만 입력해주세요", False),
        ("1e1", False, False, False, "숫자만 입력해주세요", False),
        ("32", True, True, True, "pwd", True),    # 기대: 길이 32, 네 종류 각각 1개 이상, 0 O o 1 l I 없음
        ("32", False, False, False, "pwd", True), # 기대: 길이 32, 소문자만, o l 없음
        ("4", True, True, True, "pwd", True),     # 기대: 길이 4, 네 종류 각각 1개씩, 0 O o 1 l I 없음
        ("abc", False, False, False, "숫자만 입력해주세요", True),  # 빼기는 판정에 영향 없음
    ]

    passed_count = 0
    failed_count = 0

    special_chars = "!@#$%^&*"
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    similar_chars = "0Oo1lI"

    print(f"{'No':<3} | {'Input':<32} | {'Expected':<25} | {'Actual':<25} | {'Result'}")
    print("-" * 117)

    for i, (l_str, u, d, s, expected, ex) in enumerate(test_cases, 1):
        actual = logic.generate_password(l_str, u, d, s, ex)
        is_pass = False

        if expected == "pwd":
            # 비밀번호 검사 로직
            try:
                expected_len = int(l_str)
                correct_len = len(actual) == expected_len
                has_lower = any(c in lowercase for c in actual)

                # 체크한 종류 확인
                has_upper = any(c in uppercase for c in actual) if u else False
                has_digit = any(c in digits for c in actual) if d else False
                has_special = any(c in special_chars for c in actual) if s else False

                # 체크한 종류가 적어도 하나씩 있는지 검사 (u, d, s가 True인 경우만)
                check_kinds = True
                if u and not has_upper: check_kinds = False
                if d and not has_digit: check_kinds = False
                if s and not has_special: check_kinds = False

                # 체크하지 않은 종류의 문자가 있는지 검사 (u, d, s가 False인 경우)
                check_unwanted = True
                if not u and any(c in uppercase for c in actual): check_unwanted = False
                if not d and any(c in digits for c in actual): check_unwanted = False
                if not s and any(c in special_chars for c in actual): check_unwanted = False

                # 허용된 문자만 있는지 검사
                allowed = lowercase
                if u: allowed += uppercase
                if d: allowed += digits
                if s: allowed += special_chars
                only_allowed = all(c in allowed for c in actual)

                # 빼기가 켜져 있으면 헷갈리는 글자가 하나도 없는지 검사
                no_similar = not any(c in similar_chars for c in actual) if ex else True

                if correct_len and has_lower and check_kinds and check_unwanted and only_allowed and no_similar:
                    is_pass = True
            except Exception as e:
                is_pass = False
        else:
            # 문구 검사
            if actual == expected:
                is_pass = True

        if is_pass:
            passed_count += 1
            result_str = "PASS"
        else:
            failed_count += 1
            result_str = "FAIL"

        input_info = f"('{l_str}', {u}, {d}, {s}, {ex})"
        exp_info = expected
        act_info = actual

        print(f"{i:<3} | {input_info:<32} | {exp_info:<25} | {act_info:<25} | {result_str}")

    print("-" * 117)
    print(f"Total: {len(test_cases)}, Passed: {passed_count}, Failed: {failed_count}")

if __name__ == "__main__":
    test_all()
