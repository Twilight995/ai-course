# main.py
import logic
import flet as ft


def main(page: ft.Page):
    page.title = "비밀번호 생성기"
    page.window.width = 360
    page.window.height = 440
    page.window.resizable = False

    length_input = ft.TextField(label="길이", width=200)
    upper_check = ft.Checkbox(label="대문자 포함", value=False)
    digit_check = ft.Checkbox(label="숫자 포함", value=False)
    special_check = ft.Checkbox(label="특수문자 포함", value=False)
    
    result_text = ft.Text(value="")
    notice_text = ft.Text(value="", color=ft.Colors.RED)

    def on_generate(e):
        res = logic.generate_password(
            length_input.value,
            upper_check.value,
            digit_check.value,
            special_check.value
        )
        
        if res in logic.ERROR_MESSAGES:
            notice_text.value = res
            result_text.value = ""
        else:
            notice_text.value = ""
            result_text.value = res
        page.update()

    def on_regenerate(e):
        on_generate(None)

    page.add(
        length_input,
        upper_check,
        digit_check,
        special_check,
        ft.Button(content="만들기", on_click=on_generate, expand=True, bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE),
        result_text,
        ft.Button(content="다시 만들기", on_click=on_regenerate, expand=True, bgcolor=ft.Colors.GREY, color=ft.Colors.WHITE),
        notice_text
    )


ft.run(main)
