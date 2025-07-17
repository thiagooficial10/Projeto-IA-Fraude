import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker('pt_BR')
np.random.seed(42)
random.seed(42)

# Parâmetros
num_transacoes = 20000
num_clientes = 1000

# Opções realistas
canais = ['App', 'Site', 'Agência']
tipos_transacao = ['Pix', 'Cartão', 'Boleto', 'Transferência']
estados = ['SP', 'RJ', 'MG', 'RS', 'SC', 'PR', 'GO']
dispositivos = ['Android', 'iOS', 'Desktop', 'Outro']
probs_dispositivos = [0.6, 0.35, 0.04, 0.01]

# Criar clientes
clientes = []
for cliente_id in range(1, num_clientes + 1):
    idade = random.randint(18, 85)
    cidade = fake.city()
    estado = random.choice(estados)
    dispositivo_pref = np.random.choice(dispositivos, p=probs_dispositivos)
    clientes.append({
        'ClienteID': cliente_id,
        'Idade': idade,
        'CidadeResidencia': cidade,
        'EstadoResidencia': estado,
        'DispositivoPreferido': dispositivo_pref
    })

# Criar transações
transacoes = []
for i in range(1, num_transacoes + 1):
    cliente = random.choice(clientes)
    cliente_id = cliente['ClienteID']
    idade = cliente['Idade']
    cidade_res = cliente['CidadeResidencia']
    estado_res = cliente['EstadoResidencia']
    dispositivo_pref = cliente['DispositivoPreferido']

    data_hora = fake.date_time_between(start_date='-180d', end_date='now')
    valor = round(np.random.exponential(scale=300), 2)
    valor = min(max(valor, 10), 15000)

    if random.random() < 0.8:
        cidade_trans = cidade_res
        estado_trans = estado_res
    else:
        cidade_trans = fake.city()
        estado_trans = random.choice(estados)

    localizacao = f"{cidade_trans} - {estado_trans}"
    canal = random.choice(canais)
    tipo = random.choice(tipos_transacao)
    dispositivo = np.random.choice(dispositivos, p=probs_dispositivos)

    if cidade_res == cidade_trans:
        distancia_km = 0
    elif estado_res == estado_trans:
        distancia_km = random.randint(50, 200)
    else:
        distancia_km = random.randint(200, 1500)

    transacoes_recentes = random.randint(0, 5)

    # Deixa a coluna de fraude vazia para IA preencher depois
    fraude_verificada = None

    transacoes.append([
        i, cliente_id, data_hora, valor, localizacao, canal, tipo, dispositivo,
        idade, cidade_res, estado_res, dispositivo_pref, distancia_km, transacoes_recentes, fraude_verificada
    ])

# Criar DataFrame
df = pd.DataFrame(transacoes, columns=[
    'TransacaoID', 'ClienteID', 'DataHora', 'ValorTransacao', 'Localizacao', 'CanalCompra',
    'TipoTransacao', 'Dispositivo', 'IdadeCliente', 'CidadeResidencia', 'EstadoResidencia',
    'DispositivoPreferido', 'DistanciaKM', 'TransacoesUltimaHora', 'FraudeVerificadaIA'
])

# Exportar CSV
df.to_csv(r'C:\Users\thiago.ferreira\Downloads\MEUS PROJETOS\PROJETO DE IA\transacoes_financeiras_completa.csv', index=False, sep=';')

print(df.head())
