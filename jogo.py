import pygame
import sys

pygame.init()

# Janela
LARGURA = 800
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Malha Hidráulica")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (100, 200, 100)
VERMELHO = (200, 100, 100)

# Configuração da malha
LINHAS = 8
COLUNAS = 8

LARGURA_CELULA = LARGURA // COLUNAS
ALTURA_CELULA = ALTURA // LINHAS


# Loop principal
while True:

    # Eventos
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fundo
    tela.fill(BRANCO)

# Desenhar linhas verticais
    for coluna in range(COLUNAS + 1):
        x = coluna * LARGURA_CELULA
        pygame.draw.line(tela, PRETO, (x, 0), (x, ALTURA), 1)

# Desenhar linhas horizontais
    for linha in range(LINHAS + 1):
        y = linha * ALTURA_CELULA
        pygame.draw.line(tela, PRETO, (0, y), (LARGURA, y), 1)

# Desenhar nós nos vértices
    for linha in range(LINHAS + 1):
        for coluna in range(COLUNAS + 1):
            x = coluna * LARGURA_CELULA
            y = linha * ALTURA_CELULA

            pygame.draw.circle(tela, VERMELHO, (x, y), 5)        
 
    #Atualiza tela
    pygame.display.update()
