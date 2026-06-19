import pygame
import random
import heapq

LINHAS = 10
COLUNAS = 10
TAMANHO_CELULA = 60

LARGURA = COLUNAS * TAMANHO_CELULA
ALTURA = LINHAS * TAMANHO_CELULA + 130

UMIDADE_MINIMA = 35

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (90, 180, 90)
AMARELO = (230, 200, 60)
VERMELHO = (220, 80, 70)
AZUL = (70, 130, 220)
CINZA = (180, 180, 180)
CINZA_CLARO = (230, 230, 230)

VELOCIDADE_MS = 250


def gerar_malha():
    return [
        [random.randint(10, 80) for _ in range(COLUNAS)]
        for _ in range(LINHAS)
    ]


def caminho_busca_cega():
    caminho = []

    for i in range(LINHAS):
        for j in range(COLUNAS):
            caminho.append((i, j))

    return caminho


def caminho_busca_heuristica(malha):
    fila = []

    for i in range(LINHAS):
        for j in range(COLUNAS):
            umidade = malha[i][j]
            heapq.heappush(fila, (umidade, i, j))

    caminho = []

    while fila:
        umidade, i, j = heapq.heappop(fila)
        caminho.append((i, j))

    return caminho


def cor_por_umidade(umidade):
    if umidade < UMIDADE_MINIMA:
        return VERMELHO
    elif umidade < 50:
        return AMARELO
    else:
        return VERDE


def desenhar_malha(tela, fonte, malha, visitados, atual, irrigar):
    for i in range(LINHAS):
        for j in range(COLUNAS):
            x = j * TAMANHO_CELULA
            y = i * TAMANHO_CELULA

            umidade = malha[i][j]
            cor = cor_por_umidade(umidade)

            if (i, j) in visitados:
                cor = CINZA

            if (i, j) in irrigar:
                cor = VERMELHO

            if atual == (i, j):
                cor = AZUL

            pygame.draw.rect(tela, cor, (x, y, TAMANHO_CELULA, TAMANHO_CELULA))
            pygame.draw.rect(tela, PRETO, (x, y, TAMANHO_CELULA, TAMANHO_CELULA), 1)

            texto = fonte.render(str(umidade), True, PRETO)
            texto_rect = texto.get_rect(
                center=(x + TAMANHO_CELULA / 2, y + TAMANHO_CELULA / 2)
            )
            tela.blit(texto, texto_rect)


def desenhar_painel(tela, fonte, modo, passo, total_passos, area_irrigar):
    y = LINHAS * TAMANHO_CELULA

    pygame.draw.rect(tela, CINZA_CLARO, (0, y, LARGURA, 130))

    linhas_texto = [
        "Jogo de Irrigacao - Caminhada da busca",
        "C: busca cega | H: busca heuristica | R: nova malha | ESC: sair",
        f"Modo atual: {modo}",
        f"Passo: {passo} de {total_passos}",
        f"Area identificada para irrigacao: {area_irrigar} ha",
    ]

    for indice, texto in enumerate(linhas_texto):
        render = fonte.render(texto, True, PRETO)
        tela.blit(render, (10, y + 10 + indice * 23))


def iniciar_busca(tipo, malha):
    if tipo == "cega":
        caminho = caminho_busca_cega()
        modo = "Busca cega: varredura linha por linha"

    elif tipo == "heuristica":
        caminho = caminho_busca_heuristica(malha)
        modo = "Busca heuristica: menor umidade primeiro"

    else:
        caminho = []
        modo = "Nenhuma busca"

    return caminho, modo


def main():
    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Busca cega e heuristica na irrigacao")

    fonte = pygame.font.SysFont("Arial", 18)

    malha = gerar_malha()

    caminho = []
    visitados = set()
    irrigar = set()
    atual = None

    modo = "Nenhuma busca realizada"
    passo = 0
    rodando_busca = False
    ultimo_tempo = 0

    clock = pygame.time.Clock()

    executando = True

    while executando:
        tempo_atual = pygame.time.get_ticks()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    executando = False

                elif evento.key == pygame.K_r:
                    malha = gerar_malha()
                    caminho = []
                    visitados = set()
                    irrigar = set()
                    atual = None
                    modo = "Nova malha gerada"
                    passo = 0
                    rodando_busca = False

                elif evento.key == pygame.K_c:
                    caminho, modo = iniciar_busca("cega", malha)
                    visitados = set()
                    irrigar = set()
                    atual = None
                    passo = 0
                    rodando_busca = True
                    ultimo_tempo = tempo_atual

                elif evento.key == pygame.K_h:
                    caminho, modo = iniciar_busca("heuristica", malha)
                    visitados = set()
                    irrigar = set()
                    atual = None
                    passo = 0
                    rodando_busca = True
                    ultimo_tempo = tempo_atual

        if rodando_busca and tempo_atual - ultimo_tempo >= VELOCIDADE_MS:
            if passo < len(caminho):
                atual = caminho[passo]
                i, j = atual

                visitados.add(atual)

                if malha[i][j] < UMIDADE_MINIMA:
                    irrigar.add(atual)

                passo += 1
                ultimo_tempo = tempo_atual

            else:
                rodando_busca = False
                atual = None

        tela.fill(BRANCO)

        desenhar_malha(tela, fonte, malha, visitados, atual, irrigar)

        desenhar_painel(
            tela,
            fonte,
            modo,
            passo,
            len(caminho),
            len(irrigar),
        )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


main()