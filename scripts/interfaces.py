import pygame

class Texto:
    def __init__(self, tela, texto, x, y, cor=(255,255,255), tamanho=32):
        self.tela = tela
        self.texto = str(texto)
        self.x = x
        self.y = y
        self.cor = cor
        self.fonte = pygame.font.SysFont(None, tamanho)

    def atualizarTexto(self, novo):
        self.texto = str(novo)

    def desenhar(self):
        img = self.fonte.render(self.texto, True, self.cor)
        self.tela.blit(img, (self.x, self.y))


class Botao:
    def __init__(self, tela, x, y, largura, altura, texto, acao):
        self.tela = tela
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.acao = acao
        self.fonte = pygame.font.SysFont(None, 36)
        self.clicado = False

    def desenhar(self):
        pygame.draw.rect(self.tela, (255,200,100), self.rect, border_radius=10)
        img = self.fonte.render(self.texto, True, (30,30,30))
        self.tela.blit(img, img.get_rect(center=self.rect.center))

    def checarClique(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                self.acao()
