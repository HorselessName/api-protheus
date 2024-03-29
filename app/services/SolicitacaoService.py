# == Solicitação Service ==
import json

from models import Solicitacao
from services.Utils import valores_por_virgula, verificar_asterisco
from services.OrdemServicoService import OrdemServicoService
from typing import List, Union, Dict
from schemas import SolicitacaoSchema

SolicitacaoType = Union[Dict, SolicitacaoSchema, Solicitacao]


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
    def get_solicitacoes():
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
        print("\n----> Service Solicitações: Verificando Status das S.S. recebidas <----")
        for solicitacao in solicitacoes:
            if solicitacao['solicitacao_status'] == 'D':
                SolicitacaoService.validar_se_ss_distribuida(solicitacao)

    @staticmethod
    def validar_se_ss_distribuida(solicitacao: SolicitacaoType):
        ordens_ss_atual, query_ordens_ss_str = (OrdemServicoService
                                                .get_ordens_por_solicitacao
                                                (solicitacao['solicitacao_id'], solicitacao['solicitacao_filial']))

        if len(ordens_ss_atual) == 0:
            print("##### Não tem O.S. para a S.S.: ", solicitacao['solicitacao_id'])
            solicitacao['solicitacao_status'] = "A"
            return

        print("##### Tem O.S. na S.S.: ", solicitacao['solicitacao_id'], "; Verificando se possuem Executores...")
        if not SolicitacaoService.checar_se_ordem_tem_executores(ordens_ss_atual):
            print("##### Atualizando status da S.S. para 'A' devido à falta de executor em uma ou mais O.S.")
            solicitacao['solicitacao_status'] = "A"
            return  # Saio do método, pois a S.S. não está conforme esperado.

        print("##### Todas as O.S. possuem Executores; Verificando se a S.S. está em Serviço...")
        for ordem_ss in ordens_ss_atual:
            SolicitacaoService.ver_se_ss_em_servico(ordem_ss, solicitacao)

    @staticmethod
    def checar_se_ordem_tem_executores(ordens_ss_atual):
        for ordem in ordens_ss_atual:
            tem_executor = False
            for insumo in ordem['ordem_insumos']:
                detalhes_insumo = insumo['detalhes_insumo']
                if detalhes_insumo['insumo_tipo'] == 'M' and detalhes_insumo['executor_nome'].strip():
                    tem_executor = True
                    break  # Se encontrar um executor, não precisa verificar os outros insumos

            if not tem_executor:
                print("##### O.S. sem executor: ", ordem['ordem_id'])
                return False  # Retorna False assim que encontra uma O.S. sem executor

        return True  # Retorna True se todas as O.S. têm executor

    @staticmethod
    def ver_se_ss_em_servico(ordem_ss: dict, solicitacao: SolicitacaoType):
        """
        Verifica se a Ordem de Serviço indica que a Solicitação de Serviço está em serviço,
        atualizando o status da S.S. para "S" se aplicável.

        :param ordem_ss: A Ordem de Serviço sendo verificada.
        :param solicitacao: A Solicitação de Serviço a ser potencialmente atualizada.
        """

        if (
                ordem_ss['ordem_data_inicio_atendimento'].strip() != "" and
                ordem_ss['ordem_hora_inicio_atendimento'].strip() != "" and
                ordem_ss['ordem_data_fim_atendimento'].strip() == "" and
                ordem_ss['ordem_hora_fim_atendimento'].strip() == ""
        ):
            # Se a O.S. está aberta com uma data inicial de atendimento, então a S.S. está em "Em Serviço".
            solicitacao['solicitacao_status'] = "S"
            print("##### S.S. atualizada para Status 'S': ", solicitacao)
