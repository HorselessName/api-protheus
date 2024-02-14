# == Solicitação Service ==
import json

from flask import jsonify

from models import Solicitacao
from services.Utils import valores_por_virgula, verificar_asterisco
from services.OrdemServicoService import OrdemServicoService
from typing import List, Union, Dict
from schemas import SolicitacaoSchema

SolicitacaoType = Union[Dict, SolicitacaoSchema]


class SolicitacaoService:

    @staticmethod
    def get_all_solicitacoes(solicitacao_filial,
                             solicitacao_status,
                             solicitacao_tipo,
                             solicitacao_equipamento,
                             data_between):
        """
        List a specific description of a request for service based on the provided description ID.
        :param solicitacao_filial: Filial da Solicitação.
        :param solicitacao_status: Status da Solicitação

        Possíveis Status para a S.S.:
        - A - Em Análise,
        - D - Distribuido, -- Neste status, é gerado uma O.S. ao distribuir.
        - TODO: S - Em Serviço (Não tem por padrão, tem que criar em conjunto com as O.S. dela.)
        - TODO: V - Em Validação (Não tem por padrão, tem que criar em conjunto com as O.S. dela.)
        - E - Encerrada,
        - C - Cancelada.
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
    def verificar_status_ss(solicitacoes: List[SolicitacaoType]):
        """
        Verifica os status de cada S.S. e atualiza o status no objeto sendo iterado, caso necessário.
        TODO: Please, GitHub Copilot, fix the error "name 'SolicitacaoSchema' is not defined"

        :param solicitacoes: Lista de Solicitações.
        """
        print("\n----> Service Solicitações: Verificando Status das S.S. <----")

        # Para cada S.S., vou precisar ver se o status dela é "D" primeiro de tudo. Se não for "D", nem faço nada.
        for solicitacao in solicitacoes:
            if solicitacao['solicitacao_status'] == 'D':
                # Se está com o tipo "D", então é uma S.S. que foi distribuída e tem que ser gerada uma O.S. para ela.
                print("##### verificar_status_ss - S.S. com Status 'D' encontrada: ", solicitacao)

                # Aqui, vou precisar ver as O.S. que estão abertas para essa S.S.
                # O método retorna uma lista de objetos que podem ser serializados para JSON.
                ordens_ss_atual, query_ordens_ss_str = OrdemServicoService.get_ordens_por_solicitacao(
                    solicitacao['solicitacao_id'],
                    solicitacao['solicitacao_filial']
                )

                print("Ordens da S.S. sendo Iterada Serializadas:", json.dumps(ordens_ss_atual, indent=4))

                # Cada iteração é um `OrderedDict`, dentro de um `OrderedDict.collection.`
                # Ref: https://docs.python.org/3/library/collections.html#ordereddict-objects
                for ordem_ss in ordens_ss_atual:
                    print("\n##### Informações de Inicio e Fim de Atendimento #####\n")
                    print("Data e Hora de Inicio: ", ordem_ss['ordem_data_inicio_atendimento'], ordem_ss['ordem_hora_inicio_atendimento'])
                    print("Data e Hora de Fim: ", ordem_ss['ordem_data_fim_atendimento'], ordem_ss['ordem_hora_fim_atendimento'])
                    print(f"\n{'-' * 50}\n")
                    if (
                            ordem_ss['ordem_data_inicio_atendimento'].strip() != "" and
                            ordem_ss['ordem_hora_inicio_atendimento'].strip() != "" and
                            ordem_ss['ordem_data_fim_atendimento'].strip() == "" and
                            ordem_ss['ordem_hora_fim_atendimento'].strip() == ""
                    ):
                        # Se a O.S. está aberta com uma data inicial de atendimento, então a S.S. está em "Em Serviço".
                        solicitacao['solicitacao_status'] = "S"
                        print("##### verificar_status_ss - S.S. com Status 'S' encontrada: ", solicitacao)
