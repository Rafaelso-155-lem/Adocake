import pygame
import os
import random

class Bolo:
    def __init__(self, tela, velocidade_base=2):
        self.tela = tela
        assets = os.path.join(os.path.dirname(__file__), "..", "assets")
        try:
            img = pygame.image.load(os.path.join(assets, "bolo.png")).convert_alpha()
        except:
            # fallback: desenhar um bolo simples
            img = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.ellipse(img, (250,200,180), (0, 10, 40, 25))  # massa
            pygame.draw.circle(img, (200,60,80), (20, 12), 6)  # cereja

        # escala (opcional)
        self.imagem = pygame.transform.scale(img, (60, 60))

        self.rect = self.imagem.get_rect()
        w = self.tela.get_width()
        # spawn aleatório X com margem para caber inteiro
        self.rect.x = random.randint(8, w - self.rect.width - 8)
        self.rect.y = -self.rect.height - random.randint(0, 80)

        # velocidade
        self.vel = velocidade_base + random.random() * 1.8

    def atualizar(self):
        self.rect.y += self.vel

    def desenhar(self):
        self.tela.blit(self.imagem, self.rect)

    def saiu_da_tela(self):
        return self.rect.top > self.tela.get_height()
