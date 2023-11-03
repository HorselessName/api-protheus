# == Filial Service ==
import re

from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy import case, literal
from models import Filial, Setor, Equipamento
from schemas import FilialSchema, SetorSchema
from db_context import db_sql


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
    def buscar_setores(setor_param=None,
                       grupo_condicional=None,
                       grupo_default=None,
                       filial_condicional=None,
                       setor_filial=None,
                       setor_grupo=None):
        # Passo 4: Tratando os Testes, Condições e Segurança dos Parâmetros
        def validate_parameters(**kwargs):
            """Função que valida os parâmetros baseado em condições e regras de segurança."""
            # Evitando XSS e SQL Injection
            def is_valid_param(param):
                # Definindo um tamanho máximo para cada parâmetro
                max_length = 50
                if not re.match("^[a-zA-Z0-9]*$", param) or len(param) > max_length:
                    return False
                return True

            # Validação de cada parâmetro contra regras de segurança
            for key, value in kwargs.items():
                if value and not is_valid_param(value):
                    return {"error": f"O parâmetro '{key}' contém caracteres inválidos ou é muito longo."}

            # Validação de lógica dos parâmetros
            if not kwargs.get('grupo_default'):
                return {"error": "Um Grupo Default deve ser fornecido."}

            if kwargs.get('setor_param') and (not kwargs.get('grupo_condicional') or not kwargs.get('filial_condicional')):
                return {"error": "Se Setor for informado, o Grupo Condicional e a Filial Condicional são Obrigatórios."}

            if not kwargs.get('setor_param') and (kwargs.get('grupo_condicional') or kwargs.get('filial_condicional')):
                return {"error": "Se Grupo Condicional ou Filial Condicional forem informados, o Setor é Obrigatório."}

            return None  # se tudo estiver bem

        # Passo 4 - Continuação: Verificar / Validar todos os Parametros informados.
        error_response = validate_parameters(setor_param=setor_param,
                                             grupo_condicional=grupo_condicional,
                                             grupo_default=grupo_default,
                                             filial_condicional=filial_condicional,
                                             setor_filial=setor_filial,
                                             setor_grupo=setor_grupo)

        if error_response:
            return error_response

        sub_query_with_case = None
        results = []

        # Etapa 4 - Continuação: Tratando o fluxo quando apenas o grupo_default é fornecido
        if grupo_default and not setor_param and not grupo_condicional:
            try:
                # Se apenas o grupo_default for fornecido, busca todos os setores
                query = db_sql.session.query(
                    Setor.setor_filial.label("setor_filial"),
                    literal(grupo_default).label("setor_grupo"),
                    Setor.setor_codigo,
                    Setor.setor_nome
                )
                results = query.all()
            except SQLAlchemyError as e:
                print(f"Erro na Etapa 4 - Continuação: {e}")
                return None

        # Passo 1: Juntar os resultados das Tabelas - INNER JOIN de Setores e Equipamentos
        try:
            sub_query = db_sql.session.query(
                Equipamento.equipamento_filial.label("setor_filial"),
                Setor.setor_codigo,
                Setor.setor_nome
            ).join(
                Setor, Setor.setor_codigo == Equipamento.equipamento_setor
            ).distinct().subquery('setores_temp')
        except SQLAlchemyError as e:
            print(f"Erro no passo 1: {e}")
            return None

        try:
            # Passo 4: Testes e validações - Verificamos se todas as condições foram atendidas
            if setor_param and grupo_condicional and filial_condicional:
                # Passo 3: Aplicação da condição para definição do setor_grupo e da filial.
                conditions_grupo = [
                    (sub_query.c.setor_codigo == setor_param, grupo_condicional)
                ]

                conditions_filial = [
                    (sub_query.c.setor_codigo == setor_param, filial_condicional)
                ]

                # Passo 5: Incrementando o campo da filial junto com o que já estava sendo usado, campo grupo.
                sub_query_with_case = db_sql.session.query(
                    case(
                        *conditions_filial,
                        else_=sub_query.c.setor_filial
                    ).label("setor_filial"),
                    case(
                        *conditions_grupo,
                        else_=grupo_default
                    ).label("setor_grupo"),
                    sub_query.c.setor_codigo,
                    sub_query.c.setor_nome
                ).subquery('setores')

        except SQLAlchemyError as e:
            print(f"Erro ao buscar setores: {e}")
            return None

        try:
            # Passo 4 - Continuação: Só tento fazer a query aqui se a sub_query_with_case foi definida.
            if sub_query_with_case is not None:

                # Passo 2: Tabela Setores - Retorno do INNER JOIN de Setores e Equipamentos
                query = db_sql.session.query(
                    sub_query_with_case.c.setor_filial,
                    sub_query_with_case.c.setor_grupo,
                    sub_query_with_case.c.setor_codigo,
                    sub_query_with_case.c.setor_nome
                )

                # Condições de filtro
                filter_conditions = []

                # Passo 6: Adicionando o filtro para a filial e o grupo
                if setor_filial:  # Se setor_filial tiver um valor
                    filter_conditions.append(sub_query_with_case.c.setor_filial == setor_filial)

                if setor_grupo:  # Se setor_grupo tiver um valor
                    filter_conditions.append(sub_query_with_case.c.setor_grupo == setor_grupo)

                # Aplicando todos os filtros de uma vez
                if filter_conditions:
                    query = query.filter(*filter_conditions)

                results = query.all()
        except SQLAlchemyError as e:
            print(f"Erro nos passos 2/4/6 - Consulta na Sub Query with Case: {e}")
            return None

        try:
            # Desserialização usando Marshmallow
            schema = SetorSchema(many=True)
            output = schema.dump(results)

            if not output:
                return {"error": "Não foram encontrados dados para os parâmetros fornecidos."}

            return output
        except Exception as e:
            print(f"Erro ao desserializar: {e}")
            return None
