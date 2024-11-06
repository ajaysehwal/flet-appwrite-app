import flet as ft

def not_found_page(page: ft.Page):
    content = ft.Column(
        controls=[
            ft.Text("404 - Page Not Found", 
                   size=32, 
                   weight=ft.FontWeight.BOLD,
                   text_align=ft.TextAlign.CENTER),
            ft.Text("The page you're looking for doesn't exist.",
                   text_align=ft.TextAlign.CENTER),
            ft.ElevatedButton(
                "Go Home",
                on_click=lambda _: page.go("/"),
                icon=ft.icons.HOME
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    container = ft.Container(
        content=content,
        padding=20,
        border_radius=10,
        border=ft.border.all(1, ft.colors.OUTLINE),
    )

    page.add(container)