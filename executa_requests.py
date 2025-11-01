import requests
import pandas as pd
from faz_login_config_request import sessao_data, driver
import os
from datetime import datetime
from urllib.parse import quote
import time


# Função auxiliar para converter string decimal (até 2 casas) para inteiro em centavos
def str_to_cents(value_str):
    if pd.isna(value_str) or value_str == '':
        return 0
    # Remove espaços e trata vírgula como ponto se necessário (comum em dados brasileiros)
    value_str = str(value_str).strip().replace(',', '.')
    if '.' in value_str:
        parts = value_str.split('.')
        integer_part = int(parts[0]) if parts[0] else 0
        decimal_part = parts[1].ljust(2, '0')[:2]  # Pega até 2 decimais, preenche com 0 se menos
        decimal_value = int(decimal_part)
        return integer_part * 100 + decimal_value
    else:
        return int(value_str) * 100  # Inteiro puro, multiplica por 100

# FUNÇÃO PARA FORMATAR A DATA DO FORMATO DD/MM/YYYY PARA O FORMATO UTILIZADO COMO PARÂMETRO NA URL
def formatar_data_params(data_antiga):
    data_obj = datetime.strptime(data_antiga, "%d/%m/%Y")
    data_str = data_obj.strftime("%a %b %d %Y")
    return quote(data_str)


# FUNÇÃO PARA CRIAR A SESSÃO DE USUÁRIO, RECUPERAR TODOS OS COOKIES SALVOS NO NAVEGADOR E ADICIONÁ-LOS A SESSÃO;
# ATUALIZA OS CABEÇALHOS DA SESSÃO PARA SEREM UTILIZADOS NAS REQUISIÇÕES
def criar_sessao():
    session = requests.Session()
    cookies_list = driver.get_cookies()
    for cookie in cookies_list:
        session.cookies.set(cookie['name'], cookie['value'])

    access_token = sessao_data.get('access_token')
    user_agent = driver.execute_script("return navigator.userAgent;")

    if not access_token:
        print("Token de acesso não encontrado no sessionStorage.")
        return

    session.headers.update({
        "accept": "application/json, text/plain, */*",
        "authorization": f"Bearer {access_token}",
        "connection": "keep-alive",
        "host": "educadf.se.df.gov.br",
        "sec-fetch-site": "same-origin",
        "user-agent": user_agent
    })

    return session


# FAZ A REQUISIÇÃO HTML E DEVOLVE A RESPOSTA DO SERVIDOR
def executar_request(session, url):
    response = session.get(url)
    if response.status_code != 200:
        print("Falha! Sessão expirada ou acesso negado. Reautenticando...")
        drive.quit()
        session_base = criar_sessao()
        response = session.get(url)
    return response


# DEFINE OS PARÂMETROS QUE SERÃO BUSCADOS
ano_letivo = '2025'
cre_id = '10104'  # codigo do cre
unidade_id = '4062'  # codigo da escola
data_quadro_aula = '30/06/2025'  # data do registro no EducaDF (Essa data pouco importa. O periodo_id é quem manda)
matricula_professor = '0'  # também não precisa para a query


#turmas_id_list = ['5031444']
#componentes_id_list = ['3']
#periodos_id_list = ['1']


#Criando a lista de turmas e de componentes

#df_turmas = pd.read_csv('turmas.csv')
#df_materias = pd.read_csv('materias.csv')

# Filtra as linhas conforme as condições
#filtro = (df_turmas['anoLetivo'] == 2025) & (df_turmas['codigoComponente'] == 0) 

# Extrai os ids das turmas que cumprem esses critérios
#turmas_id_list = df_turmas.loc[filtro, 'id'].astype(str).unique().tolist()
#componentes_id_list = df_materias['codigoComponente'].astype(str).unique().tolist()

#periodos_id_list =['3']

