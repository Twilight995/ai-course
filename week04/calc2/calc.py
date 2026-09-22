 class Calculator:
     def __init__(self):
         self.display = "0"
         self.current_input = "0"  # The number being typed
         self.running_total = None  # The result of previous operations
         self.operator = None       # The current operator
         self.is_result_displayed = False
         self.error_state = False
 
     def _format_display(self, value: float) -> str:
         # Rule 6: Round to 10 decimal places, then strip trailing zeros and unnecessary decimal point.
         formatted = f"{value:.10f}"
         if "." in formatted:
             formatted = formatted.rstrip("0").rstrip(".")
         if formatted == "" or formatted == "-0":
             return "0"
         return formatted
 
     def press(self, key: str) -> str:
         if self.error_state:
             if key == "C":
                 self.__init__()
             return self.display
 
         if key == "C":
             self.__init__()
             return self.display
 
         if key == "=":
             if self.operator and self.running_total is not None and self.current_input != "":
                 # Perform final calculation
                 try:
                     val2 = float(self.current_input)
                     if self.operator == "+": res = self.running_total + val2
                     elif self.operator == "-": res = self.running_total - val2
                     elif self.operator == "*": res = self.running_total * val2
                     elif self.operator == "/":
                         if val2 == 0:
                             self.error_state = True
                             self.display = "0으로 나눌 수 없습니다"
                             return self.display
                         res = self.running_total / val2
                     
                     self.display = self._format_display(res)
                     self.running_total = res
                     self.current_input = ""
                     self.operator = None
                     self.is_result_displayed = True
                 except ZeroDivisionError:
                     self.error_state = True
         if key in ("+", "-", "*", "/"):
             if self.is_result_displayed:
                 self.running_total = float(self.display)
                 self.current_input = ""
                 self.operator = key
                 self.is_result_displayed = False
             else:
                 if self.operator and self.current_input == "":
                     self.operator = key
                     return self.display
                 
                 if self.operator and self.running_total is not None and self.current_input != "":
                     try:
                         val2 = float(self.current_input)
                         if self.operator == "+": self.running_total += val2
                         elif self.operator == "-": self.running_total -= val2
                         elif self.operator == "*": self.running_total *= val2
                         elif self.operator == "/":
                             if val2 == 0:
                                 self.error_state = True
                                 self.display = "0으로 나눌 수 없습니다"
                                 return self.display
                             self.running_total /= val2
                         self.display = self._format_display(self.running_total)
                     except ZeroDivisionError:
                         self.error_state = True
                         self.display = "0으로 나눌 수 없습니다"
                         return self.display
                 else:
                     if self.running_total is None:
                         self.running_total = float(self.current_input) if self.current_input != "" and self.current_input != "0" else 0.0
                     else:
                         # This case should be covered by the 'if self.operator...' above if current_input != ""
                         pass
                 
                 self.operator = key
                 self.current_input = ""
                 self.is_result_displayed = False
             return self.display
                     else:
                         # We already have a running total, so we just set the operator
                         pass
                 
                 self.operator = key
                 self.current_input = ""
                 self.is_result_displayed = False
             return self.display
 
         if key == "BS":
             if self.is_result_displayed:
                 return self.display
             if self.current_input == "0":
                 self.current_input = "0"
             else:
                 self.current_input = self.current_input[:-1]
                 if self.current_input == "":
                     self.current_input = "0"
             self.display = self.current_input
             return self.display
         if key == "+/-":
             if self.is_result_displayed:
                 return self.display
             if self.current_input != "0":
                 if self.current_input.startswith("-"):
                     self.current_input = self.current_input[1:]
                 else:
                     self.current_input = "-" + self.current_input
             else:
                 self.current_input = "-0"
             self.display = self._format_display(float(self.current_input))
             # Wait, if I use _format_display, it might strip "-0" to "0".
             # The spec says "9 +/-" -> "-9". 
             # If current_input was "9", it becomes "-9".
             # If it was "0", it becomes "-0", which format_display makes "0".
             # Actually, let's just update the display directly.
             self.display = self.current_input
             # Let's re-check if -0 should be 0 or -0. Usually 0.
             if self.display == "-0": self.display = "0"
             return self.display
 
         if key == "+/-":
             if self.is_result_displayed:
                 return self.display
             if self.current_input != "0":
                 if self.current_input.startswith("-"):
                     self.current_input = self.current_input[1:]
                 else:
                     self.current_input = "-" + self.current_input
             else:
                 self.current_input = "-0" # Will be formatted to "-0" or "0" later
             self.display = self.current_input
             return self.display
 
         if key == "%":
             val = float(self.current_input) if self.current_input != "0" or self.is_result_displayed else 0.0
             # If it's just "0", 0 / 100 = 0.
             if self.current_input == "0" and not self.is_result_displayed:
                 val = 0.0
             elif self.current_input == "0" and self.is_result_displayed:
                 val = float(self.display)
             else:
                 val = float(self.current_input)
                 
             res = val / 100.0
             self.display = self._format_display(res)
             self.current_input = self.display
             self.is_result_displayed = True
             return self.display
 
         # Numbers and dot
         if key.isdigit() or key == ".":
             if self.is_result_displayed:
                 self.__init__()
                 self.is_result_displayed = False
             
             if self.current_input == "0" and key != ".":
                 self.current_input = key
             elif key == ".":
                 if "." not in self.current_input:
                     self.current_input += "."
                 else:
                     return self.display
             else:
                 digits_only = "".join(c for c in self.current_input if c.isdigit())
                 if len(digits_only) < 12:
                     self.current_input += key
                 else:
                     return self.display
             
             if len(self.current_input) > 1 and self.current_input.startswith("0") and self.current_input[1] != ".":
                 self.current_input = self.current_input.lstrip("0")
                 if self.current_input == "" or self.current_input.startswith("."):
                     self.current_input = "0" + self.current_input
                     
             self.display = self.current_input
             return self.display
 
         return self.display
 
     def _process_key(self, key):
         pass
 
         # Numbers and dot
         if key.isdigit() or key == ".":
             if self.is_result_displayed:
                 # Rule 8: If number pressed after '=', start new calculation
                 self.__init__()
                 self.is_result_displayed = False
             
             if self.current_input == "0" and key != ".":
                 self.current_input = key
             elif key == ".":
                 if "." not in self.current_input:
                     self.current_input += "."
                 else:
                     return self.display # Ignore second dot
             else:
                 # Rule 11: Max 12 digits (excluding sign and dot)
                 # Let's count only digits
                 digits_only = "".join(c for c in self.current_input if c.isdigit())
                 if len(digits_only) < 12:
                     self.current_input += key
                 else:
                     return self.display
             
             # Rule 5: Remove leading zeros (except for "0.")
             if len(self.current_input) > 1 and self.current_input.startswith("0") and self.current_input[1] != ".":
                 self.current_input = self.current_input.lstrip("0")
                 if self.current_input == "" or self.current_input.startswith("."):
                     self.current_input = "0" + self.current_input
                     
             self.display = self.current_input
             return self.display
 
         return self.display
     def _process_key(self, key):
         # Re-implementing inside _process_key for clarity
         pass
 
 # I will rewrite this properly in the next step.