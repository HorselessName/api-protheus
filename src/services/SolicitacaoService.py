# == Solicitação Service ==
import json

from models import Solicitacao


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
    def get_descriptions(loc_solicitacao_id):
        """
        List a specific description of a request for service based on the provided description ID.
        :param loc_solicitacao_id: ID of the request description to filter.
        """

        # ----- Criação da Query para trazer "ID da Solicitação" e "Descrição da Solicitação" -----
        # Importante: O método `Query` do SQLAlchemy não é chamado diretamente, precisa chamar sub-métodos dele.
        # Fazendo isto, evita o erro "TypeError: 'Query' object is not callable".

        query_solicitacoes = (Solicitacao.query
                              .filter(Solicitacao.solicitacao_id == loc_solicitacao_id)
                              .all())

        # Imprimindo os resultados
        for solicitacao in query_solicitacoes:
            print(json.dumps(solicitacao.to_dict(), indent=4))

        print("----> End of Descriptions List <----\n")
        pass
