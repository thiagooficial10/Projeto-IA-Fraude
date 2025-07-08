import pandas as pd
import numpy as np
from faker import Faker  # Biblioteca para gerar dados fictícios e realistas
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

# Clientes (fixos)
clientes = []
for cliente_id in range(1, num_clientes + 1):
    idade = random.randint(18, 85)
    cidade = fake.city()
    estado = random.choice(estados)
    dispositivo_preferido = np.random.choice(dispositivos, p=probs_dispositivos)
    clientes.append({
        'ClienteID': cliente_id,
        'Idade': idade,
        'CidadeResidencia': cidade,
        'EstadoResidencia': estado,
        'DispositivoPreferido': dispositivo_preferido
    })
df_clientes = pd.DataFrame(clientes)

# Transações
transacoes = []
for i in range(1, num_transacoes + 1):
    cliente = random.choice(clientes)
    cliente_id = cliente['ClienteID']
    idade = cliente['Idade']
    cidade_res = cliente['CidadeResidencia']
    estado_res = cliente['EstadoResidencia']
    dispositivo_preferido = cliente['DispositivoPreferido']
    
    data_hora = fake.date_time_between(start_date='-180d', end_date='now')
    valor = round(np.random.exponential(scale=300), 2)
    valor = min(max(valor, 10), 15000)
    
    cidade_trans = fake.city()
    estado_trans = random.choice(estados)
    localizacao = f"{cidade_trans} - {estado_trans}"
    canal = random.choice(canais)
    tipo = random.choice(tipos_transacao)
    
    dispositivo = np.random.choice(dispositivos, p=probs_dispositivos)
    
    # Distância simulada (cidade igual = 0 km, estado igual = 50-200km, estados diferentes = 200-1500km)
    if cidade_res == cidade_trans:
        distancia_km = 0
    elif estado_res == estado_trans:
        distancia_km = random.randint(50, 200)
    else:
        distancia_km = random.randint(200, 1500)
    
    # Simula transações recentes (0 a 5 transações na última hora)
    transacoes_recentes = random.randint(0, 5)
    
    # Define transações na madrugada (1% das transações)
    is_madrugada = random.random() < 0.01
    hora = data_hora.hour
    if is_madrugada:
        hora = random.choice([0, 1, 2, 3, 4, 5])
        data_hora = data_hora.replace(hour=hora)
    
    # Regra simples: fraude apenas se for de madrugada e valor acima de 1000 (0,2% de chance)
    fraude = 0
    if is_madrugada and valor > 1000 and random.random() < 0.002:
        fraude = 1
    
    transacoes.append([
        i, cliente_id, data_hora, valor, localizacao, canal, tipo, dispositivo, 
        idade, cidade_res, estado_res, dispositivo_preferido, distancia_km, transacoes_recentes, fraude
    ])

# DataFrame
df_transacoes = pd.DataFrame(transacoes, columns=[
    'TransacaoID', 'ClienteID', 'DataHora', 'ValorTransacao', 'Localizacao', 'CanalCompra',
    'TipoTransacao', 'Dispositivo', 'IdadeCliente', 'CidadeResidencia', 'EstadoResidencia',
    'DispositivoPreferido', 'DistanciaKM', 'TransacoesUltimaHora', 'TransacaoSuspeita'
])

# Exporta CSV (modo acumulativo)
nome_arquivo = r'C:\Users\thiago.ferreira\Downloads\MEUS PROJETOS\PROJETO DE IA\transacoes_financeiras_completa.csv'
try:
    df_existente = pd.read_csv(nome_arquivo, sep=';')
    df_final = pd.concat([df_existente, df_transacoes], ignore_index=True)
except FileNotFoundError:
    df_final = df_transacoes

df_final.to_csv(nome_arquivo, index=False, sep=';')
print(df_final.head())
