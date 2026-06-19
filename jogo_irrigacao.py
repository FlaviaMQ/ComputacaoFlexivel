import random
import heapq

LINHAS = 10
COLUNAS = 10
UMIDADE_MINIMA = 35  # abaixo disso, o talhão precisa ser irrigado


def gerar_malha():
    """
    Gera uma malha 10x10.
    Cada célula representa 1 ha e recebe uma umidade aleatória entre 10% e 80%.
    """
    malha = []

    for i in range(LINHAS):
        linha = []
        for j in range(COLUNAS):
            umidade = random.randint(10, 80)
            linha.append(umidade)
        malha.append(linha)

    return malha


def mostrar_malha(malha):
    """
    Mostra a malha com os valores de umidade.
    """
    print("\nMALHA DE UMIDADE DO SOLO (%)")
    print("Cada posição representa 1 ha\n")

    for i in range(LINHAS):
        for j in range(COLUNAS):
            print(f"{malha[i][j]:3}", end=" ")
        print()


def busca_cega(malha):
    """
    Busca cega:
    Percorre todos os talhões, linha por linha, sem priorizar nenhum.
    """
    talhoes_irrigar = []

    for i in range(LINHAS):
        for j in range(COLUNAS):
            umidade = malha[i][j]

            if umidade < UMIDADE_MINIMA:
                talhoes_irrigar.append((i, j, umidade))

    return talhoes_irrigar


def busca_heuristica(malha):
    """
    Busca heurística:
    Prioriza os talhões com menor umidade.
    Quanto menor a umidade, maior a urgência de irrigação.
    """
    fila_prioridade = []

    for i in range(LINHAS):
        for j in range(COLUNAS):
            umidade = malha[i][j]

            if umidade < UMIDADE_MINIMA:
                prioridade = umidade
                heapq.heappush(fila_prioridade, (prioridade, i, j, umidade))

    talhoes_priorizados = []

    while fila_prioridade:
        prioridade, i, j, umidade = heapq.heappop(fila_prioridade)
        talhoes_priorizados.append((i, j, umidade))

    return talhoes_priorizados


def mostrar_resultado(talhoes, tipo_busca):
    """
    Mostra os talhões que devem ser irrigados.
    """
    print(f"\nRESULTADO - {tipo_busca}")
    print(f"Umidade mínima adotada: {UMIDADE_MINIMA}%\n")

    if not talhoes:
        print("Nenhum talhão precisa ser irrigado.")
        return

    print("Talhões que precisam de irrigação:")
    print("Linha | Coluna | Umidade (%) | Área (ha)")

    for i, j, umidade in talhoes:
        print(f"{i:5} | {j:6} | {umidade:11} | 1 ha")

    print(f"\nTotal de talhões irrigados: {len(talhoes)}")
    print(f"Área total a irrigar: {len(talhoes)} ha")


def jogo():
    malha = gerar_malha()

    mostrar_malha(malha)

    print("\nEscolha o tipo de busca:")
    print("1 - Busca cega")
    print("2 - Busca heurística")

    opcao = input("Digite a opção: ")

    if opcao == "1":
        resultado = busca_cega(malha)
        mostrar_resultado(resultado, "BUSCA CEGA")

    elif opcao == "2":
        resultado = busca_heuristica(malha)
        mostrar_resultado(resultado, "BUSCA HEURÍSTICA")

    else:
        print("Opção inválida.")


jogo()
