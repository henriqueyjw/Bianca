import os
import re
import os.path
import pandas as pd

ini_path = '/mnt/e/bianca/possessorio/dados/trf1_versao_2'
final_path = '/mnt/e/bianca/possessorio/dados/dados_tipos'
files = os.listdir(ini_path)

class extracao():
# Define todos os tipos de informações de interesse da pesquisa, com filtro por tipo e as informações necessárias por tipo.
    def __init__(self, tipo):
        if tipo == 'agrario':
            self.tipo = tipo
            self.filtro = r'incra|instituto\s?nacional\s?d[ea]\s?coloniza\w{2}o\s?e?\s?reforma\s?agr\wria'
            self.dicionario = {
                'incra':
                r'incra|instituto\s?nacional\s?d[ea]\s?coloniza\w{2}o\s?e?\s?reforma\s?agr\wria',
                'produtiva_improdutiva':
                r'produtiva|improdutiva',
                'reforma_agraria':
                r'reforma\s?agr\wria',
                'sem_terra':
                r'mst|movimento\s?sem\s?terra|sem\s?terra',
                'assentamento':
                r'assentamento',
                'coletiva':
                r'ocupantes|invasor[ea]s|desconhecid[oa]s|fam[ií]lias|morador[ea]s|invadiram|ocuparam|amea[cç]aram|esbulharam|turbaram|autor[ea]s|apelantes|apelados|demandados|embargantes|ambargados|agravantes|agravados|requeridos|invadiriam|ocupariam|amea[cç]am|esbulhariam|turbariam|ingressaram|desocuparem'
            }

        if tipo == 'greve':
            self.tipo = tipo
            self.filtro = r'greve[\s.,]?|sindicato|justi\wa\s?d[eo]\s?trabalho'
            self.dicionario = {
                'greve':r'greve[\s.,]?',
                'sindicato':r'sindicato',
                'justica_trabalho':r'justi\wa\s?d[eo]\s?trabalho',
                'livre_manifestacao':r'livre\s?manifesta\w{2}o',
                'piquete':r'piquete',
                'coletiva':r'ocupantes|invasor[ea]s|desconhecid[oa]s|fam[ií]lias|morador[ea]s|invadiram|ocuparam|amea[cç]aram|esbulharam|turbaram|autor[ea]s|apelantes|apelados|demandados|embargantes|ambargados|agravantes|agravados|requeridos|invadiriam|ocupariam|amea[cç]am|esbulhariam|turbariam|ingressaram|desocuparem'
            }

        if tipo == 'indigena':
            self.tipo = tipo
            self.filtro = r'funai|funda\w{2}o\s?nacional\s?d[eo]\s?[íi]ndio|índio|ind\wgena'
            self.dicionario = {
                'funai':r'funai|funda\w{2}o\s?nacional\s?d[eo]\s?[íi]ndio',
                'indigena':r'ind\wgena',
                'coletiva':r'ocupantes|invasor[ea]s|desconhecid[oa]s|fam[ií]lias|morador[ea]s|invadiram|ocuparam|amea[cç]aram|esbulharam|turbaram|autor[ea]s|apelantes|apelados|demandados|embargantes|ambargados|agravantes|agravados|requeridos|invadiriam|ocupariam|amea[cç]am|esbulhariam|turbariam|ingressaram|desocuparem'
            }

        if tipo == 'protesto':
            self.tipo = tipo
            self.filtro = r'direito\sd[ea]\smanifestação|direito\sa\smanifestação|manifestante[s]?'
            self.dicionario = {
                'protesto':r'protesto',
                'direito_a_manifestacao':r'direito\sd[ea]\smanifesta\w{2}o|direito\sa\smanifesta\w{2}o',
                'invasao_ocupacao':r'invas\wo|ocupa\w{2}o',
                'manifestante':r'manifestante[s]?',
                'coletiva':r'ocupantes|invasor[ea]s|desconhecid[oa]s|fam[ií]lias|morador[ea]s|invadiram|ocuparam|amea[cç]aram|esbulharam|turbaram|autor[ea]s|apelantes|apelados|demandados|embargantes|ambargados|agravantes|agravados|requeridos|invadiriam|ocupariam|amea[cç]am|esbulhariam|turbariam|ingressaram|desocuparem'
            }

        if tipo == 'rolezinho':
            self.tipo = tipo
            self.filtro = r'direito\sd[ea]\smanifestação|direito\sa\smanifestação|manifestante[s]?|rolezinho|secundarista'
            self.dicionario = {
                'protesto':r'protesto',
                'direito_a_manifestacao':r'direito\sd[ea]\smanifesta\w{2}o|direito\sa\smanifesta\w{2}o',
                'invasao_ocupacao':r'invas\wo|ocupa\w{2}o',
                'manifestante':r'manifestante[s]?',
                'rolezinho':r'rolezinho',
                'jovens':r'jovens',
                'estudantes':r'estudantes',
                'secundarista':r'secundarista',
                'coletiva':r'ocupantes|invasor[ea]s|desconhecid[oa]s|fam[ií]lias|morador[ea]s|invadiram|ocuparam|amea[cç]aram|esbulharam|turbaram|autor[ea]s|apelantes|apelados|demandados|embargantes|ambargados|agravantes|agravados|requeridos|invadiriam|ocupariam|amea[cç]am|esbulhariam|turbariam|ingressaram|desocuparem'
            }

        if tipo == 'quilombo':
            self.tipo = tipo
            self.filtro = r'funda[çc][aã]o\scultural\spalmares|fcp|funda\w{2}o\s?palmares|quilombo|quilombolas'
            self.dicionario = {
                'palmares':r'funda[çc][aã]o\scultural\spalmares|fcp|funda\w{2}o\s?palmares',
                'quilombo':r'quilombo|quilombolas',
                'coletiva':r'ocupantes|invasor[ea]s|desconhecid[oa]s|fam[ií]lias|morador[ea]s|invadiram|ocuparam|amea[cç]aram|esbulharam|turbaram|autor[ea]s|apelantes|apelados|demandados|embargantes|ambargados|agravantes|agravados|requeridos|invadiriam|ocupariam|amea[cç]am|esbulhariam|turbariam|ingressaram|desocuparem'
            }
        
        if tipo == 'moradia':
            self.tipo = tipo
            self.filtro = r'aeis|[\s,\.][aá]rea\sespecial\sde\sinteresse\ssocial|aglomerado[s]|assentamento\sirregular|assentamento\sinformal|bolsa[\s-]aluguel|corti[cç]o|favela|fundi[áa]ri[ao]|grota|habita[cç][ãa]o|habitacional|habitam|loteamento\sinformal|loteamento\sirregular|loteamento\sclandestino|mocambo|moradia|moram|palafita|parcelamento|residem|urban[ao]|[\s,\.]vila[\s,\.]|zeis|[\s,\.]zona\sespecial\sde\sinteresse\ssocial'
            self.dicionario = {
                'aeis':r'aeis|[\s,\.][aá]rea\sespecial\sde\sinteresse\ssocial',
                'aglomerado':r'aglomerado[s]',
                'assentamento_irregular':r'assentamento\sirregular',
                'assentamento_informal':r'assentamento\sinformal',    
                'bolsa_aluguel':r'bolsa[\s-]aluguel',
                'cortico':r'corti[cç]o',
                'favela':r'favela',
                'fundiario':r'fundi[áa]ri[ao]',
                'grota':r'grota',
                'habitacao':r'habita[cç][ãa]o',
                'habitacional':r'habitacional',
                'habitam':r'habitam',
                'loteamento_informal':r'loteamento\sinformal',
                'loteamento_informal':r'loteamento\sirregular',
                'loteamento_clandestino':r'loteamento\sclandestino',
                'mocambo':r'mocambo',
                'moradia':r'moradia',
                'moram':r'moram',
                'palafita':r'palafita', 
                'parcelamento':r'parcelamento',
                'residem':r'residem',
                'urbano': r'urban[ao]',
                'vila':r'[\s,\.]vila[\s,\.]',
                'zeis':r'zeis|[\s,\.]zona\sespecial\sde\sinteresse\ssocial',
                'embargo':r'embargo[s]\sde\sterceiro',
                'coletiva':r'ocupantes|invasor[ea]s|desconhecid[oa]s|fam[ií]lias|morador[ea]s|invadiram|ocuparam|amea[cç]aram|esbulharam|turbaram|autor[ea]s|apelantes|apelados|demandados|embargantes|ambargados|agravantes|agravados|requeridos|invadiriam|ocupariam|amea[cç]am|esbulhariam|turbariam|ingressaram|desocuparem'
            }
        
        if tipo == 'enderecos':
            self.tipo = tipo
            self.filtro = r'aeis|[\s,\.][aá]rea\sespecial\sde\sinteresse\ssocial|aglomerado[s]|assentamento\sirregular|assentamento\sinformal|bolsa[\s-]aluguel|corti[cç]o|favela|fundi[áa]ri[ao]|grota|habita[cç][ãa]o|habitacional|habitam|loteamento\sinformal|loteamento\sirregular|loteamento\sclandestino|mocambo|moradia|moram|palafita|parcelamento|residem|urban[ao]|[\s,\.]vila[\s,\.]|zeis|[\s,\.]zona\sespecial\sde\sinteresse\ssocial'
            self.dicionario = {'endereco':r'im[oó]vel\s{1,3}situado\s{1,3}nesta\s{1,3}(.{1,150})|im[oó]vel\s{1,3}situado\s{1,3}n?[aà]\s{1,3}(.{1,150})|im[oó]vel\s{1,3}descrito\s{1,3}na\s{1,3}inicial\s{1,3}(.{1,150})|localizad[oa]s?\s{1,3}n?[oaà]\s{1,3}(.{1,150})|localizad[oa]s?,?\s{1,3}nesta\s{1,3}(.{1,150})|localizad[oa]s?,?\s{1,3}nesta\s{1,3}cidade,?\s{1,3}n?d?[eaà]\s{1,3}(.{1,150})|localizad[oa]s?,?\s{1,3}nesta\s{1,3}urbe,?\s{1,3}n?d?[eaà]\s{1,3}(.{1,150})|localizad[oa]s?,?\s{1,3}no\s{1,3}munic[ií]pio\s{1,3}e\s{1,3}comarca\s{1,3}de\s{1,3}s[aã]o\s{1,3}paulo,?\s{1,3}(.{1,150})|localizad[oa]s?,?\s{1,3}nesta\s{1,3}capital,?\s{1,3}n?[aà]\s{1,3}(.{1,150})|localizad[oa]s?,?\s{1,3}nestas?\s{1,3}localidades?,?\s{1,3}n?[aà]\s{1,3}(.{1,150})|pertence\s{1,3}às\s{1,3}ruas(.{1,150})|situad[oa]s?\s{1,3}n?[aà]\s{1,3}(.{1,150})|[aá]rea\s{1,3}correspondete\s{1,3}[aà]o?\s{1,3}(.{1,150})|im[oó]vel\s{1,3}situado,?\s{1,3}pr[eé]dio\s{1,3}(.{1,150})|situad[oa]s?,?\s{1,3}nes[ts]a\s{1,3}cidade,?\s{1,3}(.{1,150})|situad[oa]s?,?\s{1,3}nes[ts]a\s{1,3}urbe,?\s{1,3}(.{1,150})|situad[oa]s?,?\s{1,3}nes[ts]a\s{1,3}capital,?\s{1,3}(.{1,150})|situa[-\s]se\s{1,3}na\s{1,3}(.{1,150})|sito\s{1,3}à\s{1,3}(.{1,150})|endere[cç]o\s{1,3}indicado\s{1,3}[eé]\s{1,3}(.{1,150})|endere[cç]o:?\s{1,3}(.{1,150})|loteamento\s{1,3}(.{1,150})|conjunto\s{1,3}habitacional\s{1,3}(.{1,150})|diligenciei\s{1,3}na\s{1,3}(.{1,150})|com\s{1,3}frente\s{1,3}para\s{1,3}(.{1,150})|do\s{1,3}apartamento\s{1,3}(.{1,150})|a\s{1,3}ser\s{1,3}cumprido\s{1,3}na\s{1,3}(.{1,150})|dirigi[-\s]{1,2}me\s{1,3}[aà]\s{1,3}(.{1,150})|dirigimos\s{1,3}[aà]\s{1,3}(.{1,150})',
            }

        if tipo == 'coletivas':
            self.tipo = tipo
            self.filtro = r'ocupantes|invasor[ea]s|desconhecid[oa]s|fam[ií]lias|morador[ea]s|invadiram|ocuparam|amea[cç]aram|esbulharam|turbaram|autor[ea]s|apelantes|apelados|demandados|embargantes|ambargados|agravantes|agravados|requeridos|invadiriam|ocupariam|amea[cç]am|esbulhariam|turbariam|ingressaram|desocuparem'
            self.dicionario = {'coletivas':r'ocupantes|invasor[ea]s|desconhecid[oa]s|fam[ií]lias|morador[ea]s|invadiram|ocuparam|amea[cç]aram|esbulharam|turbaram|autor[ea]s|apelantes|apelados|demandados|embargantes|ambargados|agravantes|agravados|requeridos|invadiriam|ocupariam|amea[cç]am|esbulhariam|turbariam|ingressaram|desocuparem',
            }

