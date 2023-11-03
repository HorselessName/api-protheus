# == Manutenção Service ==

from sqlalchemy.exc import OperationalError
from models import Solicitacao
from .utils import validar_filial, validar_equipamento
from schemas import SolicitacaoSchema


class ManutencaoService:

    @staticmethod
    def buscar_solicitacoes_abertas(filial: str, equipamento: str):
        """
        Busca as solicitações de manutenção abertas com base na filial e no equipamento fornecidos.

        Exemplo do SQL gerado:
        SELECT * FROM SOLICITACOES WHERE
            solicitacao_filial = 'XXXX' AND
            solicitacao_equipamento = 'YYYY' AND
            solicitacao_status = 'A' AND
            D_E_L_E_T_ <> '*';

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
            solicitacoes = Solicitacao.query.filter(
                Solicitacao.solicitacao_filial == filial,
                Solicitacao.solicitacao_equipamento == equipamento,
                Solicitacao.solicitacao_status == 'A',
                Solicitacao.D_E_L_E_T_ != '*'
            ).all()

            if not solicitacoes:
                return [], "Não existe nenhuma solicitação aberta para a filial e equipamento fornecidos.", False

            print(f"----- Solicitações: Passo 1 -----\n"
                  f"Usando o Marshmallow para converter as solicitações para JSON...\n"
                  f"Solicitações brutos: {solicitacoes}")

            try:
                solicitacao_schema = SolicitacaoSchema(many=True)
                solicitacoes_json = solicitacao_schema.dump(solicitacoes)
                print("-" * 30)
                print(f"Solicitações serializadas: {solicitacoes_json}")

            except ValueError as ve:
                print(f"Erro ao serializar as solicitações: {ve}")
                return None, f"Erro ao serializar as solicitações: {ve}", False

            possui_ss_aberta = len(solicitacoes) > 0
            return solicitacoes_json, None, possui_ss_aberta

        except OperationalError as e:
            return None, str(e), False
