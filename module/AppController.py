from flet import app, Page
from auto_clicker import Auto_Clicker
from module.welcome_screen import WelcomeScreen

class AppController:
    def __init__(self):
        self.auto_clicker = Auto_Clicker()
        self.welcome_screen = WelcomeScreen(self.start_main_app)

    def start_main_app(self, page: Page):
        self.auto_clicker._tela(page)

    def main(self, page: Page):
        page.title = "Auto-Clicker Pro"
        page.bgcolor = "#1E293B"
        self.welcome_screen.build(page)

if __name__ == "__main__":
    controller = AppController()
    app(target=controller.main)