# CAMINHO BÁSICO DAS URLS QUE SERÃO UTILIZADAS NAS REQUISIÇÕES
#url_base_filtro_cre = "https://educadf.se.df.gov.br/educadffiltrocreapi/api/FiltroCre"
#url_base_diario = "https://educadf.se.df.gov.br/educadfdiarioapi/api"
#params_data_quadro_aula = formatar_data_params(data_quadro_aula)


#url_base_menu = "https://educadf.se.df.gov.br/educadfperfilapi/api/Menu"
url_GetAll = "https://educadf.se.df.gov.br/comumapi/api/redeensino/GetAll"
url_GetByUsuarioLogadoKeyClo = "https://educadf.se.df.gov.br/comumapi/api/perfil/GetByUsuarioLogadoKeyCloak"
url_GetRegionalEnsinoPorComp = "https://educadf.se.df.gov.br/comumapi/api/regionalensino/GetRegionalEnsinoPorComportamento?nrComportamento=3"
url_GetUnidadeEscolarByRedeEnsino = "https://educadf.se.df.gov.br/comumapi/api/UnidadeEscolar/GetUnidadeEscolarByRedeEnsinoELotacao/?idRedeEnsino=1"
url_GetUnidadeEscolarByRede = "https://educadf.se.df.gov.br/comumapi/api/UnidadeEscolar/GetUnidadeEscolarByRedeEnsinoERegionalEnsinoELotacao/?idRedeEnsino=1&idRegionalEnsino=10104"
url_GetTipoEnsinoPorUnidadeEs = "https://educadf.se.df.gov.br/matriculaapi/api/RelatorioPontosAcumulados/GetTipoEnsinoPorUnidadeEscolar?idUnidadeEscolar=4062"
url_GetSerieByAnoLetivoEscolar = "https://educadf.se.df.gov.br/matriculaapi/api/RelatorioPontosAcumulados/GetSerieByAnoLetivoEscola?anoLetivo=2025&idEscola=4062&cargoUsuarioLogado=TECNICO09"
url_GetTurmaByAnoLetivoEscolar = "https://educadf.se.df.gov.br/matriculaapi/api/RelatorioPontosAcumulados/GetTurmaByAnoLetivoEscolaSerie?anoLetivo=2025&idEscola=4062&idSerie=82&cargoUsuarioLogado=TECNICO09"
url_GetByFilter = "https://educadf.se.df.gov.br/matriculaapi/api/RelatorioPontosAcumulados/getByFilter?filter=%7B%22next%22%3A%2250%22%2C%22offset%22%3A%220%22%2C%22column%22%3A%22%22%2C%22direction%22%3A%22%22%2C%22searchTerm%22%3A%22%22%2C%22cargo%22%3A%22TECNICO09%22%2C%22codEscola%22%3A4062%2C%22anoLetivo%22%3A2025%2C%22tipoEnsinoId%22%3A10%2C%22serieId%22%3A82%2C%22turmaId%22%3A5031444%2C%22bimestreId%22%3A3%7D"
# ======== INÍCIO DAS CHAMADAS FORA DA ITERAÇÃO ===========
session_base = criar_sessao()

# Cria a pasta para salvar os CSV, caso ainda não exista
pasta = 'dados_csv'
os.makedirs(pasta, exist_ok=True)

# URL_BASE + PARÂMETROS
#cre_request_URL = f"{url_base_filtro_cre}/lista-cre"
#escola_request_URL = f"{url_base_filtro_cre}/cre/{cre_id}/lista-escola"
#turmas_request_URL = f"{url_base_filtro_cre}/unidade/{unidade_id}/lista-turma?matriculaProfessor={matricula_professor}"
#professores_request_URL = f"{url_base_filtro_cre}/unidade/{unidade_id}/lista-professor?anoLetivo={ano_letivo}"

# REQUISIÇÕES HTML
#response_cre = executar_request(session_base, cre_request_URL)
#response_escola = executar_request(session_base, escola_request_URL)
#response_turmas = executar_request(session_base, turmas_request_URL)
#response_professores = executar_request(session_base, professores_request_URL)

