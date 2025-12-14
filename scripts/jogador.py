import pygame
import os

class Jogador:
    def __init__(self, tela):
        self.tela = tela
        assets = os.path.join(os.path.dirname(__file__), "..", "assets")

        try:
            img = pygame.image.load(os.path.join(assets, "ado.png")).convert_alpha()
        except:
            img = pygame.Surface((80, 120), pygame.SRCALPHA)
            img.fill((120, 120, 255))

        self.imagem = pygame.transform.scale(img, (80, 120))

        self.rect = self.imagem.get_rect()
        self.rect.midbottom = (
            tela.get_width() // 2,
            tela.get_height() - 40
        )

        self.vel = 6

    def atualizar(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.vel
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.vel

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.tela.get_width():
            self.rect.right = self.tela.get_width()

    def desenhar(self):
        self.tela.blit(self.imagem, self.rect)

    def getRect(self):
        return self.rect
