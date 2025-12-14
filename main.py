import pygame
import sys
import os
from scripts.cenas import Partida

pygame.init()
LARGURA = 480
ALTURA = 640
FPS = 60

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Ado Cake Catcher")
clock = pygame.time.Clock()

ASSETS = os.path.join(os.path.dirname(__file__), "assets")
# garante pasta assets exista
if not os.path.isdir(ASSETS):
    os.makedirs(ASSETS)

partida = Partida(tela)

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # teclado para flap / controle é tratado nos eventos abaixo:
        if evento.type == pygame.KEYDOWN:
            # tecla ESC volta ao menu
            if evento.key == pygame.K_ESCAPE:
                partida.estado = "menu"

        partida.tratar_evento(evento)

    partida.atualizar()
    partida.desenhar()

    pygame.display.update()
    clock.tick(FPS)
