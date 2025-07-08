import pandas as pd
import psycopg2
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Conectando ao banco de dados Neon (PostgreSQL)
conn = psycopg2.connect(
    "postgresql://neondb_owner:npg_Gc9J5ydaIrRo@ep-gentle-resonance-a880bab4-pooler.eastus2.azure.neon.tech/neondb?sslmode=require&channel_binding=require"
)

# Carregar os dados para um DataFrame
query = "SELECT * FROM transacoes_financeiras"
df = pd.read_sql_query(query, conn)
conn.close()

# Visualizando as primeiras linhas
print(df.head())

# Definindo as variáveis independentes (X) e a variável alvo (y)
X = df[['cliente_id', 'valor_transacao', 'localizacao', 'canal_compra', 'tipo_transacao', 'dispositivo']]
y = df['transacao_suspeita']

# Separar variáveis numéricas e categóricas
categorical_features = ['localizacao', 'canal_compra', 'tipo_transacao', 'dispositivo']
numerical_features = ['cliente_id', 'valor_transacao']

print("Categorias e variáveis numéricas separadas com sucesso.")

# Criando transformador para variáveis categóricas
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

# Combinando transformações em um pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', categorical_transformer, categorical_features)
    ],
    remainder='passthrough'  # Deixa as numéricas como estão
)

# Separar dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f'Treino: {X_train.shape}, Teste: {X_test.shape}')

# Criando pipeline final com modelo
clf = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Treinamento do modelo
clf.fit(X_train, y_train)
print("Modelo treinado com sucesso.")

# Fazendo previsões
y_pred = clf.predict(X_test)

# Relatório de desempenho
print("Relatório de Classificação:")
print(classification_report(y_test, y_pred))


#Resumo das Principais Técnicas Usadas:
#One-Hot Encoding: Transforma textos em números.
#Random Forest: Modelo robusto para classificação binária.
#Pipeline: Mantém tudo organizado e reproduzível.
#train_test_split: Garante avaliação justa.