response_GetAll = executar_request(session_base, url_GetAll)
response_GetByUsuarioLogadoKeyClo = executar_request(session_base, url_GetByUsuarioLogadoKeyClo)
response_GetRegionalEnsinoPorComp = executar_request(session_base, url_GetRegionalEnsinoPorComp)
response_GetUnidadeEscolarByRedeEnsino = executar_request(session_base, url_GetUnidadeEscolarByRedeEnsino)
response_GetUnidadeEscolarByRede = executar_request(session_base, url_GetUnidadeEscolarByRede)
response_GetTipoEnsinoPorUnidadeEs = executar_request(session_base, url_GetTipoEnsinoPorUnidadeEs)
response_GetSerieByAnoLetivoEscolar = executar_request(session_base, url_GetSerieByAnoLetivoEscolar)
response_GetTurmaByAnoLetivoEscolar = executar_request(session_base, url_GetTurmaByAnoLetivoEscolar)
response_GetByFilter = executar_request(session_base, url_GetByFilter)


# CONVERTE AS RESPONSES EM DATAFRAMES PANDAS
#df_cre = pd.DataFrame(response_cre.json()['data'])
#df_escola = pd.DataFrame(response_escola.json()['data'])
#df_turmas = pd.DataFrame(response_turmas.json()['data'])
#df_professores = pd.DataFrame(response_professores.json()['data'])

df_GetAll = pd.DataFrame(response_GetAll.json()['data'])
df_GetByUsuario = pd.DataFrame(response_GetByUsuarioLogadoKeyClo.json()['data']) 
df_GetRegionalEnsino = pd.DataFrame(response_GetRegionalEnsinoPorComp.json()['data'])
df_GetUnidadeEscolarByRedeEnsino = pd.DataFrame(response_GetUnidadeEscolarByRedeEnsino.json()['data'])
df_GetUnidadeEscolarByRede = pd.DataFrame(response_GetUnidadeEscolarByRede.json()['data'])
df_GetTipo = pd.DataFrame(response_GetTipoEnsinoPorUnidadeEs.json()['data'])
df_GetSerie = pd.DataFrame(response_GetSerieByAnoLetivoEscolar.json()['data'])
df_GetTurma = pd.DataFrame(response_GetTurmaByAnoLetivoEscolar.json()['data'])
df_GetByFilter = pd.DataFrame(response_GetByFilter.json()['data'])

# SALVA OS DATAFRAMES COMO CSV
#df_cre.to_csv(f'{pasta}/cre.csv', encoding='utf-8', index=False)
#df_escola.to_csv(f'{pasta}/escola.csv', encoding='utf-8', index=False)
#df_turmas.to_csv(f'{pasta}/turmas.csv', encoding='utf-8', index=False)
#f_professores.to_csv(f'{pasta}/professores.csv', encoding='utf-8', index=False)
df_GetAll.to_csv(f'{pasta}/GetAll.csv', encoding='utf-8', index=False)
df_GetByUsuario.to_csv(f'{pasta}/GetByUsuario.csv', encoding='utf-8', index=False)
df_GetRegionalEnsino.to_csv(f'{pasta}/GetRegionalEnsino.csv', encoding='utf-8', index=False)
df_GetUnidadeEscolarByRedeEnsino.to_csv(f'{pasta}/GetUnidadeEscolarByRedeEnsino.csv', encoding='utf-8', index=False)
df_GetUnidadeEscolarByRede.to_csv(f'{pasta}/GetUnidadeEscolarByRede.csv', encoding='utf-8', index=False)
df_GetTipo.to_csv(f'{pasta}/GetTipo.csv', encoding='utf-8', index=False)
df_GetSerie.to_csv(f'{pasta}/GetSerie.csv', encoding='utf-8', index=False)
df_GetTurma.to_csv(f'{pasta}/GetTurma.csv', encoding='utf-8', index=False)
df_GetByFilter.to_csv(f'{pasta}/GetByFilter.csv', encoding='utf-8', index=False)





            
driver.quit()

