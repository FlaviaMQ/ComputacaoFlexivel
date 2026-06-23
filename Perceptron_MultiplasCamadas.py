import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# 1. Ler a aba da planilha
dados = pd.read_excel("Conforto-Termico-anapolis.xlsm", sheet_name="treino1")

dados = dados.dropna(subset=["Temperatura", "UR", "Classe"])

# remove linhas totalmente vazias
dados = dados.dropna(how="all")

# remove linhas sem classe
dados = dados.dropna(subset=["Classe"])

# remove linhas com classe inválida
dados = dados[dados["Classe"].isin([0, 1, 2])]


# 2. Separar entradas e saída
X = dados[["Temperatura", "UR"]]
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

print("\nMatriz de confusão:")
print(confusion_matrix(y_teste, prev_teste))

print("\nRelatório de classificação:")
print(classification_report(y_teste, prev_teste))
