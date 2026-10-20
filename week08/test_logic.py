import logic

def test_calculate_parking_fee_errors():
    test_cases = [
        (("", "10:00"), (None, "입차 시각을 입력해주세요")),
        (("10:00", ""), (None, "출차 시각을 입력해주세요")),
        (("9:5", "10:00"), (None, "입차 시각 형식이 올바르지 않습니다 (예: 09:05)")),
        (("930", "10:00"), (None, "입차 시각 형식이 올바르지 않습니다 (예: 09:05)")),
        (("24:00", "10:00"), (None, "입차 시각 형식이 올바르지 않습니다 (예: 09:05)")),
        (("12:60", "13:00"), (None, "입차 시각 형식이 올바르지 않습니다 (예: 09:05)")),
        (("abc", "10:00"), (None, "입차 시각 형식이 올바르지 않습니다 (예: 09:05)")),
        (("09:00", "25:00"), (None, "출차 시각 형식이 올바르지 않습니다 (예: 09:05)")),
        (("09:00", "09:00"), (None, "출차는 입차보다 뒤여야 합니다")),
        (("abc", ""), (None, "입차 시각 형식이 올바르지 않습니다 (예: 09:05)")),
        (("", ""), (None, "입차 시각을 입력해주세요")),
    ]
    
    passed = 0
    failed = 0
    total = len(test_cases)
    
    for i, (inputs, expected) in enumerate(test_cases):
        actual = logic.calculate_parking_fee(*inputs)
        if actual == expected:
            passed += 1
        else:
            failed += 1
            print(f"Error Case {i+1} Failed:")
            print(f"  Input: {inputs}")
            print(f"  Expected: {expected}")
            print(f"  Actual: {actual}")
            
    return total, passed, failed

def test_calculate_parking_fee_success():
    test_cases = [
        (("09:00", "09:30"), "0시간 30분", 0),
        (("09:00", "09:31"), "0시간 31분", 500),
        (("09:00", "09:40"), "0시간 40분", 500),
        (("09:00", "09:41"), "0시간 41분", 1000),
        (("09:00", "16:10"), "7시간 10분", 20000),
        (("09:00", "16:11"), "7시간 11분", 20000),
        ((" 09:00 ", "10:00"), "1시간 0분", 1500),
        (("23:00", "01:00"), "2시간 0분", 4500),
        (("10:00", "09:00"), "23시간 0분", 20000),
    ]
    
    passed = 0
    failed = 0
    total = len(test_cases)
    
    for i, (inputs, exp_duration, exp_fee) in enumerate(test_cases):
        res_dict, error = logic.calculate_parking_fee(*inputs)
        
        # Check error is None
        # Check duration and fee
        # Check in_time stripped (for leading/trailing spaces, in check if "09:00" is in in_time)
        
        is_valid = (error is None and 
                    res_dict["duration"] == exp_duration and 
                    res_dict["fee"] == exp_fee and
                    "09:00" in inputs[0]) # As per requirement: "앞뒤 공백 줄은 in이 "09:00"인지도 본다."
        
        # Wait, the requirement says: "앞뒤 공백 줄은 in이 "09:00"인지도 본다." 
        # It's specifically for the case where there were spaces. 
        # Let's re-read: "성공 줄은 안내 문구가 None이고, duration과 fee가 표와 같은지 본다. 앞뒤 공백 줄은 in이 "09:00"인지도 본다."
        # This implies for the case (" 09:00 ", "10:00"), we check if res_dict["in"] is "09:00".
        
        # Re-evaluating validation logic for success cases:
        actual_error = error
        actual_duration = res_dict["duration"] if res_dict else None
        actual_fee = res_dict["fee"] if res_dict else None
        actual_in = res_dict["in"] if res_dict else None
        
        # Specific check for the space case
        if inputs[0].strip() == "09:00" and " " in inputs[0]:
            space_check = (actual_in == "09:00")
        else:
            space_check = True

        if actual_error is None and actual_duration == exp_duration and actual_fee == exp_fee and space_check:
            passed += 1
        else:
            failed += 1
            print(f"Success Case {i+1} Failed:")
            print(f"  Input: {inputs}")
            print(f"  Expected: duration={exp_duration}, fee={exp_fee}")
            print(f"  Actual: error={actual_error}, duration={actual_duration}, fee={actual_fee}, in='{actual_in}'")
            
    return total, passed, failed

def test_calculate_total_sum():
    test_cases = [
        ([], "합계: 0원"),
        ([500, 1000, 2000], "합계: 3,500원"),
        ([20000, 500], "합계: 20,500원"),
    ]
    
    passed = 0
    failed = 0
    total = len(test_cases)
    
    for i, (inputs, expected) in enumerate(test_cases):
        actual = logic.calculate_total_sum(inputs)
        if actual == expected:
            passed += 1
        else:
            failed += 1
            print(f"Total Sum Case {i+1} Failed:")
            print(f"  Input: {inputs}")
            print(f"  Expected: {expected}")
            print(f"  Actual: {actual}")
            
    return total, passed, failed

def test_format_row():
    test_cases = [
        ({"in": "09:30", "out": "11:05", "duration": "1시간 35분", "fee": 3500}, "입차 09:30 → 출차 11:05, 1시간 35분, 3,500원"),
        ({"in": "09:00", "out": "09:30", "duration": "0시간 30분", "fee": 0}, "입차 09:00 → 출차 09:30, 0시간 30분, 0원"),
    ]
    
    passed = 0
    failed = 0
    total = len(test_cases)
    
    for i, (inputs, expected) in enumerate(test_cases):
        actual = logic.format_row(inputs)
        if actual == expected:
            passed += 1
        else:
            failed += 1
            print(f"Format Row Case {i+1} Failed:")
            print(f"  Input: {inputs}")
            print(f"  Expected: {expected}")
            print(f"  Actual: {actual}")
            
    return total, passed, failed

if __name__ == "__main__":
    t1, p1, f1 = test_calculate_parking_fee_errors()
    t2, p2, f2 = test_calculate_parking_fee_success()
    t3, p3, f3 = test_calculate_total_sum()
    t4, p4, f4 = test_format_row()
    
    all_total = t1 + t2 + t3 + t4
    all_passed = p1 + p2 + p3 + p4
    all_failed = f1 + f2 + f3 + f4
    
    print(f"전체 {all_total}, 통과 {all_passed}, 실패 {all_failed}")