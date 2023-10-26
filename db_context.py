# Imports relacionados ao banco de dados e configurações
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
import urllib.parse
from dotenv import dotenv_values
from sqlalchemy.exc import OperationalError, InvalidRequestError

config = dotenv_values(".env")

# Configuracoes do SQL Server - Timeout aqui é para tentativa de conexão inicial.
config_mssql = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=" + config['SQL_SERVER_HOST'] + ";"
    "DATABASE=" + config['SQL_SERVER_DATABASE'] + ";"
    "UID=" + config['SQL_SERVER_USER'] + ";"
    "PWD=" + config['SQL_SERVER_PASSWORD'] + ";"
    "timeout=3;")

DATABASE_URI = 'mssql+pyodbc:///?odbc_connect={}'.format(config_mssql)


# Base para as models seguirem o padrão do SQLAlchemy, usando suas naming conventions.
class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })


# Definir objeto para servir o SQLAlchemy no app - Timeout aqui é o tempo para uma operação específica.
db_sql = SQLAlchemy(
    model_class=Base,
    engine_options={
        "connect_args": {"use_setinputsizes": False, "timeout": 3},
    }
)


def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    try:
        # Tratar erros de conexão com o banco de dados.
        db_sql.init_app(app)
    except OperationalError as e:
        app.logger.error("Erro ao inicializar a conexão com o banco de dados: %s", e)
        raise
    except InvalidRequestError as e:
        app.logger.error("Erro ao fazer a requisição ao banco de dados: %s", e)
        raise
    except Exception as e:
        app.logger.error("Erro desconhecido ao inicializar a conexão com o banco de dados: %s", e)
        raise
