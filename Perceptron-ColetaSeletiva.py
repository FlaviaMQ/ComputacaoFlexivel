import pandas as pd

amostra1 = [-1, 1, 0, 0]
amostra2 = [-1, 0, 1, 0]
amostra3 = [-1, 0, 0, 1]
amostra4 = [-1, 1, 0, 1]

amostras = [amostra1, amostra2, amostra3, amostra4]

Yesperado = [1, 1, 0, 0]

pesos = [0, 0, 0, 0]

taxa_aprendizagem = 1

historico = []

def funcao_ativacao(soma):
    if soma >= 1:
        return 1
    else:
        return 0

def treinamento(amostras, Yesperado, pesos, taxa_aprendizagem, epoca, historico):
    erros = []
   

    for i in range(len(amostras)):
        soma = 0
        for j in range(len(amostras[i])):
            soma += amostras[i][j] * pesos[j]

        ycalculado = funcao_ativacao(soma)
        erro = Yesperado[i] - ycalculado
        erros.append(erro)

        for k in range(len(pesos)):
            pesos[k] += taxa_aprendizagem * erro * amostras[i][k]

   

      # Armazena os dados da tabela
        historico.append({
            "Epoca": epoca,
            "Amostra": i + 1,
            "Entrada": str(amostras[i]),
            "Soma": soma,
            "Esperado": Yesperado[i],
            "Calculado": ycalculado,
            "Erro": erro,
            "Peso1": pesos[0],
            "Peso2": pesos[1],
            "Peso3": pesos[2],
            "Peso4": pesos[3],
            
        })
    return pesos, erros

#treinamento até que o erro seja zero para todas as amostras


epoca = 0
max_epocas = 100  # Limite para evitar loop infinito

while epoca < max_epocas:
    epoca += 1
    pesos, erros = treinamento(amostras, Yesperado, pesos, taxa_aprendizagem, epoca, historico)
    

    if all(erro == 0 for erro in erros):
        print("\nTreinamento concluído. Todos os erros são zero.\n")
        print("**************************************************\n")
        break

df = pd.DataFrame(historico)
print(df)

df.to_excel(
    "historico_treinamento.xlsx",
    index=False
)
#teste do perceptron final: Validação do modelo treinado com as amostras de entrada

print("\nTeste do Perceptron Resultado final:\n")

for i in range(len(amostras)):
    soma = 0

    for j in range(len(amostras[i])):
        soma += amostras[i][j] * pesos[j]

    yprevisto = funcao_ativacao(soma)
    erro = Yesperado[i] - yprevisto

    print(
        f"Amostra {i + 1}: "
        f"Esperado={Yesperado[i]}, "
        f"Calculado={yprevisto}, "
        f"Erro={erro}"
    )

print("Pesos finais:", pesos)
print("\n***********************************************\n")

def classificar(nova_amostra, pesos):
    soma = 0

    for j in range(len(nova_amostra)):
        soma += nova_amostra[j] * pesos[j]

    yprevisto = funcao_ativacao(soma)

    return yprevisto, soma

novas_amostras = [
    [-1, 1, 1, 1],
    [-1, 1, 1, 0],
    [-1, 0, 1, 1],
    [-1, 0, 0, 1]
]


print("\nClassificação de novas amostras:\n")
print("*" * 60)
print("\n")

for i in range(len(novas_amostras)):
    resultado, soma = classificar(novas_amostras[i], pesos)

    print(
        f"Nova amostra {i + 1}: "
        f"Entrada={novas_amostras[i]}, "
        f"Soma={soma}, "
        f"Classe prevista={resultado}"
    )