# Dado o tipo de informação, o arquivo de entrada e o DataFrame bruto, gera o DataFrame com a extração
    def database(self,filename,dados):
        rows = []
        for _,row in dados.iterrows():
            if not re.search(self.filtro,row['texto_publicacao'], re.S | re.I):
                continue

            flag = True

            if self.tipo == 'moradia':
                dicionario_expressoes_1 = {
                    'arred_residencial': r'programa\sde\sarrendamento\sresidencial',
                    'funai': r'funai|funda\w{2}o\s?nacional\s?d[eo]\s?[íi]ndio',
                    'incra': r'incra|instituto\s?nacional\s?d[ea]\s?coloniza\w{2}o\s?e?\s?reforma\s?agr\wria'
                }
                for k, v in dicionario_expressoes_1.items():
                    if re.search(v, row['texto_publicacao'], re.S | re.I):
                        flag = False
                        break   

            if flag:
                dici = dict()
                dici['numero_processo'] = row['numero_processo']
                dici['tribunal'] = filename[:-4]
                dici['texto_publicacao'] = row['texto_publicacao']
                dici['manutencao_posse'] = row['manutencao_posse']
                dici['reintegracao_posse'] = row['reintegracao_posse']
                dici['interdito_proibitorio'] = row['interdito_proibitorio']
                for k, v in self.dicionario.items():
                    if re.search(v, row['texto_publicacao'], re.S | re.I):
                        # dici[k] = re.search(v, row['texto_publicacao'], re.S | re.I).group(0)
                        dici[k] = 1
                    else:
                        dici[k] = 0
                
                if self.tipo == 'agrario':
                    if dici['sem_terra'] == 1:
                        dici['coletiva'] = 1
                    if re.search(r'assentados|sindicato', row['texto_publicacao'],
                                re.S | re.I):
                        dici['coletiva'] = 1
                
                if self.tipo == 'indigena':
                    if dici['funai'] ==1:
                        dici['coletiva'] = 1
                    if re.search(r'comunidade',row['texto_publicacao'], re.S|re.I):
                        dici['coletiva'] = 1
                    
                rows.append(dici)
                
        data_frame = pd.DataFrame(rows)
        return data_frame

