# == Manutenção Service ==

from sqlalchemy.exc import OperationalError
from models import Solicitacao
from .Utils import validar_numeros, validar_caracteres, format_sql_query
from .SolicitacaoService import SolicitacaoService
from schemas import SolicitacaoSchema
from sqlalchemy import or_


class ManutencaoService:

    @staticmethod
    def buscar_solicitacoes_filial(filial: str, status: str):
        """
        Busca todas as S.S. de uma filial com base no status fornecido.

        Esse método aplica a regra de negócio RENG-01, que gera os status da S.S. de acordo com possíveis
        valores de uma O.S. aberta, para ela.

        Valores Possíveis:
        - A - Em Análise,
        - D - Distribuido, -- Neste status, é gerado uma O.S. ao distribuir.
        - TODO: S - Em Serviço (Gerar pela Regra de Negócio),
        - TODO: V - Em Validação (Gerar pela Regra de Negócio, depois da S. Fazer primeiro apenas S.),
        - E - Encerrada,
        - C - Cancelada.

        :param filial:
        :param status:
        :return:
        """
        isvalid, message = validar_numeros(filial)
        if not isvalid:
            return None, message

        try:
            status_list = status.split(',')

            print("##### Manutencao Service - S.S. Status Check: ", filial, status)

            solicitacoes = Solicitacao.query.filter(
                Solicitacao.solicitacao_filial.in_(filial.split(',') if ',' in filial else [filial]),
                Solicitacao.solicitacao_status.in_(status_list),
                Solicitacao.D_E_L_E_T_ != '*'
            )

            query_str = format_sql_query(solicitacoes)
            solicitacao_schema = SolicitacaoSchema(many=True)
            solicitacoes_json = solicitacao_schema.dump(solicitacoes.all())

            # TODO: GDM-116 - Verificar o `status` da SS e ajustar se realmente é `D` de Distribuido.
            SolicitacaoService.verificar_status_ss(solicitacoes_json)

            return query_str, solicitacoes_json, None

        except (ValueError, OperationalError) as error:
            return None, f"Error: {error}"

    @staticmethod
    def buscar_solicitacoes_abertas(filial: str, equipamento: str):
        """
        Busca as solicitações de manutenção abertas com base na filial e no equipamento fornecidos.
        Tem S.S. aberta se a "Solicitação Status" tem os seguintes valores: A, D

        :param filial: ID da filial.
        :param equipamento: ID do equipamento.
        :return: Uma lista das solicitações, mensagem de erro (se houver) e
        um booleano indicando se há solicitações abertas.
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
