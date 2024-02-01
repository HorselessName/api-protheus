# DockerFile: É usado pelo Docker Compose p/ construir a imagem do container.

FROM python:3.10-slim
LABEL authors="Raul Chiarella"

##### Quick CheatSheet #####
#
# Workdir: Comandos como CMD, RUN, ENTRYPOINT, serão executados a partir deste diretório.
# Run: Geralmente usado para executar comandos na construção da imagem, como instalar pacotes.
# Entrypoint: Comando raiz do container, quando o container é iniciado, este comando é executado.
# Cmd: Fornece argumentos para o comando ENTRYPOINT, ou pode ser usado como comando raiz do container.
#
############################

# Não criar VENV para o PIPENV pois o container já é isolado, usar só como gerenciador de pacotes.
ENV PIPENV_IGNORE_VIRTUALENVS=1

# Previne a criação de arquivos .pyc no Container.
ENV PYTHONDONTWRITEBYTECODE=1

# Desligar o Buffering p/ melhorar os Logs do Container.
ENV PYTHONUNBUFFERED=1

# Copiar os arquivos Fonte p/ a pasta de Trabalho do Container.
WORKDIR /app
COPY src/ /app/

# PyODBC Dependencies + MS SQL Server ODBC Driver v17 (Ver Versão do Linux na Imagem usada.)
RUN apt update -y
RUN apt install -y gcc apt-transport-https curl gnupg
RUN apt install -y unixodbc-dev unixodbc
RUN apt clean -y

# Fix (-fsSL) para "Signatures couldn't be verified because the public key is not available".
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt update -y
RUN ACCEPT_EULA=Y apt install -y msodbcsql17 --assume-yes

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools pipenv

# Instalação de Dependencias, Sincronizar o Pipfile com o Pipfile.lock, Ignora o Pipfile e usa o Pipfile.lock.
RUN pipenv install --system --deploy --ignore-pipfile

# Cria um usuário não-root chamado 'appuser' e define a propriedade do diretório /app para esse usuário
RUN adduser --disabled-password --gecos "" --uid 10000 api_protheus
RUN chown -R api_protheus:api_protheus /app

# Muda para o usuário não-root
USER api_protheus

# Comando a Ser Executado quando o Container Inicia como Não-Root
ENTRYPOINT ["python"]
CMD ["main.py"]

# Para Testes:
# ENTRYPOINT ["tail", "-f", "/dev/null"]
