import flet as ft
from services.authService import login
from utils.logger import setup_logger
from components.input import create_input_field
from components.divider import create_divider_with_text

logger = setup_logger()

def login_page(page: ft.Page):
    try:
        page.title = "Login - Flet Auth"
        page.theme_mode = ft.ThemeMode.LIGHT

        # Form fields
        email = create_input_field(
            "Email",
            ft.icons.EMAIL_OUTLINED,
            hint_text="Enter your email"
        )
        
        password = create_input_field(
            "Password",
            ft.icons.LOCK_OUTLINE,
            password=True,
            hint_text="Enter your password"
        )

        error_text = ft.Text(color="red", size=12)

        def validate_form():
            if not email.value or not password.value:
                error_text.value = "Please fill in all fields"
                page.update()
                return False
            return True

        def handle_login(e):
            if not validate_form():
                return
            
            login_btn.content.controls[0].visible = False
            login_btn.content.controls[1].visible = True
            page.update()

            try:
                logger.info(f"Attempting login for user: {email.value}")
                session = login(email.value, password.value)
                page.go("/")
                
            except Exception as error:
                logger.error(f"Login error: {str(error)}")
                error_text.value = "Invalid email or password"
            finally:
                login_btn.content.controls[0].visible = True
                login_btn.content.controls[1].visible = False
                page.update()

        def handle_google_login(e):
            google_btn.content.controls[0].visible = False
            google_btn.content.controls[1].visible = True
            page.update()

            try:
                # Uncomment this once `google_auth()` is implemented
                # session = await google_auth()
                # if session:
                #     page.go("/")
                pass
            except Exception as error:
                logger.error(f"Google login error: {str(error)}")
                error_text.value = "Google login failed"
            finally:
                google_btn.content.controls[0].visible = True
                google_btn.content.controls[1].visible = False
                page.update()

        # Buttons
        login_btn = ft.Container(
            content=ft.Stack(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.LOGIN, color=ft.colors.WHITE, size=18),
                            ft.Text("Login", size=14, color=ft.colors.WHITE),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.ProgressRing(
                        width=16,
                        height=16,
                        stroke_width=2,
                        color=ft.colors.WHITE,
                        visible=False,
                    ),
                ],
            ),
            width=300,
            height=42,
            bgcolor=ft.colors.PRIMARY,
            border_radius=8,
            ink=True,
            on_click=lambda e: (handle_login(e)),
            alignment=ft.alignment.center,
        )

        google_btn = ft.Container(
            content=ft.Stack(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Image(
                                src="../icons/google.png",
                                width=20,
                                height=20,
                            ),
                            ft.Text("Continue with Google", size=14),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    ft.ProgressRing(
                        width=16,
                        height=16,
                        stroke_width=2,
                        visible=False,
                    ),
                ],
            ),
            width=300,
            height=42,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=8,
            ink=True,
            on_click=lambda e:(handle_google_login(e)),  # Use `o.run`
            alignment=ft.alignment.center,
        )

        register_btn = ft.TextButton(
            content=ft.Text(
                "Don't have an account? Register",
                size=14,
                color=ft.colors.PRIMARY,
            ),
            on_click=lambda _: page.go("/register"),
        )

        # Layout
        content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Welcome Back!",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.PRIMARY,
                            ),
                            ft.Text(
                                "Sign in to continue",
                                size=14,
                                color="grey",
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                    ),
                    padding=ft.padding.only(bottom=20),
                ),
                error_text,
                email,
                ft.Container(height=10),
                password,
                ft.Container(height=20),
                login_btn,
                ft.Container(height=20),
                create_divider_with_text(),
                ft.Container(height=20),
                google_btn,
                ft.Container(height=10),
                register_btn,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        )

        container = ft.Container(
            content=content,
            width=400,
            padding=30,
            border_radius=10,
            bgcolor=ft.colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLACK12,
            ),
        )

        page.add(
            ft.Container(
                content=container,
                alignment=ft.alignment.center,
                padding=20,
            )
        )

    except Exception as e:
        logger.error(f"Error in login page: {str(e)}")
        page.add(ft.Text("Error loading login page", color="red"))
