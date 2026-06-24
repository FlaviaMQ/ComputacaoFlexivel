import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# 1. Ler a aba da planilha
dados = pd.read_excel("Conforto-Termico-anapolis.xlsm", sheet_name="treino")

dados = dados.dropna(subset=["Mes", "Hora", "Temperatura", "UR", "Classe"])

# remove linhas totalmente vazias
dados = dados.dropna(how="all")

# remove linhas sem classe
dados = dados.dropna(subset=["Classe"])

# remove linhas com classe inválida
dados = dados[dados["Classe"].isin([0, 1, 2])]

dados["Mes_sen"] = np.sin(2*np.pi*dados["Mes"]/12)
dados["Mes_cos"] = np.cos(2*np.pi*dados["Mes"]/12)

dados["Hora_sen"] = np.sin(2*np.pi*dados["Hora"]/24)
dados["Hora_cos"] = np.cos(2*np.pi*dados["Hora"]/24)

#Análise exploratória: tabela cruzada de Mes e Hora com Classe
print("\nClasse por mês:")
print(pd.crosstab(dados["Mes"], dados["Classe"]))

print("\nClasse por hora:")
print(pd.crosstab(dados["Hora"], dados["Classe"]))

print("\nClasse por mês e hora:")
print(pd.crosstab(
    [dados["Mes"], dados["Hora"]],
    dados["Classe"]
))
print(
    pd.crosstab(
        dados["Classe"],
        pd.cut(
            dados["Temperatura"],
            bins=[0,15,20,25,30,50]
        )
    )
)

print(
    pd.crosstab(
        dados["Classe"],
        pd.cut(
            dados["UR"],
            bins=[0,40,60,80,100]
        )
    )
)

print("\nEstatísticas descritivas por classe:")
print(
    dados.groupby("Classe")[["Temperatura","UR"]]
    .agg(["mean","std","min","max"])
)
print(
    dados.groupby("Classe")[["Temperatura","UR"]]
    .describe()
)



for classe in [0,1,2]:
    subset = dados[dados["Classe"] == classe]
    plt.scatter(
        subset["Temperatura"],
        subset["UR"],
        alpha=0.3,
        label=f"Classe {classe}"
    )

plt.xlabel("Temperatura")
plt.ylabel("UR")
plt.legend()
plt.show()

# 2. Separar entradas e saída
X = dados[["Mes_sen", "Mes_cos", "Hora_sen", "Hora_cos", "Temperatura", "UR"]]
y = dados["Classe"]

# 3. Dividir dados: 70% treino, 15% validação, 15% teste
X_treino, X_temp, y_treino, y_temp = train_test_split(
    X, y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

X_valid, X_teste, y_valid, y_teste = train_test_split(
    X_temp, y_temp,
    test_size=0.50,
    random_state=42,
    stratify=y_temp
)

# 4. Normalizar entradas
scaler = StandardScaler()

X_treino = scaler.fit_transform(X_treino)
X_valid = scaler.transform(X_valid)
X_teste = scaler.transform(X_teste)

# 5. Criar e treinar a rede MLP
rede = MLPClassifier(
    hidden_layer_sizes=(6,),
    activation="relu",
    solver="adam",
    max_iter=1000,
    random_state=42
)

rede.fit(X_treino, y_treino)

# 6. Validação
prev_valid = rede.predict(X_valid)
print("Acurácia validação:", accuracy_score(y_valid, prev_valid))

# 7. Teste final
prev_teste = rede.predict(X_teste)
print("Acurácia teste:", accuracy_score(y_teste, prev_teste))

matriz = confusion_matrix(y_teste, prev_teste, labels=[0, 1, 2])

print("\n" + "="*50)
print("MATRIZ DE CONFUSÃO")
print("="*50)
print(matriz)

print("\n" + "="*50)
print("RELATÓRIO DE CLASSIFICAÇÃO")
print("="*50)
print(classification_report(y_teste, prev_teste, labels=[0, 1, 2], zero_division=0))

