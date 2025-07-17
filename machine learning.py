import pandas as pd
import psycopg2
from datetime import time

# Conexão com o banco
conn = psycopg2.connect(
    "postgresql://neondb_owner:npg_Gc9J5ydaIrRo@ep-gentle-resonance-a880bab4-pooler.eastus2.azure.neon.tech/neondb?sslmode=require&channel_binding=require"
)

# Buscar apenas transações ainda não analisadas
query = "SELECT * FROM transacoes_financeiras WHERE fraude_verificada_IA IS NULL"
df = pd.read_sql_query(query, conn)

if df.empty:
    print("Nenhuma transação nova para analisar.")
    exit()

# Função para aplicar a regra
def aplicar_regra(row):
    hora = pd.to_datetime(row['data_hora']).time()
    is_madrugada = hora >= time(0, 0) and hora <= time(5, 59)
    valor_alto = row['valor_transacao'] > 1000
    if is_madrugada and valor_alto:
        return 'Sim'
    return 'Não'

# Aplica a regra
df['fraude_verificada_IA'] = df.apply(aplicar_regra, axis=1)

# Atualiza no banco
cur = conn.cursor()
for _, row in df.iterrows():
    cur.execute("""
        UPDATE transacoes_financeiras
        SET fraude_verificada_IA = %s
        WHERE transacao_id = %s
    """, (row['fraude_verificada_IA'], row['transacao_id']))

conn.commit()
cur.close()
conn.close()

print("Transações analisadas e coluna atualizada com sucesso.")
