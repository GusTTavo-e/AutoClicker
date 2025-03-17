from flet import Page, Text, Row, app, Column, Container, MainAxisAlignment, FilledButton, CrossAxisAlignment, Dropdown, dropdown
from pyautogui import position, click
import time
from threading import Thread
from keyboard import add_hotkey # Biblioteca para detectar teclas pressionadas
from pywinauto import Desktop  # Biblioteca para interagir com janelas

class Auto_Clicker:
    def __init__(self):
        self._running = False  # Flag para controlar o loop do auto-clicker
        self._container = None  # Referência ao Container para modificar sua cor
        self._selected_window = None  # Janela selecionada pelo usuário
        self._dropdown_janelas = None  # Referência ao Dropdown para listar janelas

    def _auto_click_ON(self, page):
        try:
            if not self._selected_window:
                print("Erro: Nenhuma janela selecionada.")
                return

            print(f"Janela selecionada: {self._selected_window.window_text()}")
            self._selected_window.set_focus()  # Coloca a janela em foco
            time.sleep(2)  # Dá tempo para a janela ganhar foco

            # Muda a cor do Container para verde suave
            self._container.bgcolor = "#A7F3D0"  # Verde pastel mai vibrante
            page.update()

            # Obtém as coordenadas iniciais do mouse
            x, y = position()
            print(f"Coordenadas do mouse: X = {x}, Y = {y}")

            # Define o intervalo entre os cliques (em segundos)
            intervalo_entre_cliques = 0.5  # 0.5 segundo

            self._running = True
            print("Auto-click ligado. Pressione 'Q' para parar o script.")
            while self._running:
                click(x, y)  # Clique nas coordenadas
                print(f"Clicado em X = {x}, Y = {y}")
                time.sleep(intervalo_entre_cliques)  # Aguarda o intervalo
        except Exception as e:
            print(f"Erro durante o auto-click: {e}")
        finally:
            print("Auto-click desligado.")
            # Restaura a cor do Container para azul claro
            self._container.bgcolor = "#FCA5A5"  # Vermelho pastel mais vibrante
            page.update()

    def _auto_click_OFF(self):
        self._running = False
        print("Auto-click desligado.")

    def _listar_janelas(self, page):
        try:
            print("Listando janelas...")
            # Lista todas as janelas abertas usando o backend 'uia'
            desktop = Desktop(backend="uia")
            janelas = desktop.windows()

            # Cria uma lista de títulos de janelas
            titulos_janelas = [janela.window_text() for janela in janelas if janela.window_text()]
            print(f"Janelas encontradas: {titulos_janelas}")

            # Atualiza o Dropdown com as janelas encontradas
            self._dropdown_janelas.options = [
                dropdown.Option(text=titulo) for titulo in titulos_janelas
            ]
            page.update()
        except Exception as e:
            print(f"Erro ao listar janelas: {e}")

    def _selecionar_janela(self, page):
        try:
            if not self._dropdown_janelas.value:
                print("Erro: Nenhuma janela selecionada.")
                return

            # Obtém o título da janela selecionada
            titulo_janela = self._dropdown_janelas.value

            # Lista todas as janelas abertas novamente para encontrar a janela correta
            desktop = Desktop(backend="uia")
            janelas = desktop.windows()

            # Procura a janela com o título selecionado
            for janela in janelas:
                if janela.window_text() == titulo_janela:
                    self._selected_window = janela
                    print(f"Janela selecionada: {self._selected_window.window_text()}")
                    break
        except Exception as e:
            print(f"Erro ao selecionar janela: {e}")

    def _tela(self, page: Page):
        page.title = "Auto-Clicker"
        page.window.center()
        page.window.width = 480
        page.window.height = 480  # Aumentei a altura para acomodar a lista de janelas
        page.horizontal_alignment = "center"
        page.vertical_alignment = "center"
        page.bgcolor = "grey900"  # Fundo da página em cinza claro

        # Dropdown para listar as janelas
        self._dropdown_janelas = Dropdown(
            label="Selecione uma janela",
            options=[],  # Inicialmente vazio
            autofocus=True,
            width=400,  # Largura maior para o Dropdown
            color= 'white',
        )

        # Botões
        Title_text = Text("Auto-Clicker", color="black", size=20, weight="bold")
        bnt_ligar = FilledButton(text="Ligar", on_click=lambda e: self._iniciar_auto_click(page))
        bnt_desligar = FilledButton(text="Desligar", on_click=lambda e: self._auto_click_OFF())
        bnt_listar_janelas = FilledButton(text="Listar Janelas", on_click=lambda e: self._listar_janelas(page))
        bnt_selecionar_janela = FilledButton(text="Selecionar Janela", on_click=lambda e: self._selecionar_janela(page))

        # Container principal
        self._container = Container(
            width=440,
            height=400,  # Aumentei a altura para acomodar a lista de janelas
            bgcolor="#FCA5A5",  # Azul pastel
            padding=25,
            border_radius=10,
            content=Column(
                [
                    Row(
                        [Title_text],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    Row(
                        [self._dropdown_janelas],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    Row(
                        [bnt_listar_janelas, bnt_selecionar_janela],
                        alignment=MainAxisAlignment.CENTER,
                        spacing=20,  # Espaçamento entre os botões
                    ),
                    Row(
                        [bnt_ligar, bnt_desligar],
                        alignment=MainAxisAlignment.CENTER,
                        spacing=20,  # Espaçamento entre os botões
                    )
                ],
                alignment=MainAxisAlignment.START,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=20,  # Espaçamento entre as linhas
            )
        )

        page.add(self._container)
        page.update()

    def _iniciar_auto_click(self, page):
        print("Iniciando auto-click...")
        # Inicia o auto-clicker em uma thread separada
        Thread(target=self._auto_click_ON, args=(page,), daemon=True).start()

        # Configura a tecla "Q" para desligar o auto-click
        add_hotkey("q", self._auto_click_OFF)

    def _run(self):
        app(target=self._tela)
