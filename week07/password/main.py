# main.py
import flet as ft


def main(page: ft.Page):
    page.title = "예제"
    page.window.width = 360
    page.window.height = 440
    page.window.resizable = False

    value = ft.TextField(label="값", value="", width=150)
    unit = ft.Dropdown(label="단위", value="cm", width=120,
                       options=[ft.dropdown.Option("cm"), ft.dropdown.Option("m")])
    upper = ft.Checkbox(label="대문자 포함", value=True)
    result = ft.Text(value="", size=20, weight=ft.FontWeight.BOLD)
    notice = ft.Text(value="", color=ft.Colors.RED)
    items = ft.ListView(expand=True, spacing=4)

    def on_run(e):
        notice.value = ""
        if not value.value.strip():
            notice.value = "값을 입력합니다"
        else:
            result.value = f"{value.value} {unit.value}, 대문자 {upper.value}"
            items.controls.append(ft.Row(controls=[
                ft.Text(value=result.value, expand=True),
                ft.Button(content="삭제", data=len(items.controls), on_click=on_delete),
            ]))
        page.update()

    def on_delete(e):
        items.controls.pop(e.control.data)     # 버튼을 만들 때 data에 넣어 둔 번호
        for i, row in enumerate(items.controls):
            row.controls[1].data = i
        page.update()

    page.add(
        ft.Row(controls=[value, unit]),
        upper,
        ft.Button(content="실행", on_click=on_run, expand=True, height=44,
                  bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE),
        result,
        notice,
        items,
    )


ft.run(main)
