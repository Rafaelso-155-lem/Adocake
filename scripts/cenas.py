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

        # transição de fases
        self.estado_anterior = None
        self.timer_transicao = 0
        self.duracao_transicao = 120  # 2 segundos (60 FPS)


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

        assets = os.path.join(os.path.dirname(__file__), "..", "assets")

        # fundo fase 2
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

        # fundo fase 3 (ESPAÇO)
        try:
            self.bg_fase3 = pygame.image.load(
                os.path.join(assets, "espaço.png")
            ).convert()
            self.bg_fase3 = pygame.transform.scale(
                self.bg_fase3,
                (tela.get_width(), tela.get_height())
            )
        except:
            self.bg_fase3 = None

        # imagem da vitória (Ado dominando o mundo)
        try:
            self.img_vitoria = pygame.image.load(
                os.path.join(assets, "adominacao.png")
            ).convert_alpha()
            self.img_vitoria = pygame.transform.scale(self.img_vitoria, (260, 260))
        except:
            self.img_vitoria = None


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

        if evento.type == pygame.KEYUP:
            if evento.key in (pygame.K_SPACE, pygame.K_RETURN):
                if self.estado in ("menu", "vitoria"):
                    self.reiniciar()


    def atualizar(self):
        if self.estado == "transicao":
            self.timer_transicao += 1
            if self.timer_transicao >= self.duracao_transicao:
                self.estado = "partida"
            return

        teclas = pygame.key.get_pressed()
        self.jogador.atualizar(teclas)

        self.spawn_timer += 1
        if self.spawn_timer > self.spawn_interval:
            vel = self.vel_base + (self.fase * 0.8)
            self.bolos.append(Bolo(self.tela, velocidade_base=vel))
            self.spawn_timer = 0

        for bolo in list(self.bolos):
            bolo.atualizar()

            if bolo.rect.colliderect(self.jogador.getRect()):
                self.bolos.remove(bolo)
                self.pontos += 1
                self.pontosTexto.atualizarTexto(f"Pontos: {self.pontos}")
                self.verificar_fase()
                continue

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

                # inicia transição
                self.estado_anterior = "partida"
                self.estado = "transicao"
                self.timer_transicao = 0
            else:
                self.estado = "vitoria"


    def desenhar(self):

        # MENU
        if self.estado == "menu":
            self.tela.fill(self.bg_color)

            pygame.draw.ellipse(self.tela, (255,255,255), (40, 60, 160, 70))
            pygame.draw.ellipse(self.tela, (255,255,255), (220, 40, 180, 80))
            pygame.draw.ellipse(self.tela, (255,255,255), (120, 140, 200, 90))

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
            self.tela.fill((0, 0, 0))

            font = pygame.font.SysFont(None, 30)

            linha1 = font.render(
                "VOCÊ ZEROU O JOGO!",
                True,
                (255, 255, 255)
            )
            linha2 = font.render(
                "E CONQUISTOU A ADOminação DO MUNDO",
                True,
                (255, 255, 255)
            )

            self.tela.blit(
                linha1,
                linha1.get_rect(center=(self.tela.get_width()//2, 90))
            )
            self.tela.blit(
                linha2,
                linha2.get_rect(center=(self.tela.get_width()//2, 130))
            )

            caixa_rect = pygame.Rect(
                self.tela.get_width()//2 - 130,
                170,
                260,
                260
            )
            pygame.draw.rect(self.tela, (255, 255, 255), caixa_rect, 2)

            if self.img_vitoria:
                self.tela.blit(self.img_vitoria, caixa_rect.topleft)

            font2 = pygame.font.SysFont(None, 32)
            inst = font2.render(
                "Pressione ENTER para jogar novamente",
                True,
                (200, 200, 200)
            )
            self.tela.blit(
                inst,
                inst.get_rect(center=(self.tela.get_width()//2, 460))
            )
            return


        # TRANSIÇÃO DE FASE
        if self.estado == "transicao":
            self.tela.fill((0, 0, 0))

            font = pygame.font.SysFont(None, 56)
            titulo = font.render(f"FASE {self.fase}", True, (255, 255, 255))
            self.tela.blit(
                titulo,
                titulo.get_rect(center=(self.tela.get_width()//2, 200))
            )

            font2 = pygame.font.SysFont(None, 32)

            if self.fase == 1:
                 subtitulo = "O INÍCIO DE UM SONHO"
            elif self.fase == 2:subtitulo = "SANTUÁRIO MALEVOLENTE"
            elif self.fase == 3:subtitulo = "DOMÍNIO DO ESPAÇO TEMPO"
            else:
                 subtitulo = ""


            sub = font2.render(subtitulo, True, (200, 200, 200))
            self.tela.blit(
                sub,
                sub.get_rect(center=(self.tela.get_width()//2, 250))
            )
            return


        # FUNDO DO JOGO (somente se estiver jogando)
        if self.fase == 1:
            self.tela.fill(self.bg_color)

            pygame.draw.ellipse(self.tela, (255,255,255), (40, 60, 160, 70))
            pygame.draw.ellipse(self.tela, (255,255,255), (220, 40, 180, 80))
            pygame.draw.ellipse(self.tela, (255,255,255), (120, 140, 200, 90))
            # sol
            pygame.draw.circle(self.tela, (255, 215, 0),
                   (self.tela.get_width() - 50, 50), 30)

            pygame.draw.circle(self.tela, (255, 235, 120),
                   (self.tela.get_width() - 50, 50), 25)



        elif self.fase == 2 and self.bg_fase2:
            self.tela.blit(self.bg_fase2, (0, 0))

        elif self.fase == 3 and self.bg_fase3:
            self.tela.blit(self.bg_fase3, (0, 0))

        else:
            self.tela.fill((40, 40, 40))


        # JOGO
        self.jogador.desenhar()
        for bolo in self.bolos:
            bolo.desenhar()

        self.pontosTexto.desenhar()
        self.faseTexto.desenhar()
        self.errosTexto.desenhar()
