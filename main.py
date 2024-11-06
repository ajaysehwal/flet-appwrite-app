import flet as ft
from typing import Callable
from pages.login import login_page
from pages.register import register_page
from pages.home import home_page
from pages.not_found import not_found_page
from services.authService import is_authenticated
from utils.logger import setup_logger
from services.authService import account
logger = setup_logger()

class AppRouter:
    def __init__(self, page: ft.Page):
        self.page = page
        self.routes = {
            "/login": login_page,
            "/register": register_page,
            "/": home_page,
            "404": not_found_page
        }

    def route_guard(self, route: str, handler: Callable) -> None:
        protected_routes = ["/"]
        public_routes = ["/login", "/register"]
        is_auth = is_authenticated()
        logger.info(f"Route Guard | Route: {route} | Authenticated: {is_auth}")
        if route in protected_routes and not is_auth:
            logger.info(f"Unauthorized access attempt to {route}. Redirecting to /login.")
            self.page.go("/login")
            return
        if route in public_routes and is_auth:
            logger.info(f"Authenticated user accessing {route}. Redirecting to home.")
            self.page.go("/")
            return
        logger.info(f"Authorized access to {route}. Loading page.")
        handler(self.page)

    def handle_routing(self, route: str) -> None:
        """Handle route changes and apply guards"""
        self.page.clean()
        route = route or "/login"
        
        try:
            handler = self.routes.get(route, self.routes["404"])
            self.route_guard(route, handler)
            self.page.update()
        except Exception as e:
            logger.error(f"Routing error: {str(e)}")
            self.page.go("/login")

def main(page: ft.Page):
    page.title = "Flet Appwrite Auth"
    page.theme_mode = "light"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20
    page.spacing = 20
    def error_boundary(error: Exception):
        logger.error(f"Application error: {str(error)}")
        page.clean()
        page.add(
            ft.Text("An error occurred. Please try again later.", color="red"),
            ft.ElevatedButton("Reload", on_click=lambda _: page.clean())
        )
        page.update()

    try:
        router = AppRouter(page)
        
        def route_change(e):
            logger.info(f"Route Change Triggered | New Route: {e.route}")
            router.handle_routing(e.route)
        
        page.on_route_change = route_change
        is_auth = is_authenticated()
        logger.info(f"Initial Authentication Status: {is_auth}")
        initial_route = "/" if is_auth else "/login"
        
        page.go(initial_route)
    except Exception as e:
        error_boundary(e)

ft.app(target=main)
