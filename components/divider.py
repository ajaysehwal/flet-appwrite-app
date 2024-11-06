import flet as ft

def create_divider_with_text() -> ft.Row:
    return ft.Row(
        controls=[
            ft.Container(
                content=ft.Divider(
                    color=ft.colors.OUTLINE,
                ),
                expand=True,
                margin=ft.margin.symmetric(horizontal=16),
            ),
            ft.Text(
                "OR",
                size=12,
                color="grey",
            ),
            ft.Container(
                content=ft.Divider(
                    color=ft.colors.OUTLINE,
                ),
                expand=True,
                margin=ft.margin.symmetric(horizontal=16),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )