# Importar Models para as queries do Flask-SQLAlchemy
from models import Filial
from models.Equipamento import Equipamento
from models.Setor import Setor

# Importar o Controller do DB, o SQLAlchemy do Flask.
from db_context import db_sql

# Importar nossos Schemas para o Marshmallow conseguir serializar os dados.
from schemas import SetorSchema, FilialSchema

# Importar classes do SQLAlchemy para construirmos as lógicas condicionais.
from sqlalchemy import case, literal_column
from sqlalchemy.exc import SQLAlchemyError, OperationalError

# Importar modulos de validacao
from services.utils import *


class SetorLogic:

    @staticmethod
    def junta_tabelas_setores_equipamentos():
        """
        Passo 1: Junta as tabelas de Setores e Equipamentos.
        Retorna a Sub Query que pode ser usada em outros métodos,
        inclusive podendo adicionar mais métodos do SQLAlchemy dentro da Sub Query.

        :return: Sub Query com as tabelas de Setores e Equipamentos.
        """
        # Iniciar consulta para juntar tabelas de Equipamentos e Setores
        equipamentos_setores = db_sql.session.query(
            # SELECT n FROM <Table>
            Equipamento.equipamento_filial.label('setor_filial'),
            Setor.setor_codigo.label('setor_codigo'),
            Setor.setor_nome.label('setor_nome'),
        ).join(
            # JOIN <Table> ON <Table>.<Column> = <Table>.<Column>
            Setor, Setor.setor_codigo == Equipamento.equipamento_setor
        ).distinct(
            # SELECT DISTINCT <Column>
        )

        return equipamentos_setores

    @staticmethod
    def setores_equipamentos_com_grupo(setor_codigo_opcional=None, grupo_condicional=None, grupo_padrao=None):
        """ Passo 3: Adicionar a coluna de Grupo de forma condicional e retornar a query montada. """

        # Objeto base para os filtros e métodos do SQLAlchemy.
        query_base = SetorLogic.junta_tabelas_setores_equipamentos()

        # Verifica se devemos adicionar a lógica condicional.
        if setor_codigo_opcional and grupo_condicional and grupo_padrao is not None:
            # Adiciona coluna com lógica condicional CASE WHEN.
            query_setores_com_grupo = query_base.add_columns(
                case(
                    (Equipamento.equipamento_setor == setor_codigo_opcional, grupo_condicional),
                    else_=grupo_padrao
                ).label('setor_grupo')
            )
        elif grupo_padrao is not None:
            # Adiciona coluna com valor padrão.
            query_setores_com_grupo = query_base.add_columns(
                literal_column(f"'{grupo_padrao}'").label('setor_grupo')
            )
        else:
            # Se não houver grupo padrão definido e a condição não for aplicável,
            # apenas continua sem a coluna 'setor_grupo'
            query_setores_com_grupo = query_base

        return query_setores_com_grupo

    @staticmethod
    def setores_ajustar_filial(setor_codigo_opcional=None,
                               grupo_condicional=None,
                               filial_condicional=None,
                               grupo_padrao=None,
                               filial_padrao=None):
        """Passo 4: Alterar a coluna de Filial de forma condicional e retornar a query montada."""

        # Primeiro, obtemos a query com o grupo já aplicado
        query_com_grupo = SetorLogic.setores_equipamentos_com_grupo(
            setor_codigo_opcional, grupo_condicional, grupo_padrao)

        # Verifica se devemos adicionar a lógica condicional para a coluna de Filial.
        if setor_codigo_opcional and filial_condicional:
            # Adiciona coluna com lógica condicional CASE WHEN.
            # noinspection PyTypeChecker
            query_com_filial = query_com_grupo.add_columns(
                case(
                    (Equipamento.equipamento_setor == setor_codigo_opcional, filial_condicional),
                    else_=filial_padrao
                ).label('setor_filial')
            )
        else:
            # Adiciona coluna com valor padrão.
            query_com_filial = query_com_grupo.add_columns(
                literal_column(f"'{filial_padrao}'").label('setor_filial')
            )

        # Retorna a query com as modificações aplicadas
        return query_com_filial


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

    @staticmethod
    def executar_e_serializar_query(setor_codigo_opcional=None,
                                    grupo_condicional=None,
                                    filial_condicional=None,
                                    grupo_padrao=None,
                                    filial_padrao=None):
        """ Executa a query e serializa os dados para JSON. """

        # Verifica se Grupo Padrão e Filial Padrão foram fornecidos
        if not grupo_padrao or not filial_padrao:
            return {"Erro": "Grupo Padrão e Filial Padrão são obrigatórios."}

        # Valida Grupo Padrão e Filial Padrão
        grupo_valido, msg_grupo = validar_grupo(grupo_padrao)
        filial_valida, msg_filial = validar_filial(filial_padrao)
        if not grupo_valido:
            return {"Erro": msg_grupo}
        if not filial_valida:
            return {"Erro": msg_filial}

        # Valida Setor Código, se fornecido
        if setor_codigo_opcional:
            # Verifica se os parâmetros condicionais acompanham o Setor Código
            if not grupo_condicional or not filial_condicional:
                return {"Erro": "Grupo e Filial Condicional são obrigatórios quando Setor Código é fornecido."}

            # Valida o Setor Código
            setor_valido, msg = validar_setor(setor_codigo_opcional)
            if not setor_valido:
                return {"Erro": msg}

        # Ignora Grupo e Filial Condicional se Setor Código não é fornecido
        if not setor_codigo_opcional and (grupo_condicional or filial_condicional):
            grupo_condicional = None
            filial_condicional = None

        # Tente executar a query com os parâmetros validados
        try:
            # Constrói a query com os parâmetros fornecidos
            query_setores_com_grupo = SetorLogic.setores_ajustar_filial(
                setor_codigo_opcional, grupo_condicional, filial_condicional, grupo_padrao, filial_padrao
            )

            # Executa a Query e armazena os dados
            dados_setores_equipamentos = query_setores_com_grupo.all()

            # Serializa os resultados para JSON
            setor_schema = SetorSchema(many=True)
            dados_setores_equipamentos_json = setor_schema.dump(dados_setores_equipamentos)

            # Captura o comando SQL executado
            comando_sql = str(query_setores_com_grupo.statement.compile(compile_kwargs={"literal_binds": True}))

            # Retorna um objeto com os detalhes da operação
            return {
                "Passo": "Teste -- Executar e serializar a query",
                "Detalhes": {
                    "Comando SQL": comando_sql,
                    "Dados": dados_setores_equipamentos_json
                }
            }
        except SQLAlchemyError as e:
            # Em caso de erro na execução da query, retorna a descrição do erro
            return {"Erro": str(e)}
