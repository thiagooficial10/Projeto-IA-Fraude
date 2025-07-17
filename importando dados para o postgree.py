import pandas as pd
import psycopg2

# Caminho do seu CSV
csv_path = r'C:\Users\thiago.ferreira\Downloads\MEUS PROJETOS\PROJETO DE IA\transacoes_financeiras_completa.csv'

# Leia o CSV
df = pd.read_csv(csv_path, sep=';')

# Conecte ao banco Neon
conn = psycopg2.connect(
    "postgresql://neondb_owner:npg_Gc9J5ydaIrRo@ep-gentle-resonance-a880bab4-pooler.eastus2.azure.neon.tech/neondb?sslmode=require&channel_binding=require"
)

cur = conn.cursor()

# Itera e insere no banco
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
        row.get('fraude_verificada_IA', None)  # Preenche com None se estiver ausente
    )
    
    cur.execute("""
        INSERT INTO transacoes_financeiras 
        (transacao_id, cliente_id, data_hora, valor_transacao, localizacao, canal_compra, tipo_transacao, dispositivo, 
         idade_cliente, cidade_residencia, estado_residencia, dispositivo_preferido, distancia_km, transacoes_ultima_hora, fraude_verificada_IA)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (transacao_id) DO NOTHING;
    """, valores)

# Finaliza
conn.commit()
cur.close()
conn.close()

print("Importação concluída com sucesso.")
