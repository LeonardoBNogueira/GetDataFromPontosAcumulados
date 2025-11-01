from cfg_data import credenciais
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# URLs para acessar a tela de login
URL_LOGIN = "https://educadf.se.df.gov.br/auth/login?id=2"
# URL_REGISTROS = "https://educadf.se.df.gov.br/diario_classe/modulos/calendario"

# RECUPERA OS VALORES DE LOGIN E SENHA DO OBJETO Credenciais
USERNAME = credenciais['login']
PASSWORD = credenciais['pass']

# ABRE O CHROME, DEFINE QUE ELE FICARÁ OCULTO, CARREGA A TELA DE LOGIN
options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")  # oculta o navegador
driver = webdriver.Chrome(options=options)
driver.get(URL_LOGIN)

# LOCALIZA OS CAMPOS INPUT A PARTIR DO ID NO DOCUMENTO HTML
usuario = driver.find_element(By.ID, 'username')
senha = driver.find_element(By.ID, 'password-input')

# PREENCHE OS CAMPOS DE USUÁRIO, SENHA, APERTA ENTER E AGUARDA 5S PARA A TELA CARREGAR
usuario.send_keys(USERNAME)
senha.send_keys(PASSWORD)
senha.send_keys(Keys.RETURN)
time.sleep(5)
# driver.get(URL_REGISTROS)
# time.sleep(5)


# RECUPERA O NOME DE TODOS OS OBJETOS SALVOS NO SessionStorage QUE FICA NO NAVEGADOR. LÁ ESTARÁ TAMBÉM O ACCESS_TOKEN
sessao_data = {}
sessionKeys = driver.execute_script("""
    var keys = [];
    for (var i = 0; i < window.sessionStorage.length; i++) {
        keys.push(window.sessionStorage.key(i));
    }
    return keys;
""")

# A PARTIR DOS NOMES DOS OBJETOS QUE ESTÃO NA sessionStorage, ACESSA CADA UM DELES E SALVA EM sessao_data no formato
# chave: valor
for key in sessionKeys:
    sessao_data[key] = driver.execute_script(f'return window.sessionStorage.getItem("{key}")')

