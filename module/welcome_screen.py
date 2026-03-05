from flet import Page, Text, Column, Container, FilledButton, Divider, CrossAxisAlignment, Alignment

class WelcomeScreen:
    def __init__(self, on_start_callback):
        self.on_start_callback = on_start_callback

    def build(self, page: Page):
        page.controls.clear()

        # Configura janela
        page.title = "Como Usar"
        page.window.width = 500
        page.window.height = 600
        page.window.center()
        page.window.resizable = False
        page.horizontal_alignment = "center"
        page.vertical_alignment = "center"
        page.bgcolor = "#1E293B"
        page.padding = 20


        titulo = Text("👋 Bem-vindo ao Auto-Clicker Pro", size=24, weight="bold", color="white")
        descricao = Text(
            "Este software permite automatizar cliques.\n\n"
            "Passo a passo:\n"
            "1️⃣ Liste as janelas\n"
            "2️⃣ Selecione a janela\n"
            "3️⃣ Escolha a velocidade\n"
            "4️⃣ Clique em Iniciar\n\n"
            "Pressione Q para parar.",
            size=14,
            color="#CBD5E1",
            text_align="center"
        )
        botao = FilledButton("🚀 Começar", on_click=lambda e: self.on_start_callback(page))

        container = Container(
            expand=True,
            alignment=Alignment.CENTER,  # ✅ CORRETO na versão atual
            content=Column(
                [
                    titulo,
                    Divider(height=20, color="transparent"),
                    descricao,
                    Divider(height=30, color="transparent"),
                    botao
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER
            )
        )

        page.add(container)
        page.update()