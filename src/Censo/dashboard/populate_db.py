# Script para popular o banco de dados do Censo com dados fictícios
# Este script deve ser executado no ambiente Django configurado
# Certifique-se de que o Django esteja instalado e configurado corretamente
# para executar este script, use o comando:
# python populate_db.py
## Certifique-se de que o Django esteja configurado corretamente
# para executar este script, você deve estar no diretório raiz do projeto Django
# e o ambiente virtual ativado, se estiver usando um.
## Exemplo de uso:
# python manage.py shell < populate_db.py

import sys
import os
import django
import random
from faker import Faker
from datetime import date, timedelta

# Configura o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censo.settings') # Substitua 'Censo' pelo nome do seu projeto principal
django.setup()

# Importa os modelos após configurar o ambiente Django
from basico.models import Domicilio, Morador, Responsavel, TipoDomicilio, TipoConstrucao, Sexo, RacaCor

fake = Faker('pt_BR') # Usar dados em português do Brasil

# --- Constantes e Opções ---
NUM_DOMICILIOS = 1000
MIN_MORADORES_POR_DOMICILIO = 1
MAX_MORADORES_POR_DOMICILIO = 6

# Opções para campos que não são TextChoices (baseado em models.py)
ABASTECIMENTO_AGUA_OPCOES = ['1', '2', '3', '4', '5', '6', '7', '8']
DESTINO_ESGOTO_OPCOES = ['1', '2', '3', '4', '5', '6', '7', '8', '9'] # Exemplo, ajuste conforme seu modelo/questionário
COLETA_LIXO_OPCOES = ['1', '2', '3', '4', '5', '6']
PARENTESCO_OPCOES = [f'{i:02d}' for i in range(1, 21)] # 01 a 20
FAIXA_RENDIMENTO_OPCOES = [str(i) for i in range(0, 10)] # 0 a 9

# Lista simplificada de UFs e Municípios para dados fictícios
UFS_MUNICIPIOS = {
    'SP': ['São Paulo', 'Campinas', 'Santos', 'Ribeirão Preto'],
    'RJ': ['Rio de Janeiro', 'Niterói', 'Duque de Caxias'],
    'MG': ['Belo Horizonte', 'Uberlândia', 'Juiz de Fora'],
    'BA': ['Salvador', 'Feira de Santana', 'Vitória da Conquista'],
    'RS': ['Porto Alegre', 'Caxias do Sul', 'Pelotas'],
}

# --- Funções Auxiliares ---

def calcular_idade(data_nascimento):
    today = date.today()
    return today.year - data_nascimento.year - ((today.month, today.day) < (data_nascimento.month, data_nascimento.day))

def gerar_faixa_rendimento(renda_mensal):
    if renda_mensal is None:
        return '0' # Sem Rendimento
    if renda_mensal <= 500: return '1'
    if renda_mensal <= 1000: return '2'
    if renda_mensal <= 2000: return '3'
    if renda_mensal <= 3000: return '4'
    if renda_mensal <= 5000: return '5'
    if renda_mensal <= 10000: return '6'
    if renda_mensal <= 20000: return '7'
    if renda_mensal <= 100000: return '8'
    return '9' # 100.001 ou mais

# --- População do Banco de Dados ---

