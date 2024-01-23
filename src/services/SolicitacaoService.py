# == Solicitação Service ==
import json
import re

from models import Solicitacao
from services.utils import valores_por_virgula, verificar_asterisco


class SolicitacaoService:
    @staticmethod
    def get_solicitacoes(solicitacao_filial: str,
                         solicitacao_status: str,
                         solicitacao_tipo: str,
                         solicitacao_equipamento: str,
                         data_between: str):
        # Trago todas as solicitações, sem filtro.
        # 1. Crio a Query apenas.
        todas_solicitacoes = Solicitacao.query.filter(Solicitacao.D_E_L_E_T_ != '*')
        print(f"\n{'-' * 50}\n----> Query Todas as Solicitações: <----\n{todas_solicitacoes}\n{'-' * 50}\n")

        # 2. Executo a Query.
        todas_solicitacoes = todas_solicitacoes.all()
        print(f"\n{'-' * 50}\n----> Todas as Solicitações: <----\n{todas_solicitacoes}\n{'-' * 50}\n")

        pass

    @staticmethod
    def get_all_solicitacoes(solicitacao_filial,
                             solicitacao_status,
                             solicitacao_tipo,
                             solicitacao_equipamento,
                             data_between):
        """
        List a specific description of a request for service based on the provided description ID.
        :param solicitacao_filial: Filial da Solicitação.
        :param solicitacao_status: Status da Solicitação (A - Em Análise, D - Distribuido, E - Encerrada, C - Cancelada.
        :param solicitacao_tipo: Tipo da Solicitação (C - Corretiva, P - Preventiva).
        :param solicitacao_equipamento: Equipamento da Solicitação.
        :param data_between: Data da Solicitação.

        :return: List of Requests with Description.
        """

        # ----- Criação da Query para trazer "ID da Solicitação" e "Descrição da Solicitação" -----
        # Importante: O método `Query` do SQLAlchemy não é chamado diretamente, precisa chamar sub-métodos dele.
        # Fazendo isto, evita o erro "TypeError: 'Query' object is not callable".

        query_solicitacoes = Solicitacao.query

        print("\n----> Service Solicitações: Criando os Filtros da S.S. <----")
        filters = [
            (solicitacao_filial, Solicitacao.solicitacao_filial),
            (solicitacao_status, Solicitacao.solicitacao_status),
            (solicitacao_tipo, Solicitacao.solicitacao_tipo),
            (solicitacao_equipamento, Solicitacao.solicitacao_equipamento),
            (data_between, Solicitacao.solicitacao_databer)
        ]

        print("----> Service Solicitações: Aplicando os Filtros da S.S.: <----")

        for filtro_valor, coluna_filtrada in filters:
            print(f"Filtro: {coluna_filtrada}; Valor a ser aplicado: {filtro_valor}")
            if not verificar_asterisco(filtro_valor) and filtro_valor is not None:
                if coluna_filtrada == Solicitacao.solicitacao_databer:
                    datas_separadas = valores_por_virgula(filtro_valor)
                    if datas_separadas:
                        data_inicial, data_final = datas_separadas
                        query_solicitacoes = query_solicitacoes.filter(
                            coluna_filtrada.between(data_inicial, data_final))
                else:
                    query_solicitacoes = query_solicitacoes.filter(coluna_filtrada == filtro_valor)

        print(f"----> Service Solicitações: Query Após Filtros. <----\n{query_solicitacoes}\n{'-' * 50}\n")

        # query_solicitacoes = query_solicitacoes.all()

        for solicitacao in query_solicitacoes:
            print(json.dumps(solicitacao.to_dict(), indent=4))

        print("----> End of Descriptions List <----\n")

        pass
