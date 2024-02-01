# API Protheus

Essa API para o Protheus é uma interface de consulta para o sistema TOTVS Protheus. 
Ela foi desenvolvida para proporcionar um acesso simplificado a dados não disponíveis nas APIs REST 
padrão da TOTVS. Ela API é de "somente leitura" e foca apenas em operações GET.

A API foi desenvolvida seguindo padrões de orientação a objeto, para facilitar a manutenção e
fornecer a abstração de dados. Ela utiliza o SQLAlchemy para mapear as entidades e o Marshmallow do Flask para
serializar os dados.

# Instalação Automática 

Com Docker Composer e DockerFile.

## Pré-Requisitos:
- Docker Instalado.
- Docker Composer Instalado.
- Arquivo .env do Docker Composer configurado com as variáveis de configuração.
  - VOLUME_PATH_APP: Pasta da Aplicação. Não use aspas no Linux. Ex: Use `/mnt/dados/db`
  - API_PORT: Porta da API.
  - API_HOST: Endereço que a API vai rodar.
- Pastas com Permissões e Usuários Configuradas p/ o Docker não ter problemas de permissões.
- Volumes que irão mapear os dados pelo `.env` devem estar criados e com permissões p/ o Docker.
- Fazer o `git clone` do projeto dentro do volume do `docker`, usando o nome `api_protheus`. Ex: Se seu volume fica em `/mnt/dados/projetos`, você deve clonar fazendo `git clone <url> /mnt/dados/projetos/api_protheus`.

## Comando para Instalar

Após cumprir os Pré-Requisitos, dentro do projeto que contém o Dockerfile, entre dentro dele e execute `docker-compose up -d`.

# Instalação Manual

## Dependencies / Installation
Atualizar o PIP, primeiramente: `python -m pip install --upgrade pip`.

## Instaladas Globalmente
- Instalar o Virtual Env: `pip install --upgrade virtualenv`
- Instalar o SetupTools: `pip install --upgrade setuptools`
- Gerenciador de pacotes: `pip install pipenv`

- Instalar o VENV com o PIPENV:
  - Configurar para fazer o VENV Local.
    - Linux: `export PIPENV_VENV_IN_PROJECT=1`
    - Windows - CMD: `set PIPENV_VENV_IN_PROJECT=1`
    - Windows - PowerShell: `$env:PIPENV_VENV_IN_PROJECT=1`
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
- Para o Driver do SQL funcinar, instale o UnixODBC: `apt install -y unixodbc`
- Python DOT Env para variaveis de ambiente: `pipenv install python-dotenv`
- Flask CORS para permitir acesso externo: `pipenv install flask-cors`

Após instalar os pacotes, você precisa configurar o seu arquivo .env com suas informações de acessos do seu Banco de Dados SQL Server.
- Rodar o Aplicativo: `pipenv run python main.py`

Arquivo de config do app, `.env` dentro de `src`:
```
# Conexões SQL Server
SQL_SERVER_HOST="IP do Servidor"
SQL_SERVER_DATABASE="Banco de Dados SQL"
SQL_SERVER_USER="Usuário do Banco"
SQL_SERVER_PASSWORD="Senha de Acesso"
```

PS - Se quiser remover tudo e tentar novamente: `docker container rm api_protheus -f ; docker volume rm apisimplify_vol_api_protheus apisimplify_vol_api_logs api-protheus_vol_api_logs api-protheus_vol_api_protheus ; docker volume prune -f ; docker rmi teste apisimplify-api-protheus api-protheus_api-protheus`

# Entitades

Entidades mapeadas para utilizar a API do Protheus.
API é Somente Leitura e feita para ser GET apenas.

- Equipamento (Bem)

## Referencias

[API reference TOTVS](https://api.totvs.com.br/)
[Layout da Tabela de Bens](https://shorturl.at/tvF19)

# Próximos Passos

- Automatizar Instalação e Deploy da API com Docker
