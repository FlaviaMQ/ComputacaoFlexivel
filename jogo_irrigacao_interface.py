import pygame
import random
import heapq

# Configurações da malha
LINHAS = 10
COLUNAS = 10
TAMANHO_CELULA = 60

# Configurações da janela
LARGURA = COLUNAS * TAMANHO_CELULA
ALTURA = LINHAS * TAMANHO_CELULA + 120

# Critério de irrigação
UMIDADE_MINIMA = 35

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (90, 180, 90)
AMARELO = (230, 200, 60)
VERMELHO = (220, 80, 70)
AZUL = (70, 130, 220)
CINZA = (220, 220, 220)


def gerar_malha():
    malha = []

    for i in range(LINHAS):
        linha = []

        for j in range(COLUNAS):
            umidade = random.randint(10, 80)
            linha.append(umidade)

        malha.append(linha)

    return malha


def busca_cega(malha):
    talhoes = []

    for i in range(LINHAS):
        for j in range(COLUNAS):
            if malha[i][j] < UMIDADE_MINIMA:
                talhoes.append((i, j, malha[i][j]))

    return talhoes


def busca_heuristica(malha):
    fila = []

    for i in range(LINHAS):
        for j in range(COLUNAS):
            umidade = malha[i][j]

            if umidade < UMIDADE_MINIMA:
                heapq.heappush(fila, (umidade, i, j))

    talhoes = []

    while fila:
        umidade, i, j = heapq.heappop(fila)
        talhoes.append((i, j, umidade))

    return talhoes


def cor_por_umidade(umidade):
    if umidade < UMIDADE_MINIMA:
        return VERMELHO
    elif umidade < 50:
        return AMARELO
    else:
        return VERDE


def desenhar_malha(tela, fonte, malha, selecionados):
    for i in range(LINHAS):
        for j in range(COLUNAS):
            x = j * TAMANHO_CELULA
            y = i * TAMANHO_CELULA

            umidade = malha[i][j]
            cor = cor_por_umidade(umidade)

            if (i, j) in selecionados:
                cor = AZUL

            pygame.draw.rect(tela, cor, (x, y, TAMANHO_CELULA, TAMANHO_CELULA))
            pygame.draw.rect(tela, PRETO, (x, y, TAMANHO_CELULA, TAMANHO_CELULA), 1)

            texto = fonte.render(str(umidade), True, PRETO)
            texto_rect = texto.get_rect(center=(x + TAMANHO_CELULA / 2, y + TAMANHO_CELULA / 2))
            tela.blit(texto, texto_rect)


def desenhar_painel(tela, fonte, modo, total_area):
    y = LINHAS * TAMANHO_CELULA

    pygame.draw.rect(tela, CINZA, (0, y, LARGURA, 120))

    texto1 = fonte.render("Jogo de Irrigacao - Malha 10 x 10", True, PRETO)
    texto2 = fonte.render("C: busca cega | H: busca heuristica | R: nova malha | ESC: sair", True, PRETO)
    texto3 = fonte.render(f"Modo atual: {modo}", True, PRETO)
    texto4 = fonte.render(f"Area total a irrigar: {total_area} ha", True, PRETO)

    tela.blit(texto1, (10, y + 10))
    tela.blit(texto2, (10, y + 35))
    tela.blit(texto3, (10, y + 65))
    tela.blit(texto4, (10, y + 90))


def main():
    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Jogo de Irrigacao com Busca Cega e Heuristica")

    fonte = pygame.font.SysFont("Arial", 20)

    malha = gerar_malha()
    selecionados = set()
    modo = "Nenhuma busca realizada"
    total_area = 0

    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False

                elif evento.key == pygame.K_r:
                    malha = gerar_malha()
                    selecionados = set()
                    modo = "Nova malha gerada"
                    total_area = 0

                elif evento.key == pygame.K_c:
                    resultado = busca_cega(malha)
                    selecionados = {(i, j) for i, j, umidade in resultado}
                    modo = "Busca cega"
                    total_area = len(resultado)

                elif evento.key == pygame.K_h:
                    resultado = busca_heuristica(malha)
                    selecionados = {(i, j) for i, j, umidade in resultado}
                    modo = "Busca heuristica"
                    total_area = len(resultado)

        tela.fill(BRANCO)

        desenhar_malha(tela, fonte, malha, selecionados)
        desenhar_painel(tela, fonte, modo, total_area)

        pygame.display.flip()

    pygame.quit()


main()
