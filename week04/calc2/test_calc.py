 from calc import Calculator
 
 def run_tests():
     cases = [
         ([], "0"),
         (["1", "2", "+", "3", "="], "15"),
         (["2", "+", "3", "*", "4", "="], "20"),
         (["5", "+", "-", "3", "="], "2"),
         (["0", ".", "1", "+", "0", ".", "2", "="], "0.3"),
         (["6", "/", "3", "="], "2"),
         (["7", "/", "2", "="], "3.5"),
         (["5", "/", "0", "="], "0으로 나눌 수 없습니다"),
         (["5", "/", "0", "=", "7"], "0으로 나눌 수 없습니다"),
         (["5", "/", "0", "=", "C"], "0"),
         (["1", ".", ".", "5"], "1.5"),
         (["."], "0."),
         (["0", "0", "7"], "7"),
         (["1", "2", "3", "BS"], "12"),
         (["5", "BS"], "0"),
         (["9", "+/-"], "-9"),
         (["5", "0", "%"], "0.5"),
         (["2", "+", "3", "=", "4"], "4"),
         (["2", "+", "3", "=", "+", "4", "="], "9"),
         (["2", "+", "3", "=", "=", "5"], "5"),
     ]
 
     for inputs, expected in cases:
         calc = Calculator()
         for key in inputs:
             calc.press(key)
         if calc.display != expected:
             print(f"Failed on {' '.join(inputs)}. Expected '{expected}', got '{calc.display}'")
             return
 
     print(f"모든 테스트 통과 ({len(cases)}개)")
 
 if __name__ == "__main__":
     run_tests()
 
 # Let's rewrite test_calc.py to match the exact requirement.