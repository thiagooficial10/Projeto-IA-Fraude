import pandas as pd
import psycopg2

# Caminho do seu CSV
csv_path = r'C:\Users\thiago.ferreira\Downloads\MEUS PROJETOS\PROJETO DE IA\transacoes_financeiras_completa.csv'

# Leia o CSV
df = pd.read_csv(csv_path, sep=';')

# Conexão com o banco Neon
conn = psycopg2.connect(
    "postgresql://neondb_owner:npg_Gc9J5ydaIrRo@ep-gentle-resonance-a880bab4-pooler.eastus2.azure.neon.tech/neondb?sslmode=require&channel_binding=require"
)
cur = conn.cursor()

# Inserção no banco
for _, row in df.iterrows():
    valores = (
        row['TransacaoID'],
        row['ClienteID'],
        row['DataHora'],
        row['ValorTransacao'],
        row['Localizacao'],
        row['Canal'],
        row['TipoTransacao'],
        row['Dispositivo'],
        row['IdadeCliente'],
        row['CidadeResidencia'],
        row['EstadoResidencia'],
        row['DispositivoPreferido'],
        row['DistanciaKM'],
        row['TransacoesUltimos10min'],
        row['TempoContaAbertaDias'],
        row['VPNDetectada'],
        row['SuspeitaFraude'],
        row['Fraude_IA'],
        row['FraudeConfirmada']
    )

    cur.execute("""
        INSERT INTO transacoes_financeiras (
            transacao_id, cliente_id, data_hora, valor_transacao, localizacao, canal,
            tipo_transacao, dispositivo, idade_cliente, cidade_residencia, estado_residencia,
            dispositivo_preferido, distancia_km, transacoes_ultimos_10min, tempo_conta_aberta_dias,
            vpn_detectada, suspeita_fraude, fraude_ia, fraude_confirmada
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, valores)

# Finaliza conexão
conn.commit()
cur.close()
conn.close()

print("Importação concluída com sucesso.")
