import os
import re
import os.path
import pandas as pd

path = '/mnt/d/Dados/trf1_corrigido'
filename = 'extracao_possessoria_final.csv'

dicionario = {
    'manutencao_posse': r'manuten\w{2}o\s+d[ea]\s+posse',
    'reintegracao_posse': r'reintegra\w{2}o\s+d[ea]\s+posse',
    'interdito_proibitorio': r'interdito\s+proibit\wrio',
    'turbacao_esbulho_ameaca': r'esbulh|amea\wa|turba'
}

df = pd.read_csv(os.path.join(path, filename), sep=',')
rows = []

for number in df.numero_processo.unique():
    linha = dict()
    flag = False
    for _,row in df.iterrows():
        if row.tribunal[:3] != 'trf' and row.numero_processo == number:
            linha['tribunal'] = row.tribunal
            linha['numero_processo'] = row.numero_processo
            flag = True
            for k, v in dicionario.items():
                try:
                    if re.search(v, row.texto_publicacao, re.S | re.I) or linha[k] == 1:
                        linha[k] = 1
                    else:
                        linha[k] = 0
                except:
                    if re.search(v, row.texto_publicacao, re.S | re.I):
                        linha[k] = 1
                    else:
                        linha[k] = 0
        elif row.tribunal[:3] != 'trf' and row.numero_processo != number and flag:
            break
    rows.append(linha)
data_frame = pd.DataFrame(rows)

with pd.ExcelWriter(os.path.join(path, f'extracao_final_regex.xlsx'),
                    engine='openpyxl',
                    mode='w') as writer:
    data_frame.to_excel(writer, sheet_name=arquivo, index=False)
