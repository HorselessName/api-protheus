# == Manutenção Service ==

from sqlalchemy.exc import OperationalError
from models import Solicitacao
from .utils import validar_filial, validar_equipamento
from schemas import SolicitacaoSchema
from sqlalchemy import or_


class ManutencaoService:

    @staticmethod
    def buscar_solicitacoes_abertas(filial: str, equipamento: str):
        """
        Busca as solicitações de manutenção abertas com base na filial e no equipamento fornecidos.
        Tem S.S. aberta se a "Solicitação Status" tem os seguintes valores: A, D

        :param filial: ID da filial.
        :param equipamento: ID do equipamento.
        :return: Uma lista das solicitações, mensagem de erro (se houver) e um booleano indicando se há solicitações abertas.
        """
        is_valid, message = validar_filial(filial)
        if not is_valid:
            return None, message, None

        is_valid, message = validar_equipamento(equipamento)
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
            ).all()

            print("Solicitações encontradas: ", solicitacoes)

            possui_ss_aberta = len(solicitacoes) > 0

            if not possui_ss_aberta:
                return [], None, possui_ss_aberta

            print(f"----- Solicitações: Passo 1 -----\n"
                  f"Usando o Marshmallow para converter as solicitações para JSON...\n"
                  f"Solicitações brutos: {solicitacoes}")

            try:
                solicitacao_schema = SolicitacaoSchema(many=True)
                solicitacoes_json = solicitacao_schema.dump(solicitacoes)
                print("-" * 30)
                print(f"Solicitações serializadas: {solicitacoes_json}")

                return solicitacoes_json, None, possui_ss_aberta

            except ValueError as ve:
                print(f"Erro ao serializar as solicitações: {ve}")
                return None, f"Erro ao serializar as solicitações: {ve}", False

        except OperationalError as e:
            return None, str(e), False
