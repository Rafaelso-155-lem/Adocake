import pygame
import random
import os
from scripts.jogador import Jogador
from scripts.bolo import Bolo
from scripts.interfaces import Texto, Botao


class Partida:
    def __init__(self, tela):
        self.tela = tela
        self.estado = "menu"

        self.jogador = Jogador(tela)
        self.bolos = []

        # fases
        self.fase = 1
        self.meta_fase = {1: 20, 2: 30, 3: 50}

        # pontuação e erros
        self.pontos = 0
        self.erros = 0

        self.pontosTexto = Texto(tela, "Pontos: 0", 10, 10, (20, 40, 120), 28)
        self.faseTexto = Texto(tela, "Fase: 1", 10, 40, (20, 40, 120), 24)
        self.errosTexto = Texto(tela, "Erros: 0/3", 10, 70, (120, 20, 20), 24)

        # botão jogar
        self.botaoJogar = Botao(
            tela,
            tela.get_width() // 2 - 90,
            tela.get_height() // 2,
            180,
            56,
            "Jogar",
            self.reiniciar
        )

        # spawn
        self.spawn_timer = 0
        self.spawn_interval = 90
        self.vel_base = 2.0

        # fundo fase 1
        self.bg_color = (135, 206, 235)

        # fundo fase 2 (imagem)
        assets = os.path.join(os.path.dirname(__file__), "..", "assets")
        try:
            self.bg_fase2 = pygame.image.load(
                os.path.join(assets, "santuario.png")
            ).convert()
            self.bg_fase2 = pygame.transform.scale(
                self.bg_fase2,
                (tela.get_width(), tela.get_height())
            )
        except:
            self.bg_fase2 = None

    def reiniciar(self):
        self.jogador = Jogador(self.tela)
        self.bolos.clear()

        self.fase = 1
        self.pontos = 0
        self.erros = 0

        self.spawn_timer = 0
        self.spawn_interval = 90
        self.vel_base = 2.0

        self.pontosTexto.atualizarTexto("Pontos: 0")
        self.faseTexto.atualizarTexto("Fase: 1")
        self.errosTexto.atualizarTexto("Erros: 0/3")

        self.estado = "partida"

    def tratar_evento(self, evento):
        if self.estado == "menu":
            self.botaoJogar.checarClique(evento)

        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_SPACE, pygame.K_RETURN):
                if self.estado in ("menu", "vitoria"):
                    self.reiniciar()

    def atualizar(self):
        if self.estado != "partida":
            return

        teclas = pygame.key.get_pressed()
        self.jogador.atualizar(teclas)

        # spawn de bolos
        self.spawn_timer += 1
        if self.spawn_timer > self.spawn_interval:
            vel = self.vel_base + (self.fase * 0.8)
            self.bolos.append(Bolo(self.tela, velocidade_base=vel))
            self.spawn_timer = 0

        for bolo in list(self.bolos):
            bolo.atualizar()

            # pegou o bolo
            if bolo.rect.colliderect(self.jogador.getRect()):
                self.bolos.remove(bolo)
                self.pontos += 1
                self.pontosTexto.atualizarTexto(f"Pontos: {self.pontos}")
                self.verificar_fase()
                continue

            # bolo caiu
            if bolo.saiu_da_tela():
                self.bolos.remove(bolo)
                self.erros += 1
                self.errosTexto.atualizarTexto(f"Erros: {self.erros}/3")

                if self.erros >= 3:
                    self.estado = "menu"
                    return

    def verificar_fase(self):
        if self.pontos >= self.meta_fase[self.fase]:
            if self.fase < 3:
                self.fase += 1
                self.spawn_interval = max(40, self.spawn_interval - 20)
                self.vel_base += 1
                self.bolos.clear()
                self.faseTexto.atualizarTexto(f"Fase: {self.fase}")
            else:
                self.estado = "vitoria"

    def desenhar(self):
        # FUNDO
        if self.fase == 1:
            self.tela.fill(self.bg_color)

            # nuvens
            pygame.draw.ellipse(self.tela, (255,255,255), (40, 60, 160, 70))
            pygame.draw.ellipse(self.tela, (255,255,255), (220, 40, 180, 80))
            pygame.draw.ellipse(self.tela, (255,255,255), (120, 140, 200, 90))

        elif self.fase == 2 and self.bg_fase2:
            self.tela.blit(self.bg_fase2, (0, 0))

        else:
            self.tela.fill((40, 40, 40))

        # MENU
        if self.estado == "menu":
            font = pygame.font.SysFont(None, 64)
            titulo = font.render("ADO CAKE GAME", True, (20, 40, 120))
            self.tela.blit(
                titulo,
                titulo.get_rect(center=(self.tela.get_width()//2, 150))
            )
            self.botaoJogar.desenhar()
            return

        # VITÓRIA
        if self.estado == "vitoria":
            font = pygame.font.SysFont(None, 56)
            msg = font.render("VOCÊ ZEROU O JOGO!", True, (20, 40, 120))
            self.tela.blit(
                msg,
                msg.get_rect(center=(self.tela.get_width()//2, 220))
            )
            return

        # JOGO
        self.jogador.desenhar()
        for bolo in self.bolos:
            bolo.desenhar()

        self.pontosTexto.desenhar()
        self.faseTexto.desenhar()
        self.errosTexto.desenhar()
