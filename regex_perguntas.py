import os
import re
import os.path
import pandas as pd
import numpy as np
from itertools import islice

path = '/mnt/d/Dados/trf1_corrigido'
filename = 'extracao_possessoria_final.csv'

dicionario = {
    'coletividade': r'[,.\s]movimento|[,.\s]frente|[,.\s]uni[aã]o|[,.\s]associa[çc][ãa]o|[,.\s]sindicato|comunidade',
    'idoso': r'[,.\s]idos[oa]s?',
    'crianca': r'[,.\s]crian[cç]a?|[,.\s]conselho\stutelar',
    'aud_just': r'[,.\s]audi[eê]ncia\sde\sjustifica[çc][aã]o',
    'insp_jud': r'[,.\s]inspe[çc][aã]o\sjudicial',
    'coletiva':r'ocupantes|invasor[ea]s|desconhecid[oa]s|fam[ií]lias|morador[ea]s|invadiram|ocuparam|amea[cç]aram|esbulharam|turbaram|autor[ea]s|apelantes|apelados|demandados|embargantes|ambargados|agravantes|agravados|requeridos|invadiriam|ocupariam|amea[cç]am|esbulhariam|turbariam|ingressaram|desocuparem',

    'greve':r'greve[\s.,]?|sindicato|justi\wa\s?d[eo]\s?trabalho|livre\s?manifesta\w{2}o|piquete',
    'indigena':r'funai|funda\w{2}o\s?nacional\s?d[eo]\s?[íi]ndio|ind\wgena',
    'protesto':r'direito\sd[ea]\smanifestação|direito\sa\smanifestação|manifestante[s]?',
    'quilombola':r'funda[çc][aã]o\scultural\spalmares|fcp|funda\w{2}o\s?palmares|quilombo|quilombolas',
    'agrario':r'incra|instituto\s?nacional\s?d[ea]\s?coloniza\w{2}o\s?e?\s?reforma\s?agr\wria|produtiva|improdutiva|reforma\s?agr\wria|mst|movimento\s?sem\s?terra|sem\s?terra|assentamento',
    'moradia':r'aeis|[\s,\.][aá]rea\sespecial\sde\sinteresse\ssocial|aglomerado[s]|assentamento\sirregular|assentamento\sinformal|bolsa[\s-]aluguel|corti[cç]o|favela|fundi[áa]ri[ao]|grota|habita[cç][ãa]o|habitacional|habitam|loteamento\sinformal|loteamento\sirregular|loteamento\sclandestino|mocambo|moradia|moram|palafita|parcelamento|residem|urban[ao]|[\s,\.]vila[\s,\.]|zeis|[\s,\.]zona\sespecial\sde\sinteresse\ssocial'
}

info = {
    'parte_ativa': r'[,.\s]reclamante[s]?\s*:\s*(.+)|[,.\s]requerente[s]?\s*:\s*(.+)|[,.\s]autor[aes\s\(\)]?\s*:\s*(.+)|[,.\s]exequente.[s]?\s*:\s*(.+)|[,.\s]recorrente[s]?:(.+)',
    'parte_passiva': r'[,.\s]r[eé]u\s*:*\s*(.+)|[,.\s]reclamad[oas\(\)]?\s*:*\s*(.+)|[,.\s]requerid[oas\(\)]\s*:*\s*(.+)|[,.\s]executad[oas\(\)]?\s*:\s*(.+)|[,.\s]recorrid[oas\(\)]?:(.+)',
    'comarca': r'[,.\s]comarca(.+)|[,.\s]vara(.+)'
}

df = pd.read_csv(os.path.join(path, filename), sep=',', error_bad_lines = False).sort_values(by=['numero_processo'])
rows = []

# for number in np.sort(df.numero_processo.unique()):
#     linha = dict()
#     flag = False
    
#     for _,row in df.iterrows():
#         if row.tribunal[:3] != 'trf' and row.numero_processo == number:
#             linha['tribunal'] = row.tribunal
#             linha['numero_processo'] = row.numero_processo
#             flag = True
            
#             for k, v in dicionario.items():
#                 try:
#                     if re.search(v, row.texto_publicacao, re.S | re.I) or linha[k] == 1:
#                         linha[k] = 1
#                     else:
#                         linha[k] = 0
#                 except:
#                     if re.search(v, row.texto_publicacao, re.S | re.I):
#                         linha[k] = 1
#                     else:
#                         linha[k] = 0
#         elif row.tribunal[:3] != 'trf' and row.numero_processo != number and flag:
#             rows.append(linha)
#             break

for _,row in df.iterrows():
    if row.tribunal[:3] != 'trf':
        linha = dict()
        linha['tribunal'] = row.tribunal
        linha['numero_processo'] = row.numero_processo
        linha['texto_publicacao'] = row.texto_publicacao
        linha['data'] = row.data

        for k, v in dicionario.items():
            if re.search(v, row.texto_publicacao, re.S | re.I):
                linha[k] = 1
            else:
                linha[k] = 0

        # for k, v in info.items():
        #     if re.search(v, row.texto_publicacao, re.S | re.I):
        #         linha[k] = re.search(v, row.texto_publicacao, re.S | re.I).group(0)
        #     else:
        #         linha[k] = 0
        rows.append(linha)
    
data_frame = pd.DataFrame(rows)

with pd.ExcelWriter(os.path.join(path, f'extracao_final_full_regex.xlsx'),
                    engine='openpyxl',
                    mode='w') as writer:
    data_frame.to_excel(writer, sheet_name='arquivo', index=False)
