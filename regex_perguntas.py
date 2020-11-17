import os
import os.path
import re
import pandas as pd

# PATH = '/mnt/e/bianca/possessorio/dados/dados_compilados/tipos'
PATH = '/mnt/e/bianca/possessorio/dados/dados_compilados/trf5'

dicionario = {
    'manutencao_posse':
    r'manuten\w{2}o\s+d[ea]\s+posse',
    'reintegracao_posse':
    r'reintegra\w{2}o\s+d[ea]\s+posse',
    'interdito_proibitorio':
    r'interdito\s+proibit\wrio',
    'coletiva':
    r'ocupantes|invasor[ea]s|desconhecid[oa]s|fam[ií]lias|morador[ea]s|invadiram|ocuparam|amea[cç]aram|esbulharam|turbaram|autor[ea]s|apelantes|apelados|demandados|embargantes|ambargados|agravantes|agravados|requeridos|invadiriam|ocupariam|amea[cç]am|esbulhariam|turbariam|ingressaram|desocuparem',
    'coletividade':
    r'[,.\s]movimento|[,.\s]frente|[,.\s]uni[aã]o|[,.\s]associa[çc][ãa]o|[,.\s]sindicato|comunidade',
    'idoso':
    r'[,.\s]idos[oa]s?',
    'crianca':
    r'[,.\s]crian[cç]a?|[,.\s]conselho\stutelar',
    'aud_just':
    r'[,.\s]audi[eê]ncia\sde\sjustifica[çc][aã]o',
    'insp_jud':
    r'[,.\s]inspe[çc][aã]o\sjudicial',
    'func_social':
    r'[,.\s]fun[çc][aã]o\s{1,3}social\s{1,3}da\s{1,3}propriedade',
    'aud_conciliacao':
    r'[,.\s]audi[eê]ncia\s{1,3}de\s{1,3}concilia[çc][aã]o|[,.\s]audi[eê]ncia\s{1,3}de\s{1,3}media[çc][aã]o',
    'usucapiao':
    r'[,.\s]usucapi[aã]o[,.\s]',
    'gaorp':
    r'gaorp|grupo\s{1,3}de\s{1,3}apoio\s{1,3}[aà]s\s{1,3}ordens\s{1,3}judiciais\s{1,3}de\s{1,3}reintegra[cç][aã]o\s{1,3}de\s{1,3}posse',
    'cejusc':
    r'cejusc|centro\s{1,3}judici[aá]rio\s{1,3}de\s{1,3}solu[cç][aã]o\s{1,3}de\s{1,3}conflitos\s{1,3}e\s{1,3}cidadania',
    'greve':
    r'greve[\s.,]?|sindicato|justi\wa\s?d[eo]\s?trabalho|livre\s?manifesta\w{2}o|piquete',
    'indigena':
    r'funai|funda\w{2}o\s?nacional\s?d[eo]\s?[íi]ndio|ind\wgena',
    'protesto':
    r'direito\sd[ea]\smanifestação|direito\sa\smanifestação|manifestante[s]?',
    'quilombola':
    r'funda[çc][aã]o\scultural\spalmares|fcp|funda\w{2}o\s?palmares|quilombo|quilombolas',
    'agrario':
    r'incra|instituto\s?nacional\s?d[ea]\s?coloniza\w{2}o\s?e?\s?reforma\s?agr\wria|produtiva|improdutiva|reforma\s?agr\wria|mst|movimento\s?sem\s?terra|sem\s?terra|assentamento',
    'moradia':
    r'aeis|[\s,\.][aá]rea\sespecial\sde\sinteresse\ssocial|aglomerado[s]|assentamento\sirregular|assentamento\sinformal|bolsa[\s-]aluguel|corti[cç]o|favela|fundi[áa]ri[ao]|grota|habita[cç][ãa]o|habitacional|habitam|loteamento\sinformal|loteamento\sirregular|loteamento\sclandestino|mocambo|moradia|moram|palafita|parcelamento|residem|urban[ao]|[\s,\.]vila[\s,\.]|zeis|[\s,\.]zona\sespecial\sde\sinteresse\ssocial'
}

for filename in os.listdir(PATH):
    if filename.endswith('csv'):
        df = pd.read_csv(os.path.join(PATH, filename), error_bad_lines=False)
        rows = []
        for _, row in df.iterrows():
            linha = dict()
            linha['numero_processo'] = row.numero_processo
            linha['tribunal'] = row.tribunal
            linha['texto_publicacao'] = row.texto_publicacao

            for k, v in dicionario.items():
                if re.search(v, row.texto_publicacao, re.S | re.I):
                    linha[k] = 1
                else:
                    linha[k] = 0
            rows.append(linha)
        df = pd.DataFrame(rows)
        rows = []
        processos = df.numero_processo.unique()
        for numero_proc in processos:
            linha = dict()
            linha['numero_processo'] = numero_proc
            linha['tribunal'] = df[df.numero_processo ==
                                numero_proc].tribunal.iloc[0]
            linha['total_publicacao'] = len(
                df[df.numero_processo == numero_proc].tribunal)
            linha['manutencao_posse'] = df[df.numero_processo ==
                                        numero_proc].manutencao_posse.sum()
            linha['reintegracao_posse'] = df[df.numero_processo ==
                                            numero_proc].reintegracao_posse.sum()
            linha['interdito_proibitorio'] = df[
                df.numero_processo == numero_proc].interdito_proibitorio.sum()
            linha['coletiva'] = df[df.numero_processo ==
                                numero_proc].coletiva.sum()
            linha['coletividade'] = df[df.numero_processo ==
                                    numero_proc].coletividade.sum()
            linha['idoso'] = df[df.numero_processo == numero_proc].idoso.sum()
            linha['crianca'] = df[df.numero_processo == numero_proc].crianca.sum()
            linha['aud_just'] = df[df.numero_processo ==
                                numero_proc].aud_just.sum()
            linha['insp_jud'] = df[df.numero_processo ==
                                numero_proc].insp_jud.sum()
            linha['func_social'] = df[df.numero_processo ==
                                    numero_proc].func_social.sum()
            linha['aud_conciliacao'] = df[df.numero_processo ==
                                        numero_proc].aud_conciliacao.sum()
            linha['usucapiao'] = df[df.numero_processo ==
                                    numero_proc].usucapiao.sum()
            linha['gaorp'] = df[df.numero_processo == numero_proc].gaorp.sum()
            linha['cejusc'] = df[df.numero_processo == numero_proc].cejusc.sum()
            linha['greve'] = df[df.numero_processo == numero_proc].greve.sum()
            linha['indigena'] = df[df.numero_processo ==
                                numero_proc].indigena.sum()
            linha['protesto'] = df[df.numero_processo ==
                                numero_proc].protesto.sum()
            linha['quilombola'] = df[df.numero_processo ==
                                    numero_proc].quilombola.sum()
            linha['agrario'] = df[df.numero_processo == numero_proc].agrario.sum()
            linha['moradia'] = df[df.numero_processo == numero_proc].moradia.sum()
            rows.append(linha)
        df = pd.DataFrame(rows)
        with pd.ExcelWriter(os.path.join(PATH, f'{filename[:-4]}_resumo.xlsx'),
                            engine='openpyxl',
                            mode='w') as writer:
            df.to_excel(writer, index=False)
