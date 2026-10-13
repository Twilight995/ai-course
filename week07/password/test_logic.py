import logic
import string

def test_generator():
    # 테스트 케이스 정의
    # 형식: (입력_길이_문자열, (대문자, 숫자, 특수문자), 기대값_타입)
    # 타입: "message" (문구 확인), "password" (패턴 확인)
    test_cases = [
        ("", (False, False, False), "길이를 입력해주세요"),
        ("abc", (False, False, False), "숫자만 입력해주세요"),
        ("5.5", (False, False, False), "숫자만 입력해주세요"),
        (" 10 ", (False, False, False), "숫자만 입력해주세요"),
        ("3", (False, False, False), "4~32 사이로 입력해주세요"),
        ("33", (False, False, False), "4~32 사이로 입력해주세요"),
        ("8", (False, False, False), "pattern_lowercase_only"),
        ("12", (True, True, False), "pattern_mixed_lower_upper_digit"),
        ("15", (True, True, True), "pattern_all_included"),
        ("20", (False, True, True), "pattern_mixed_lower_digit_special"),
        ("10", (True, False, True), "pattern_mixed_lower_upper_special"),
        ("30", (True, True, True), "pattern_all_included_strict"),
        ("4", (True, True, True), "pattern_all_included_short"),
        ("32", (False, False, False), "pattern_lowercase_only"),
    ]

    passed_count = 0
    failed_count = 0

    print(f"{'Input':<10} | {'Checks':<20} | {'Expected':<30} | {'Result'}")
    print("-" * 80)

    for length_str, checks, expected in test_cases:
        use_upper, use_digits, use_special = checks
        actual = logic.generate_password(length_str, use_upper, use_digits, use_special)
        
        is_passed = False
        
        if expected.startswith("pattern_"):
            # 패턴 검사
            if isinstance(actual, str) and not actual.startswith("길이를") and not actual.startswith("숫자만") and not actual.startswith("4~32"):
                # 1. 길이 확인
                if len(actual) == int(length_str):
                    # 2. 체크되지 않은 종류의 문자가 포함되었는지 확인
                    forbidden = True
                    if use_upper:
                        if not any(c in string.ascii_uppercase for c in actual): forbidden = False
                    if use_digits:
                        if not any(c in string.digits for c in actual): forbidden = False
                    if use_special:
                        if not any(c in "!@#$%^&*" for c in actual): forbidden = False
                    
                    # 기본 소문자 확인
                    if not any(c in string.ascii_lowercase for c in actual): forbidden = False

                    # 체크하지 않은 종류의 문자가 있는지 검사 (매우 중요)
                    # 만약 use_upper가 False라면, actual에 대문자가 있으면 안 됨.
                    invalid_chars = False
                    if not use_upper and any(c in string.ascii_uppercase for c in actual):
                        invalid_chars = True
                    if not use_digits and any(c in string.digits for c in actual):
                        invalid_chars = True
                    if not use_special and any(c in "!@#$%^&*" for c in actual):
                        invalid_chars = True
                    
                    if not invalid_chars:
                        # pattern 이름에 따른 추가 로직
                        if expected == "pattern_lowercase_only":
                            # 소문자만 있어야 함 (대문자, 숫자, 특수문자 금지)
                            if not any(c in string.ascii_uppercase for c in actual) and \
                               not any(c in string.digits for c in actual) and \
                               not any(c in "!@#$%^&*" for c in actual):
                                is_passed = True
                        elif expected == "pattern_mixed_lower_upper_digit":
                             if any(c in string.ascii_uppercase for c in actual) and \
                                any(c in string.digits for c in actual) and \
                                not any(c in "!@#$%^&*" for c in actual):
                                 is_passed = True
                        elif expected == "pattern_all_included":
                             if any(c in string.ascii_uppercase for c in actual) and \
                                any(c in string.digits for c in actual) and \
                                any(c in "!@#$%^&*" for c in actual):
                                 is_passed = True
                        elif expected == "pattern_mixed_lower_digit_special":
                             if any(c in string.digits for c in actual) and \
                                any(c in "!@#$%^&*" for c in actual) and \
                                not any(c in string.ascii_uppercase for c in actual):
                                 is_passed = True
                        elif expected == "pattern_mixed_lower_upper_special":
                             if any(c in string.ascii_uppercase for c in actual) and \
                                any(c in "!@#$%^&*" for c in actual) and \
                                not any(c in string.digits for c in actual):
                                 is_passed = True
                        elif expected == "pattern_all_included_strict":
                             # "지정된 모든 문자 종류 포함 및 허용된 문자만 사용"
                             if any(c in string.ascii_uppercase for c in actual) and \
                                any(c in string.digits for c in actual) and \
                                any(c in "!@#$%^&*" for c in actual):
                                 is_passed = True
                        elif expected == "pattern_all_included_short":
                             if any(c in string.ascii_uppercase for c in actual) and \
                                any(c in string.digits for c in actual) and \
                                any(c in "!@#$%^&*" for c in actual):
                                 is_passed = True
                        elif expected == "pattern_lowercase_only" and len(actual) == 32:
                             if not any(c in string.ascii_uppercase for c in actual) and \
                                not any(c in string.digits for c in actual) and \
                                not any(c in "!@#$%^&*" for c in actual):
                                 is_passed = True
                        else:
                            # 위에서 명시하지 않은 pattern은 일단 최소 조건만 만족하면 통과로 간주 (단순화)
                            is_passed = True
                    else:
                        is_passed = False
                else:
                    is_passed = False
            else:
                is_passed = False
        else:
            # 메시지 확인
            if actual == expected:
                is_passed = True
            else:
                is_passed = False

        if is_passed:
            passed_count += 1
            status = "PASS"
        else:
            failed_count += 1
            status = "FAIL"
            print(f"FAILED: Input='{length_str}', Checks={checks}, Expected='{expected}', Actual='{actual}'")

        print(f"{length_str:<10} | {str(checks):<20} | {expected:<30} | {status}")

    print("-" * 80)
    print(f"Total Passed: {passed_count}")
    print(f"Total Failed: {failed_count}")

if __name__ == "__main__":
    test_generator()