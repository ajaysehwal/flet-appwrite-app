import flet as ft

def create_input_field(
    label: str,
    icon: str,
    password: bool = False,
    hint_text: str = None
) -> ft.TextField:
    return ft.TextField(
        label=label,
        hint_text=hint_text,
        password=password,
        can_reveal_password=password,
        prefix_icon=icon,
        width=300,
        border_radius=8,
        border_color=ft.colors.OUTLINE,
        focused_border_color=ft.colors.PRIMARY,
        text_size=14,
        height=48,
    )

