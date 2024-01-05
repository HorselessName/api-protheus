# API Protheus

Essa API para o Protheus é uma interface de consulta para o sistema TOTVS Protheus. 
Ela foi desenvolvida para proporcionar um acesso simplificado a dados não disponíveis nas APIs REST 
padrão da TOTVS. Ela API é de "somente leitura" e foca apenas em operações GET.

A API foi desenvolvida seguindo padrões de orientação a objeto, para facilitar a manutenção e
fornecer a abstração de dados. Ela utiliza o SQLAlchemy para mapear as entidades e o Marshmallow do Flask para
serializar os dados.

# Dependencies / Installation
Atualizar o PIP, primeiramente: `python -m pip install --upgrade pip`.
No Linux, você precisa fazer o PipEnv criar o VENV no Projeto: `export PIPENV_VENV_IN_PROJECT=1`

## Instaladas Globalmente
- Instalar o Virtual Env: `pip install --upgrade virtualenv`
- Instalar o SetupTools: `pip install --upgrade setuptools`
- Gerenciador de pacotes: `pip install pipenv`
- Instalar o VENV com o PIPENV: `pipenv install`

## Instalada no Virtual Environment
Instalar utilizando o pipenv, para melhor gerenciamento das dependencias.
Executar de fora do venv, dentro da pasta do projeto via terminal.

Se todas estiverem instaladas, e seu Pipfile.lock estiver configurado, você roda só `pipenv install`

- SQLAlchemy: `pipenv install SQLAlchemy`
- Flask: `pipenv install Flask`
- Mashmallow: `pipenv install marshmallow`
- Flask SQLAlchemy: `pipenv install Flask-SQLAlchemy`
- Marshmallow SQLAlchemy: `pipenv install marshmallow-sqlalchemy`
- Flask Marshmallow: `pipenv install flask-marshmallow`
- Flasgger for Swagger: `pipenv install flasgger`
- PyODBC Driver do SQL Server: `pipenv install pyodbc`
- Python DOT Env para variaveis de ambiente: `pipenv install python-dotenv`
- Flask CORS para permitir acesso externo: `pipenv install flask-cors`

Após instalar os pacotes, você precisa configurar o seu arquivo .env com suas informações de acessos do seu Banco de Dados SQL Server.
- Rodar o Aplicativo: `pipenv run python main.py`

Exemplo de arquivo de config, `.env`:
```
# Conexões SQL Server
SQL_SERVER_HOST="IP do Servidor"
SQL_SERVER_DATABASE="Banco de Dados SQL"
SQL_SERVER_USER="Usuário do Banco"
SQL_SERVER_PASSWORD="Senha de Acesso"
```

# Entitades

Entidades mapeadas para utilizar a API do Protheus.
API é Somente Leitura e feita para ser GET apenas.

- Equipamento (Bem)

## Referencias

[API reference TOTVS](https://api.totvs.com.br/)
[Layout da Tabela de Bens](https://shorturl.at/tvF19)

# Próximos Passos

- Automatizar Instalação e Deploy da API com Docker
