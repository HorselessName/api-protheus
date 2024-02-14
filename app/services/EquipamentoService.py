# == Equipamento Service ==

from sqlalchemy.exc import OperationalError
from sqlalchemy import or_, func, case, and_
from models import Equipamento, Solicitacao
from .Utils import validar_numeros, validar_caracteres
from schemas import EquipamentoSchema

# TODO: Organizar por Ordem Alfabética.
# TODO: Filtro de Pesquisa.


class EquipamentoService:

    @staticmethod
    def fetch_equipamentos(filial_id=None, setor_id=None):
        print(f"\n----> Trazendo os Equipamentos da Filial {filial_id} e Setor {setor_id} <----\n")
        is_valid_filial, message_filial = validar_numeros(filial_id)
        if not is_valid_filial:
            return None, {"error": f"Erro na filial: {message_filial}"}

        is_valid_setor, message_setor = validar_caracteres(setor_id)
        if not is_valid_setor:
            return None, {"error": f"Erro no setor: {message_setor}"}

        try:
            query = Equipamento.query.filter(Equipamento.D_E_L_E_T_ != '*').filter(Equipamento.T9_STATUS == '01')
            print("\n----> Montando a Query para os Filtros de Filial e Setor <----")

            if filial_id:
                print(f"----> Aplicando o Filtro por Filial: {filial_id} <----")
                query = query.filter(Equipamento.equipamento_filial == filial_id)

            if setor_id:
                print(f"----> Aplicando o Filtro por Setor: {setor_id} <----\n")
                query = query.filter(Equipamento.equipamento_setor == setor_id)

            print(f"{'-' * 100}\nFinalizando a Montagem da Query SQL: \n{query}\n{'-' * 100}\n")
            equipamentos = query.order_by(Equipamento.equipamento_id).all()

            if not equipamentos:
                return None, {"error": "Não existe nenhum equipamento para o setor ou filial fornecida."}

            equipamento_schema = EquipamentoSchema(many=True)
            equipamentos_json = equipamento_schema.dump(equipamentos, many=True)

            print(f"\n---->Primeiro Item da lista de Equipamentos Encontrados: {equipamentos_json[0]}\n")

            # Query SQL: Trás os Equipamentos.
            query_str = str(query.statement.compile(compile_kwargs={"literal_binds": True}))
            print(f"\n{'-' * 50}\n----> Query Final que foi executada: <----\n{query_str}\n{'-' * 50}\n")

            response_data = {
                "sql": query_str,
                "equipamentos": equipamentos_json
            }

            return response_data, None

        except OperationalError as e:
            return None, {"error": str(e)}

    @staticmethod
    def fetch_equipamentos_e_ss(filial_id=None, setor_id=None):
        print("----> Verificando se os Equipamentos tem SS, para visualização dinâmica <----\n")
        is_valid_filial, message_filial = validar_numeros(filial_id)
        if not is_valid_filial:
            return None, {"error": f"Erro na filial: {message_filial}"}

        print(f"----> Filial Válida: {filial_id}; Validando os Caracteres... <----\n")
        is_valid_setor, message_setor = validar_caracteres(setor_id, "setor_id")
        if not is_valid_setor:
            return None, {"error": f"Erro no setor: {message_setor}"}

        try:
            # Montando a Query com Outer Join para já informar se tem uma S.S. aberta ou não para o equipamento,
            # e qual a prioridade da S.S. se houver.
            query = (Equipamento.query.add_columns(
                case(
                    (func.count(Solicitacao.solicitacao_id) > 0, 'true'),
                    else_='false'
                ).label('possui_ss_aberta'),
                case(
                    (func.count(Solicitacao.solicitacao_id) > 0, Solicitacao.solicitacao_prioridade),
                    else_='0'
                ).label('prioridade_ss')
            ).outerjoin(Solicitacao, and_(
                Equipamento.equipamento_id == Solicitacao.solicitacao_equipamento,
                Equipamento.equipamento_filial == Solicitacao.solicitacao_filial,
                or_(
                    Solicitacao.solicitacao_status == 'A',
                    Solicitacao.solicitacao_status == 'D'
                ),
                Solicitacao.D_E_L_E_T_ != '*'
            )).filter(
                Equipamento.D_E_L_E_T_ != '*',
                Equipamento.T9_STATUS == '01'
            ))

            print("\n----> Filtros com a Filial / Setor <----")

            if filial_id:
                query = query.filter(Equipamento.equipamento_filial == filial_id)

            if setor_id:
                query = query.filter(Equipamento.equipamento_setor == setor_id)

            print(f"{'-' * 100}\nFinalizando a Montagem da Query SQL: \n{query}\n{'-' * 100}\n")

            # Importante: Ao usar funções agregadas, como COUNT, precisa usar group_by.
            # Motivo: Função agregada opera em um conjunto de linhas (agrupadas) e o SQL
            # precisa saber como tratar as colunas que não fazem parte dessa agregação.
            # Precisa aplicar em todas as colunas do SELECT, mesmo que elas não sejam usadas posteriormente.
            # Também precisa acrescentar os valores no Grupo By sempre que tentar acessar diretamente valores,
            # mesmo que de outras Models (Exemplo: Como no Outer Join acima.)
            equipamentos_com_status_ss = query.group_by(
                Equipamento.equipamento_id,
                Equipamento.equipamento_filial,
                Equipamento.equipamento_setor,
                Equipamento.equipamento_nome,
                Equipamento.equipamento_ccusto,
                Equipamento.D_E_L_E_T_,
                Equipamento.T9_STATUS,
                Solicitacao.solicitacao_prioridade  # Correção do Erro Column 'TQB010.TQB_PRIORI' is invalid
            ).order_by(Equipamento.equipamento_id).all()

            print("\n >> Resultado da Consulta (Antes da Serialização): << \n")
            print(equipamentos_com_status_ss, "\n")

            if not equipamentos_com_status_ss:
                return None, {"error": "Não existe nenhum equipamento para o setor ou filial fornecida."}

            # Serializando o resultado (Lista de Tuplas) para JSON.
            equipamento_schema = EquipamentoSchema(many=True)
            equipamentos_json = equipamento_schema.dump([e[0] for e in equipamentos_com_status_ss], many=True)

            # Valores Opcionais e Novos, precisam ser tratados seguindo o seguinte fluxo:
            # 1. Adicionar e mapear os valores no Schema que o Marshmallow vai usar.
            # 2. Usar a lógica abaixo pra serializar o novo campo manualmente.
            for equipamento_serializado, equipamento_tuple in zip(
                    equipamentos_json, equipamentos_com_status_ss):
                equipamento_serializado['possui_ss_aberta'] = equipamento_tuple[1]
                equipamento_serializado['prioridade_ss'] = equipamento_tuple[2]

            print("\n >> Resultado Após Serialização pelo Marshmallow: << \n")
            print(equipamentos_json)

            print(f"\n---->Primeiro Item da lista de Equipamentos Encontrados: {equipamentos_json[0]}\n")

            # Query SQL: Trás os Equipamentos e se tem S.S. Aberta.
            query_str = str(query.statement.compile(compile_kwargs={"literal_binds": True}))
            print(f"\n{'-' * 50}\n----> "
                  f"Query Final que foi executada (Equipamentos SS)): <----\n{query_str}\n{'-' * 50}\n")

            response_data = {
                "sql": query_str,
                "equipamentos": equipamentos_json
            }

            return response_data, None

        except OperationalError as e:
            return None, {"error": str(e)}
