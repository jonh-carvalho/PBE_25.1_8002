import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Função para gerar dados fictícios
def gerar_dados_ficticios(num_domicilios=1000, num_max_moradores_por_domicilio=5):
    """
    Gera um DataFrame do Pandas com dados fictícios do censo.
    """
    ufs = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
    municipios_por_uf = {uf: [f'Município {i+1}-{uf}' for i in range(np.random.randint(1, 5))] for uf in ufs}

    especie_domicilio_opcoes = {
        1: 'DOMICÍLIO PARTICULAR PERMANENTE OCUPADO',
        5: 'DOMICÍLIO PARTICULAR IMPROVISADO OCUPADO',
        6: 'DOMICÍLIO COLETIVO COM MORADOR'
    }
    
    tipo_domicilio_opcoes = {
        '011': 'CASA', '012': 'CASA DE VILA OU EM CONDOMÍNIO', '013': 'APARTAMENTO',
        '014': 'HABITAÇÃO EM CASA DE CÔMODOS OU CORTIÇO',
        '051': 'TENDA OU BARRACA',
        '061': 'ASILO', '062': 'HOTEL OU PENSÃO'
    }

    sexo_opcoes = {1: 'MASCULINO', 2: 'FEMININO'}
    cor_raca_opcoes = {1: 'BRANCA', 2: 'PRETA', 3: 'AMARELA', 4: 'PARDA', 5: 'INDÍGENA'}
    
    abastecimento_agua_opcoes = {
        1: 'REDE GERAL DE DISTRIBUIÇÃO', 2: 'POÇO PROFUNDO OU ARTESIANO', 3: 'POÇO RASO, FREÁTICO OU CACIMBA',
        4: 'FONTE, NASCENTE OU MINA', 5: 'CARRO-PIPA', 6: 'ÁGUA DA CHUVA ARMAZENADA',
        7: 'RIOS, AÇUDES, CÓRREGOS, LAGOS E IGARAPÉS', 8: 'OUTRA FORMA'
    }
    
    esgoto_opcoes = {
        1: 'REDE GERAL OU PLUVIAL', 2: 'FOSSA SÉPTICA LIGADA À REDE', 3: 'FOSSA SÉPTICA NÃO LIGADA À REDE',
        4: 'FOSSA RUDIMENTAR OU BURACO', 5: 'VALA', 6: 'RIO, LAGO, CÓRREGO OU MAR', 7: 'OUTRA FORMA'
    }
    
    lixo_opcoes = {
        1: 'COLETADO NO DOMICÍLIO POR SERVIÇO DE LIMPEZA', 2: 'DEPOSITADO EM CAÇAMBA DE SERVIÇO DE LIMPEZA',
        3: 'QUEIMADO NA PROPRIEDADE', 4: 'ENTERRADO NA PROPRIEDADE',
        5: 'JOGADO EM TERRENO BALDIO, ENCOSTA OU ÁREA PÚBLICA', 6: 'OUTRO DESTINO'
    }

    renda_faixa_opcoes = {
        1: 'R$ 1,00 A R$ 500,00', 2: 'R$ 501,00 A R$ 1.000,00', 3: 'R$ 1.001,00 A R$ 2.000,00',
        4: 'R$ 2.001,00 A R$ 3.000,00', 5: 'R$ 3.001,00 A R$ 5.000,00', 6: 'R$ 5.001,00 A R$ 10.000,00',
        7: 'R$ 10.001,00 A R$ 20.000,00', 8: 'R$ 20.001,00 A R$ 100.000,00', 9: 'R$ 100.001,00 OU MAIS',
        0: 'SEM RENDIMENTO' # Adicionado para quem não tem rendimento
    }
    
    sabe_ler_escrever_opcoes = {1: 'SIM', 2: 'NÃO'}

    dados_domicilios = []
    dados_moradores = []
    id_morador_global = 0

    for i in range(num_domicilios):
        id_domicilio = f'DOM{i+1:05d}'
        uf_escolhida = np.random.choice(ufs)
        municipio_escolhido = np.random.choice(municipios_por_uf[uf_escolhida])
        especie_dom_cod = np.random.choice(list(especie_domicilio_opcoes.keys()))
        tipo_dom_cod = np.random.choice(list(tipo_domicilio_opcoes.keys()))
        
        abastecimento_cod = np.random.choice(list(abastecimento_agua_opcoes.keys()))
        esgoto_cod = np.random.choice(list(esgoto_opcoes.keys()))
        lixo_cod = np.random.choice(list(lixo_opcoes.keys()))
        
        # Renda é por domicílio (para o responsável)
        renda_responsavel_cod = np.random.choice(list(renda_faixa_opcoes.keys()))

        num_moradores_neste_domicilio = np.random.randint(1, num_max_moradores_por_domicilio + 1)
        
        dados_domicilios.append({
            'ID_DOMICILIO': id_domicilio,
            'UF': uf_escolhida,
            'MUNICIPIO': municipio_escolhido,
            'ESPECIE_DOMICILIO_COD': especie_dom_cod,
            'ESPECIE_DOMICILIO_DESC': especie_domicilio_opcoes[especie_dom_cod],
            'TIPO_DOMICILIO_COD': tipo_dom_cod,
            'TIPO_DOMICILIO_DESC': tipo_domicilio_opcoes[tipo_dom_cod],
            'ABASTECIMENTO_AGUA_COD': abastecimento_cod,
            'ABASTECIMENTO_AGUA_DESC': abastecimento_agua_opcoes[abastecimento_cod],
            'ESGOTO_COD': esgoto_cod,
            'ESGOTO_DESC': esgoto_opcoes[esgoto_cod],
            'LIXO_COD': lixo_cod,
            'LIXO_DESC': lixo_opcoes[lixo_cod],
            'RENDA_FAIXA_RESPONSAVEL_COD': renda_responsavel_cod,
            'RENDA_FAIXA_RESPONSAVEL_DESC': renda_faixa_opcoes[renda_responsavel_cod],
            'NUM_MORADORES': num_moradores_neste_domicilio
        })

        for j in range(num_moradores_neste_domicilio):
            id_morador_global += 1
            sexo_cod = np.random.choice(list(sexo_opcoes.keys()))
            cor_raca_cod = np.random.choice(list(cor_raca_opcoes.keys()))
            idade = np.random.randint(0, 100)
            sabe_ler_escrever_cod = np.random.choice(list(sabe_ler_escrever_opcoes.keys())) if idade >= 5 else 2 # Só para maiores de 5 anos

            dados_moradores.append({
                'ID_MORADOR': f'MOR{id_morador_global:07d}',
                'ID_DOMICILIO': id_domicilio,
                'SEXO_COD': sexo_cod,
                'SEXO_DESC': sexo_opcoes[sexo_cod],
                'IDADE': idade,
                'COR_RACA_COD': cor_raca_cod,
                'COR_RACA_DESC': cor_raca_opcoes[cor_raca_cod],
                'SABE_LER_ESCREVER_COD': sabe_ler_escrever_cod,
                'SABE_LER_ESCREVER_DESC': sabe_ler_escrever_opcoes[sabe_ler_escrever_cod] if idade >=5 else sabe_ler_escrever_opcoes[2]
            })
            
    df_domicilios = pd.DataFrame(dados_domicilios)
    df_moradores = pd.DataFrame(dados_moradores)
    
    # Juntar os dataframes
    df_completo = pd.merge(df_moradores, df_domicilios, on='ID_DOMICILIO', how='left')
    
    return df_completo