def populate():
    print("Iniciando a população do banco de dados...")

    # Limpar dados existentes (opcional, descomente se quiser recomeçar)
    # print("Limpando dados existentes...")
    # Responsavel.objects.all().delete()
    # Morador.objects.all().delete()
    # Domicilio.objects.all().delete()
    # print("Dados limpos.")

    domicilios_criados = 0
    moradores_criados = 0
    responsaveis_criados = 0

    for _ in range(NUM_DOMICILIOS):
        # Seleciona UF e Município aleatoriamente
        uf = random.choice(list(UFS_MUNICIPIOS.keys()))
        municipio = random.choice(UFS_MUNICIPIOS[uf])

        # Cria Domicílio
        domicilio = Domicilio.objects.create(
            uf=uf,
            municipio=municipio,
            especie=random.choice([choice[0] for choice in TipoDomicilio.choices]),
            tipo=random.choice([choice[0] for choice in TipoConstrucao.choices]),
            abastecimento_agua=random.choice(ABASTECIMENTO_AGUA_OPCOES),
            banheiros=random.randint(1, 3), # 1 a 3 banheiros
            destino_esgoto=random.choice(DESTINO_ESGOTO_OPCOES),
            coleta_lixo=random.choice(COLETA_LIXO_OPCOES)
        )
        domicilios_criados += 1

        num_moradores = random.randint(MIN_MORADORES_POR_DOMICILIO, MAX_MORADORES_POR_DOMICILIO)
        moradores_do_domicilio = []

        for i in range(num_moradores):
            sexo_choice = random.choice([choice[0] for choice in Sexo.choices])
            nome = fake.first_name_male() if sexo_choice == Sexo.MASCULINO else fake.first_name_female()
            sobrenome = fake.last_name()

            # Gera data de nascimento e idade
            # Idade entre 0 e 90 anos
            idade = random.randint(0, 90)
            data_nascimento = date.today() - timedelta(days=idade * 365 + random.randint(0, 364))

            # Define parentesco (o primeiro morador é o responsável potencial)
            parentesco = '01' if i == 0 else random.choice(PARENTESCO_OPCOES[1:]) # 01 para o primeiro, outros para os demais

            # Dados de raça/cor e indígenas
            raca_cor_choice = random.choice([choice[0] for choice in RacaCor.choices])
            considera_indigena = raca_cor_choice == RacaCor.INDIGENA.value and random.random() < 0.8 # 80% de chance se for indígena
            etnia_indigena = fake.word() if considera_indigena else ''
            fala_lingua_indigena = considera_indigena and random.random() < 0.5 # 50% de chance se considerar indígena

            # Alfabetização (mais provável para idades > 7)
            alfabetizado = None # Pode ser null
            if idade >= 5: # Alfabetização é para >= 5 anos
                 alfabetizado = random.random() < (0.2 + (idade / 100.0)) # Probabilidade aumenta com a idade

            morador = Morador.objects.create(
                domicilio=domicilio,
                nome=nome,
                sobrenome=sobrenome,
                sexo=sexo_choice,
                data_nascimento=data_nascimento,
                idade=idade,
                parentesco=parentesco,
                raca_cor=raca_cor_choice,
                considera_indigena=considera_indigena,
                etnia_indigena=etnia_indigena,
                fala_lingua_indigena=fala_lingua_indigena,
                alfabetizado=alfabetizado
            )
            moradores_do_domicilio.append(morador)
            moradores_criados += 1

        # Seleciona um morador para ser o responsável (geralmente o primeiro, mas pode ser outro)
        if moradores_do_domicilio:
            responsavel_morador = moradores_do_domicilio[0] # O primeiro morador é o responsável
            
            # Gera renda mensal e faixa de rendimento para o responsável
            # Renda mais provável de ser None ou baixa
            if random.random() < 0.1: # 10% sem renda
                 renda_mensal = None
            else:
                 # Renda entre 500 e 20000 (distribuição logarítmica para simular desigualdade)
                 renda_mensal = round(random.uniform(500, 20000) ** random.uniform(0.8, 1.2), 2)
                 # Limita a renda máxima para evitar valores extremos
                 renda_mensal = min(renda_mensal, 150000)

            faixa_rendimento = gerar_faixa_rendimento(renda_mensal)

            Responsavel.objects.create(
                morador=responsavel_morador,
                renda_mensal=renda_mensal,
                faixa_rendimento=faixa_rendimento
            )
            responsaveis_criados += 1

        if domicilios_criados % 100 == 0:
            print(f"Criados {domicilios_criados} domicílios...")

    print("\nPopulação concluída!")
    print(f"Total de Domicílios criados: {domicilios_criados}")
    print(f"Total de Moradores criados: {moradores_criados}")
    print(f"Total de Responsáveis criados: {responsaveis_criados}")

if __name__ == '__main__':
    populate()