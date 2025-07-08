import pandas as pd
import psycopg2

# Leia o CSV
df = pd.read_csv(r'C:\Users\thiago.ferreira\Downloads\MEUS PROJETOS\PROJETO DE IA\transacoes_financeiras_completa.csv', sep=';')

# Conecte ao banco (substitua abaixo com sua string do Neon)
conn = psycopg2.connect(
    "postgresql://neondb_owner:npg_Gc9J5ydaIrRo@ep-gentle-resonance-a880bab4-pooler.eastus2.azure.neon.tech/neondb?sslmode=require&channel_binding=require"
)

cur = conn.cursor()

for _, row in df.iterrows():
    valores = (
        row['TransacaoID'],
        row['ClienteID'],
        row['DataHora'],
        row['ValorTransacao'],
        row['Localizacao'],
        row['CanalCompra'],
        row['TipoTransacao'],
        row['Dispositivo'],
        row['IdadeCliente'],
        row['CidadeResidencia'],
        row['EstadoResidencia'],
        row['DispositivoPreferido'],
        row['DistanciaKM'],
        row['TransacoesUltimaHora'],
        row['TransacaoSuspeita']
    )
    
    cur.execute("""
        INSERT INTO transacoes_financeiras 
        (transacao_id, cliente_id, data_hora, valor_transacao, localizacao, canal_compra, tipo_transacao, dispositivo, 
         idade_cliente, cidade_residencia, estado_residencia, dispositivo_preferido, distancia_km, transacoes_ultima_hora, transacao_suspeita)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, valores)


conn.commit()
cur.close()
conn.close()
