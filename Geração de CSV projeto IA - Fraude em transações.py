import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

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
    tempo_conta = random.randint(1, 3650)
    clientes.append({
        'ClienteID': cliente_id,
        'Idade': idade,
        'CidadeResidencia': cidade,
        'EstadoResidencia': estado,
        'DispositivoPreferido': dispositivo_pref,
        'TempoContaAbertaDias': tempo_conta
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
    tempo_conta = cliente['TempoContaAbertaDias']

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
    vpn_detectada = random.choices([0, 1], weights=[0.95, 0.05])[0]

    horario = data_hora.hour

    # Regras aprimoradas de suspeita
    if (valor > 1000 and 0 <= horario < 5) or (valor > 5000 and tipo in ['Pix', 'Boleto']):
        suspeita_fraude = "Sim"
    else:
        suspeita_fraude = "Não"

    ia_fraude = None
    fraude_real = "Sim" if random.random() < 0.05 else "Não"

    transacoes.append([
        i, cliente_id, data_hora, valor, localizacao, canal, tipo, dispositivo,
        idade, cidade_res, estado_res, dispositivo_pref, distancia_km,
        transacoes_recentes, tempo_conta, vpn_detectada,
        suspeita_fraude, ia_fraude, fraude_real
    ])

# Criar DataFrame
df = pd.DataFrame(transacoes, columns=[
    'TransacaoID', 'ClienteID', 'DataHora', 'ValorTransacao', 'Localizacao', 'Canal',
    'TipoTransacao', 'Dispositivo', 'IdadeCliente', 'CidadeResidencia', 'EstadoResidencia',
    'DispositivoPreferido', 'DistanciaKM', 'TransacoesUltimos10min',
    'TempoContaAbertaDias', 'VPNDetectada', 'SuspeitaFraude', 'Fraude_IA',
    'FraudeConfirmada'
])

# Exportar
df.to_csv(r'C:\Users\thiago.ferreira\Downloads\MEUS PROJETOS\PROJETO DE IA\transacoes_financeiras_completa.csv', index=False, sep=';')

print(df.head())
