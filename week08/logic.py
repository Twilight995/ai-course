import math
from datetime import datetime, timedelta

def _validate_time_format(time_str):
    """
    시각 형식을 검사합니다. (HH:MM, 24시간제, 00-23:00-59)
    """
    if ":" not in time_str:
        return False
    
    parts = time_str.split(":")
    if len(parts) != 2:
        return False
    
    h_str, m_str = parts[0], parts[1]
    
    # 반드시 두 자리여야 함
    if len(h_str) != 2 or len(m_str) != 2:
        return False
    
    if not (h_str.isdigit() and m_str.isdigit()):
        return False
    
    hour = int(h_str)
    minute = int(m_str)
    
    if not (0 <= hour <= 23) or not (0 <= minute <= 59):
        return False
    
    return True

def calculate_parking_fee(in_time, out_time):
    # 공백 제거
    in_time = in_time.strip()
    out_time = out_time.strip()
    
    # 1. 입차 빈칸
    if not in_time:
        return (None, "입차 시각을 입력해주세요")
    
    # 2. 입차 형식
    if not _validate_time_format(in_time):
        return (None, "입차 시각 형식이 올바르지 않습니다 (예: 09:05)")
    
    # 3. 출차 빈칸
    if not out_time:
        return (None, "출차 시각을 입력해주세요")
    
    # 4. 출차 형식
    if not _validate_time_format(out_time):
        return (None, "출차 시각 형식이 올바르지 않습니다 (예: 09:05)")
    
    # 시간 파싱
    try:
        fmt = "%H:%M"
        dt_in = datetime.strptime(in_time, fmt)
        dt_out = datetime.strptime(out_time, fmt)
    except ValueError:
        # _validate_time_format에서 이미 체크하지만 안전을 위해
        return (None, "입차 시각 형식이 올바르지 않습니다 (예: 09:05)")

    # 5. 같은 시각
    if dt_in == dt_out:
        return (None, "출차는 입차보다 뒤여야 합니다")

    # 출차가 입차보다 앞선 경우 다음 날로 간주
    if dt_out < dt_in:
        dt_out += timedelta(days=1)
    
    # 주차 시간 계산
    duration_delta = dt_out - dt_in
    total_minutes = int(duration_delta.total_seconds() // 60)
    
    hours = total_minutes // 60
    minutes = total_minutes % 60
    
    # 요금 계산
    # 30분 이하면 0원
    if total_minutes <= 30:
        fee = 0
    else:
        # 30분을 넘으면 (주차 시간 - 30)분을 10분 단위로 올림해서 단위마다 500원
        extra_minutes = total_minutes - 30
        units = math.ceil(extra_minutes / 10)
        fee = units * 500
        
        # 최대 요금 20,000원 제한
        if fee > 20000:
            fee = 20000
            
    result_dict = {
        "in": in_time,
        "out": out_time,
        "duration": f"{hours}시간 {minutes}분",
        "fee": fee
    }
    
    return (result_dict, None)

def calculate_total_sum(fee_list):
    if not fee_list:
        return "합계: 0원"
    
    total = sum(fee_list)
    return f"합계: {total:,}원"

def format_row(result_dict):
    return f"입차 {result_dict['in']} → 출차 {result_dict['out']}, {result_dict['duration']}, {result_dict['fee']:,}원"