import flet as ft
from services.authService import logout, get_user
from utils.logger import setup_logger

logger = setup_logger()

def home_page(page: ft.Page):
    try:
        user = get_user()
        if not user:
            page.go("/login")
            return

        welcome_text = ft.Text(
            f"Welcome, {user.get('name', 'User')}!",
            size=24,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )
        

        def handle_logout(e):
            try:
                logout()
                logger.info("User logged out successfully")
                page.go("/login")
            except Exception as error:
                logger.error(f"Logout error: {str(error)}")
                page.show_snack_bar(
                    ft.SnackBar(content=ft.Text("Error during logout"))
                )

        logout_button = ft.ElevatedButton(
            "Logout",
            on_click=lambda e: handle_logout(e),
            icon=ft.icons.LOGOUT
        )

        user_info = ft.Column(
            controls=[
                ft.Text(f"Email: {user.get('providerUid')}"),
                ft.Text(f"ID: {user.get('$id')}"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )


        content = ft.Column(
            controls=[
                welcome_text,
                ft.Divider(),
                user_info,
                ft.Container(height=20),
                logout_button
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )

        container = ft.Container(
            content=content,
            padding=20,
            border_radius=10,
            border=ft.border.all(1, ft.colors.OUTLINE),
        )

        page.add(container)

    except Exception as e:
        logger.error(f"Error in home page: {str(e)}")
        page.add(ft.Text("Error loading home page", color="red"))