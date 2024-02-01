# Importar Models para as queries do Flask-SQLAlchemy
from models import Filial
from models.Equipamento import Equipamento
from models.Setor import Setor

# Importar o Controller do DB, o SQLAlchemy do Flask.
from db_context import db_sql

# Importar nossos Schemas para o Marshmallow conseguir serializar os dados.
from schemas import SetorSchema, FilialSchema

# Importar classes do SQLAlchemy para construirmos as lógicas condicionais.
from sqlalchemy import case
from sqlalchemy.exc import OperationalError

# Importar o Aliased do SQLAlchemy para construirmos as lógicas condicionais.
from sqlalchemy.orm import aliased

# Importar modulos de validacao
from services.utils import *


class SetorLogic:

    @staticmethod
    def inner_join_setores(setor_informado="Setor Informado",
                           filial_condicional="Filial Condicional"):
        # Correção de Bug: Strings sendo inicializadas como None...
        # Por causa disso, o CASE do SQLAlchemy cria os `Thens` com NULL, e não com as strings.
        if not filial_condicional:
            filial_condicional = "Filial Condicional"
        if not setor_informado:
            setor_informado = "Setor Informado"

        # Criando aliases para as tabelas com os nomes específicos
        equipamentos = aliased(Equipamento, name='EQUIPAMENTOS')
        setores = aliased(Setor, name='SETORES')

        # Definindo a lógica do CASE para a coluna 'setor_filial'
        setor_filial = case(
            (equipamentos.equipamento_setor == setor_informado, filial_condicional),
            else_=equipamentos.equipamento_filial
        ).label('setor_filial')

        # Montando a consulta com a coluna 'setor_filial' utilizando o CASE
        query = db_sql.session.query(
            setor_filial,
            setores.setor_codigo.label('setor_codigo'),
            setores.setor_nome.label('setor_nome')
        ).join(
            setores,
            setores.setor_codigo == equipamentos.equipamento_setor
        ).distinct()

        # Retorna a consulta construída, o objeto setor_filial, e os alias 'equipamentos', 'setores'
        return query, setor_filial, equipamentos

    @staticmethod
    def adicionar_grupo(query, equipamentos,
                        setor_informado="Setor Informado",
                        grupo_condicional='Grupo Condicional',
                        grupo_padrao='Grupo Padrao'):
        # Correção de Bug: Strings sendo inicializadas como None...
        # Por causa disso, o CASE do SQLAlchemy cria os `Thens` com NULL, e não com as strings.
        if not setor_informado:
            setor_informado = "Setor Informado"
        if not grupo_condicional:
            grupo_condicional = "Grupo Condicional"
        if not grupo_padrao:
            grupo_padrao = "Grupo Padrao"

        # Utilizando o alias 'equipamentos' para a coluna 'equipamento_setor'
        setor_grupo = case(
            (equipamentos.equipamento_setor == setor_informado, grupo_condicional),
            else_=grupo_padrao  # Substitua NULL por um valor padrão não nulo.
        ).label('setor_grupo')

        # Acrescentando a seleção do grupo à consulta
        query = query.add_columns(setor_grupo)

        return query, setor_grupo

    @staticmethod
    def listar_setores(setor_recebido='Setor Informado',
                       filial_condicional='Filial Condicional',
                       grupo_condicional='Grupo Condicional',
                       grupo_padrao='Grupo Padrao',
                       setor_filial_filtro='Filial Padrão',
                       setor_grupo_filtro='Grupo Padrão'):

        print("Setor Informado no Listar Setores: ", setor_recebido)

        query, setor_filial, equipamentos = SetorLogic.inner_join_setores(setor_recebido,
                                                                          filial_condicional)

        query, setor_grupo = SetorLogic.adicionar_grupo(query,
                                                        equipamentos,
                                                        setor_recebido,
                                                        grupo_condicional,
                                                        grupo_padrao)

        # Executa a consulta e coleta os dados
        subquery = query.subquery("TABELA_SETORES")
        consultar_setores = db_sql.session.query(subquery)

        print(f"Subquery e Setores Consultados: \n\nSQL #### {subquery} \n\nSetores #### {consultar_setores}\n\n")

        # Aplicar filtros conjuntamente, usando a cláusula AND
        consulta_externa = consultar_setores.filter(
            (subquery.c.setor_filial == setor_filial_filtro) &
            (subquery.c.setor_grupo == setor_grupo_filtro)
        )

        # Inicializando o esquema Marshmallow com many=True para serializar uma lista de objetos
        setor_schema = SetorSchema(many=True)
        dados_json = setor_schema.dump(
            consulta_externa.all())  # Use .all() para executar a consulta e retornar os resultados

        # Query SQL: Trás os Setores (Famílias).
        query_str = str(consulta_externa.statement.compile(compile_kwargs={"literal_binds": True}))

        # Retornar a query e os dados em um JSON
        return {
            'sql': query_str,
            'dados': dados_json
        }


class FilialService:

    @staticmethod
    def buscar_todas_filiais():
        try:
            filiais = Filial.query.filter(Filial.D_E_L_E_T_ != '*').all()

            if not filiais:
                return None, "Nenhuma filial encontrada."

            # Desserialização com Marshmallow
            filial_schema = FilialSchema(many=True)
            filiais_json = filial_schema.dump(filiais)

            return filiais_json, None

        except OperationalError as e:
            return None, str(e)
