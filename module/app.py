from flet import (
    Page, Text, Row, app, Column, Container, MainAxisAlignment,
    FilledButton, CrossAxisAlignment, Dropdown, dropdown, ResponsiveRow,
    Animation, ButtonStyle, RoundedRectangleBorder, Divider, Icon, TextStyle,Image
)
from pyautogui import position, click
import time
from threading import Thread
from keyboard import add_hotkey
from pywinauto import Desktop

class Auto_Clicker:
    def __init__(self):
        self._running = False
        self._container = None
        self._selected_window = None
        self._dropdown_janelas = None
        self._clicks_count = 0
        self._status_label = None

    def _auto_click_ON(self, page, velocidade):
        try:
            if not self._selected_window:
                self._update_status(page, "❌ Nenhuma janela selecionada!", "#EF4444")
                return

            self._update_status(page, "🟢 Executando...", "#10B981")
            self._selected_window.set_focus()
            time.sleep(1)

            velocidades = {
                'Lento': 1.0,
                'Normal': 0.3,
                'Rápido': 0.1,
            }
            intervalo = velocidades.get(velocidade, 0.3)

            x, y = position()
            self._running = True
            self._clicks_count = 0
            
            while self._running:
                click(x, y)
                self._clicks_count += 1
                self._update_click_counter(page)
                time.sleep(intervalo)
                
        except Exception as e:
            self._update_status(page, f"❌ Erro: {str(e)}", "#EF4444")
        finally:
            self._auto_click_OFF(page)

    def _auto_click_OFF(self, page=None):
        self._running = False
        if page:
            self._update_status(page, "⏹ Pronto para executar", "#3B82F6")
            self._update_click_counter(page, reset=True)

    def _update_status(self, page, message, color):
        if self._status_label:
            self._status_label.value = message
            self._status_label.color = color
            page.update()

    def _update_click_counter(self, page, reset=False):
        if hasattr(self, '_counter_label'):
            if reset:
                self._counter_label.value = "Cliques: 0"
            else:
                self._counter_label.value = f"Cliques: {self._clicks_count}"
            page.update()

    def _listar_janelas(self, page, text_label):
        try:
            desktop = Desktop(backend="uia")
            janelas = desktop.windows()
            titulos_janelas = [janela.window_text() for janela in janelas if janela.window_text()]
            
            self._dropdown_janelas.options = [
                dropdown.Option(text=titulo) for titulo in titulos_janelas
            ]
            
            text_label.value = "✅ Janelas listadas com sucesso"
            text_label.color = "#10B981"
            page.update()
            
        except Exception as e:
            text_label.value = f"❌ Erro: {str(e)}"
            text_label.color = "#EF4444"
            page.update()

    def _selecionar_janela(self, page, text_label):
        if not self._dropdown_janelas.value:
            text_label.value = "❌ Selecione uma janela primeiro!"
            text_label.color = "#EF4444"
            page.update()
            return

        try:
            desktop = Desktop(backend="uia")
            for janela in desktop.windows():
                if janela.window_text() == self._dropdown_janelas.value:
                    self._selected_window = janela
                    text_label.value = f"✅ {janela.window_text()[:30]}..." if len(janela.window_text()) > 30 else f"✅ {janela.window_text()}"
                    text_label.color = "#10B981"
                    page.update()
                    break
                    
        except Exception as e:
            text_label.value = f"❌ Erro: {str(e)}"
            text_label.color = "#EF4444"
            page.update()

    def _tela(self, page: Page):
        page.title = "Auto-Clicker Pro"
        page.window.center()
        page.window.width = 500
        page.window.height = 600
        page.window_resizable = False
        page.horizontal_alignment = "center"
        page.vertical_alignment = "center"
        page.bgcolor = "#1E293B"
        page.padding = 20

        # Componentes da UI
        Title_text = Text("Auto-Clicker Pro", color="#FFFFFF", size=24, weight="bold")
        subtitle = Text("Automatize seus cliques com facilidade", color="#94A3B8", size=14)

        self._dropdown_velocidade = Dropdown(
            label="Velocidade de clique",
            options=[
                dropdown.Option("Lento"),
                dropdown.Option("Normal"),
                dropdown.Option("Rápido"),
            ],
            value="Normal",
            width=450,
            color="white",
            bgcolor="#475569",
            border_color="#64748B"
        )

        self._dropdown_janelas = Dropdown(
            label="Janela para focar",
            options=[],
            width=450,
            color="white",
            bgcolor="#475569",
            border_color="#64748B",
            autofocus=True,
            label_style=TextStyle(color="white")  # Label em branco
        )

        # Botões com ícones e estilo
        bnt_ligar = FilledButton(
            '▶ Iniciar',
            icon="play_arrow",
            style=ButtonStyle(
                bgcolor={"": "#10B981", "hovered": "#059669"},
                shape=RoundedRectangleBorder(radius=8),
                padding=15
            ),
            on_click=lambda e: self._iniciar_auto_click(page, self._dropdown_velocidade.value)
        )

        bnt_desligar = FilledButton(
            "⏹ Parar",
            icon="stop",
            style=ButtonStyle(
                bgcolor={"": "#EF4444", "hovered": "#DC2626"},
                shape=RoundedRectangleBorder(radius=8),
                padding=15
            ),
            on_click=lambda e: self._auto_click_OFF(page)
        )

        bnt_listar_janelas = FilledButton(
            "🔍 Listar Janelas",
            style=ButtonStyle(
                bgcolor={"": "#7C3AED", "hovered": "#6D28D9"},
                shape=RoundedRectangleBorder(radius=8),
                padding=15
            ),
            on_click=lambda e: self._listar_janelas(page, text_label)
        )

        bnt_selecionar_janela = FilledButton(
            "✅ Selecionar",
            style=ButtonStyle(
                bgcolor={"": "#3B82F6", "hovered": "#2563EB"},
                shape=RoundedRectangleBorder(radius=8),
                padding=15
            ),
            on_click=lambda e: self._selecionar_janela(page, text_label)
        )

        text_label = Text("Selecione uma janela para começar", color="#E2E8F0", size=14)
        self._status_label = Text("⏳ Pronto para executar", color="#3B82F6", size=14)
        self._counter_label = Text("Cliques: 0", color="#94A3B8", size=12)
        shortcut_hint = Text("Pressione Z para parar", color="#64748B", size=11)

        # Container principal
        self._container = Container(
            width=460,
            height=520,
            bgcolor="#334155",
            padding=20,
            border_radius=12,
            animate=Animation(300, "easeInOut"),
            content=Column(
                [
                    Column(
                        [
                            Row(
                                [
                                    Image(
                                        src="mouse-click-icon.png",
                                        width=40,
                                        height=40,
                                        fit="contain"
                                    ),
                                    Title_text
                                ],
                                alignment=MainAxisAlignment.CENTER,
                                vertical_alignment=CrossAxisAlignment.CENTER
                            ),
                            subtitle
                        ],
                        alignment=MainAxisAlignment.CENTER
                    ),

                    Divider(height=20, color="transparent"),
                    self._dropdown_janelas,
                    Divider(height=10, color="transparent"),
                    self._dropdown_velocidade,
                    Divider(height=20, color="transparent"),
                    ResponsiveRow(
                        [bnt_listar_janelas, bnt_selecionar_janela],
                        spacing=10,
                        alignment=MainAxisAlignment.CENTER
                    ),
                    Divider(height=20, color="transparent"),
                    ResponsiveRow(
                        [bnt_ligar, bnt_desligar],
                        spacing=10,
                        alignment=MainAxisAlignment.CENTER
                    ),
                    Divider(height=20, color="transparent"),
                    Column(
                        [
                            text_label,
                            Divider(height=10, color="transparent"),
                            self._status_label,
                            Divider(height=5, color="transparent"),
                            self._counter_label,
                            Divider(height=5, color="transparent"),
                            shortcut_hint
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER
                    )
                ],
                spacing=0,
                horizontal_alignment=CrossAxisAlignment.CENTER,
            )
        )

        page.add(self._container)
        page.update()

    def _iniciar_auto_click(self, page, dropdown_velocidade):
        Thread(target=self._auto_click_ON, args=(page, dropdown_velocidade), daemon=True).start()
        add_hotkey("q", lambda: self._auto_click_OFF(page))

    def _run(self):
        app(target=self._tela)