# Dado o nome do arquivo original e DataFrame extraido, salva os dados em Excel
    def save(self,filename,dados):
        arquivo = filename[:-4]
        if filename == 'trf3.csv':
            with pd.ExcelWriter(os.path.join(final_path, f'{self.tipo}_trf3.xlsx'),
                                engine='openpyxl',
                                mode='w') as writer:
                dados.to_excel(writer, sheet_name=arquivo, index=False)
        else:
            with pd.ExcelWriter(os.path.join(final_path, f'{self.tipo}.xlsx'),
                                engine='openpyxl',
                                mode='a') as writer:
                dados.to_excel(writer, sheet_name=arquivo, index=False)

# Define o tipo de possessoria que gostaria de extrair dos dados.
def main():
    ext = extracao('agrario') # Possessórias Agrárias.
    for filename in files:
        df = pd.read_csv(os.path.join(ini_path, filename), sep=',')
        df_final = ext.database(filename, df)
        ext.save(filename,df_final)

    ext = extracao('greve') # Possessórias de Greves.
    for filename in files:
        df = pd.read_csv(os.path.join(ini_path, filename), sep=',')
        df_final = ext.database(filename, df)
        ext.save(filename,df_final)

    ext = extracao('indigena') # Possessórias Indígenas.
    for filename in files:
        df = pd.read_csv(os.path.join(ini_path, filename), sep=',')
        df_final = ext.database(filename, df)
        ext.save(filename,df_final)

    ext = extracao('protesto') # Possessórias de Protesto.
    for filename in files:
        df = pd.read_csv(os.path.join(ini_path, filename), sep=',')
        df_final = ext.database(filename, df)
        ext.save(filename,df_final)

    ext = extracao('quilombo') # Possessórias de Quilombos.
    for filename in files:
        df = pd.read_csv(os.path.join(ini_path, filename), sep=',')
        df_final = ext.database(filename, df)
        ext.save(filename,df_final)

    ext = extracao('moradia') # Possessórias de Moradias.
    for filename in files:
        df = pd.read_csv(os.path.join(ini_path, filename), sep=',')
        df_final = ext.database(filename, df)
        ext.save(filename,df_final)
        
    ext = extracao('enderecos') # Endereços nos Textos de Possessórias.
    for filename in files:
        df = pd.read_csv(os.path.join(path, filename), sep=',')
        df_final = ext.database(filename, df)
        ext.save(filename,df_final)

    ext = extracao('coletivas') # Possessórias Coletivas.
    for filename in files:
        df = pd.read_csv(os.path.join(path, filename), sep=',')
        df_final = ext.database(filename, df)
        ext.save(filename,df_final)

# Dá inicio ao processo de extração.
if __name__ == '__main__':
	main()
