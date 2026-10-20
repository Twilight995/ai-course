# main.py
import flet as ft


def main(page: ft.Page):
    page.window.width = 420
    page.window.height = 600
    page.title = "주차 요금 계산기"
    page.window.resizable = False

    import logic

    total_text = ft.Text(value="합계: 0원", size=20, weight=ft.FontWeight.BOLD)
    in_time_field = ft.TextField(label="입차 시각", width=180)
    out_time_field = ft.TextField(label="출차 시각", width=180)
    time_row = ft.Row(controls=[in_time_field, out_time_field])
    calc_button = ft.Button(content="계산", on_click=lambda e: None, expand=True, height=44, bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)
    # Note: Button content must be a control. The instruction says "Button (텍스트: "계산", 파란 바탕에 흰 글자)". 
    # But in the skeleton, Button(content=...) is used. I'll use Text in content to match skeleton style if needed, 
    # but the skeleton uses `ft.Button(content="실행", ...)` which might be a mistake in skeleton or simplified. 
    # Actually, looking at skeleton: `ft.Button(content="실행", ...)`. Wait, `content` expects a Control. 
    # Let's check if `ft.Button(content=ft.Text("계산"), ...)` is safer or if I should follow skeleton exactly.
    # Skeleton: `ft.Button(content="실행", ...)` -> This actually won't work in real Flet if content is str. 
    # But I must follow "뼈대에 나온 Flet 문법만 쓴다". 
    # Skeleton uses `ft.Button(content="실행", ...)`. I will follow this.

    calc_button = ft.Button(content="계산", on_click=None, expand=True, height=44, bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)
    notice = ft.Text(value="", color=ft.Colors.RED)
    items_list = ft.ListView(expand=True, spacing=4)
    fees = []

    def on_delete(e):
        index = e.control.data
        items_list.controls.pop(index)
        fees.pop(index)
        for i, row in enumerate(items_list.controls):
            row.controls[1].data = i
        total_text.value = logic.calculate_total_sum(fees)
        page.update()

    def on_calculate(e):
        nonlocal fees
        res, err = logic.calculate_parking_fee(in_time_field.value, out_time_field.value)
        if err:
            notice.value = err
            page.update()
            return
        
        notice.value = ""
        fees.append(res["fee"])
        row_text = logic.format_row(res)
        items_list.controls.append(
            ft.Row(controls=[
                ft.Text(value=row_text, expand=True),
                ft.Button(content="삭제", data=len(items_list.controls), on_click=on_delete)
            ])
        )
        total_text.value = logic.calculate_total_sum(fees)
        page.update()

    # Re-assigning the button with the actual function since I can't define it inline easily while following the "skeleton" constraint strictly if it means I can't even use lambda? 
    # No, I can define functions.
    calc_button.on_click = on_calculate

    page.add(
        total_text,
        time_row,
         ft.Row(controls=[calc_button]),
        notice,
        items_list
    )


ft.run(main)