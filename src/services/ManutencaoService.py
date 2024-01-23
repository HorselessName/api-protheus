# == Manutenção Service ==

from sqlalchemy.exc import OperationalError
from models import Solicitacao
from .utils import validar_numeros, validar_caracteres, format_sql_query
from schemas import SolicitacaoSchema
from sqlalchemy import or_


class ManutencaoService:

    @staticmethod
    def buscar_solicitacoes_filial(filial: str, status: str):
        """
        Busca todas as S.S. de uma filial com base no status fornecido.

        :param filial:
        :param status:
        :return:
        """
        isvalid, message = validar_numeros(filial)
        if not isvalid:
            return None, message

        try:
            # Valores esperados: "A,D" (Ou outros adicionais, status de S.S.)
            status_list = status.split(',')
            solicitacoes = Solicitacao.query.filter(
                Solicitacao.solicitacao_filial == filial,

                # Método `In` do SQLAlchemy p/ trazer se valor da coluna está na lista.
                Solicitacao.solicitacao_status.in_(status_list),
                Solicitacao.D_E_L_E_T_ != '*'

            )

            query_str = format_sql_query(solicitacoes)
            print(f"\n{'-' * 50}\n----> Query SQL Executada: <----\n{query_str}\n{'-' * 50}\n")

            try:
                solicitacao_schema = SolicitacaoSchema(many=True)
                solicitacoes_json = solicitacao_schema.dump(solicitacoes.all())
                print("-" * 30)
                print(f"Solicitações da Filial serializadas: {solicitacoes_json}")

                # Precisa retornar o mesmo tanto de argumentos que a `route` espera,
                # senão gera o erro Not Enough Values to Unpack
                return query_str, solicitacoes_json, None

            except ValueError as erro_serializacao:
                print(f"Erro ao serializar as solicitações: {erro_serializacao}")
                return None, f"Erro ao serializar as solicitações: {erro_serializacao}"

        except OperationalError as erro_query:
            return None, None, False, str(erro_query)

    @staticmethod
    def buscar_solicitacoes_abertas(filial: str, equipamento: str):
        """
        Busca as solicitações de manutenção abertas com base na filial e no equipamento fornecidos.
        Tem S.S. aberta se a "Solicitação Status" tem os seguintes valores: A, D

        :param filial: ID da filial.
        :param equipamento: ID do equipamento.
        :return: Uma lista das solicitações, mensagem de erro (se houver) e um booleano indicando se há solicitações abertas.
        """
        is_valid, message = validar_numeros(filial)
        if not is_valid:
            return None, message, None

        is_valid, message = validar_caracteres(equipamento)
        if not is_valid:
            return None, message, None

        try:
            print("Fazendo o SELECT com os valores: ", filial, equipamento)
            solicitacoes = Solicitacao.query.filter(
                Solicitacao.solicitacao_filial == filial,
                Solicitacao.solicitacao_equipamento == equipamento,
                or_(
                    Solicitacao.solicitacao_status == 'A',
                    Solicitacao.solicitacao_status == 'D'
                ),
                Solicitacao.D_E_L_E_T_ != '*'
            )

            # Lógica da Query e Dados separados para montar o SQL no JSON.
            solicitacoes_dados = solicitacoes.all()
            possui_ss_aberta = len(solicitacoes_dados) > 0

            # Query SQL: Solicitacoes do Equipamento.
            query_str = format_sql_query(solicitacoes)
            print(f"\n{'-' * 50}\n----> Query SQL Executada: <----\n{query_str}\n{'-' * 50}\n")

            if not possui_ss_aberta:
                # Retorna a string SQL mesmo quando não há solicitações abertas
                return query_str, [], False, None

            try:
                solicitacao_schema = SolicitacaoSchema(many=True)
                solicitacoes_json = solicitacao_schema.dump(solicitacoes_dados)
                print("-" * 30)
                print(f"Solicitações serializadas: {solicitacoes_json}")

                return query_str, solicitacoes_json, possui_ss_aberta, None

            except ValueError as ve:
                print(f"Erro ao serializar as solicitações: {ve}")
                return None, None, False, f"Erro ao serializar as solicitações: {ve}"

        except OperationalError as e:
            return None, None, False, str(e)
