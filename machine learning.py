import pandas as pd
import psycopg2
from datetime import time

# Conexão com o banco
conn = psycopg2.connect(
    "postgresql://neondb_owner:npg_Gc9J5ydaIrRo@ep-gentle-resonance-a880bab4-pooler.eastus2.azure.neon.tech/neondb?sslmode=require&channel_binding=require"
)

# Buscar transações ainda não analisadas pela IA
query = """
SELECT * FROM transacoes_financeiras 
WHERE fraude_verificada_IA IS NULL
"""
df = pd.read_sql_query(query, conn)

if df.empty:
    print("Nenhuma transação nova para analisar.")
    exit()

# Aplicar a "regra simples" (valor alto + madrugada)
def aplicar_regra(row):
    hora = pd.to_datetime(row['data_hora']).time()
    is_madrugada = hora >= time(0, 0) and hora <= time(5, 59)
    valor_alto = row['valor_transacao'] > 1000
    if is_madrugada and valor_alto:
        return 'Sim'
    return 'Não'

df['suspeita_fraude_regra'] = df.apply(aplicar_regra, axis=1)

# Simular IA para transações suspeitas
def avaliar_por_ia(row):
    if row['suspeita_fraude_regra'] != 'Sim':
        return None  # Só analisa se a regra ativou

    risco = 0

    if row['cidade_transacao'] != row['cidade_cliente']:
        risco += 1
    if row['dispositivo'] != row['dispositivo_habitual']:
        risco += 1
    if row['vpn_detectada'] == 'Sim':
        risco += 1
    if row['transacoes_10_min'] >= 3:
        risco += 1
    if row['tempo_conta_aberta_dias'] < 30:
        risco += 1
    if row['categoria_gasto'] in ['Apostas', 'Criptomoeda', 'Jogos']:
        risco += 1
    if row['tipo_pagamento'] == 'Boleto' and row['tipo_pessoa'] == 'Física' and row['valor_transacao'] > 800:
        risco += 1
    if row['tipo_pagamento'] == 'PIX':
        risco += 1

    # Se risco >= 4, considera fraude
    return 'Sim' if risco >= 4 else 'Não'

df['fraude_verificada_IA'] = df.apply(avaliar_por_ia, axis=1)

# Atualizar no banco
cur = conn.cursor()
for _, row in df.iterrows():
    cur.execute("""
        UPDATE transacoes_financeiras
        SET 
            suspeita_fraude_regra = %s,
            fraude_verificada_IA = %s
        WHERE transacao_id = %s
    """, (
        row['suspeita_fraude_regra'],
        row['fraude_verificada_IA'],
        row['transacao_id']
    ))

conn.commit()
cur.close()
conn.close()

print("Transações analisadas e colunas atualizadas com sucesso.")
