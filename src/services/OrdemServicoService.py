from models import OrdemServico
from schemas import OrdemServicoSchema
from services.utils import format_sql_query

# Todo: Verificar se o Funcionário está cadastrado na Filial.


class OrdemServicoService:
    @staticmethod
    def get_ordens_por_solicitacao(ordem_codsolicitacao: str):
        try:
            query_ordens_servico = OrdemServico.query.filter(OrdemServico.ordem_codsolicitacao == ordem_codsolicitacao)
            query_ordens_servico_str = format_sql_query(query_ordens_servico)

            print(f"\n----> Query Ordem de Serviço: <----\n{query_ordens_servico}\n{'-' * 50}\n")

            ordens_servico_schema = OrdemServicoSchema(many=True)
            ordens_servico_json = ordens_servico_schema.dump(query_ordens_servico.all())
            print("-" * 30)
            print(f"Ordens de Serviço serializadas: {ordens_servico_json}")

            return ordens_servico_json, query_ordens_servico_str

        except Exception as e:
            return {"message": f"Erro ao buscar as ordens de serviço: {e}"}, 500

    @staticmethod
    def get_todas_ordens_servico():
        """
        Retorna todas as Ordens de Serviço.
        Filtros p/ garantir que as O.S estão abertas:

        - Não esteja deletado.
        - Campos de Abertura de Hora ao abrir não devem estar 00:00.
        - O código da Solicitação não deve estar vazio.
        - A Situação da O.S. deve estar "L".
        """

        # 1. Query para trazer as O.S. com os filtros acima.
        todas_ordens_servico = OrdemServico.query.filter(
            OrdemServico.ordem_excluida == '',
            OrdemServico.ordem_hora_abertura != "00:00",
            OrdemServico.ordem_codsolicitacao != "",
            OrdemServico.ordem_situacao == "L"
        )

        # 2. Serialização das O.S. para JSON.
        todas_ordens_servico_schema = OrdemServicoSchema(many=True)
        todas_ordens_servico_json = todas_ordens_servico_schema.dump(todas_ordens_servico)

        # 3. Retorno dos dados em JSON.
        print("-" * 30)
        print("Get Todas O.s. - Ordens de Serviço Formatadas:")
        print(todas_ordens_servico_json, "\n\n", format_sql_query(todas_ordens_servico))

        return todas_ordens_servico_json, format_sql_query(todas_ordens_servico)
