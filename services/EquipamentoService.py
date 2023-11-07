# == Equipamento Service ==

from sqlalchemy.exc import OperationalError
from models import Equipamento
from .utils import validar_filial, validar_setor
from schemas import EquipamentoSchema


class EquipamentoService:

    @staticmethod
    def fetch_equipamentos(filial_id=None, setor_id=None):
        print(f"\n----> Trazendo os Equipamentos da Filial {filial_id} e Setor {setor_id} <----\n")
        is_valid_filial, message_filial = validar_filial(filial_id)
        if not is_valid_filial:
            return None, {"error": f"Erro na filial: {message_filial}"}

        is_valid_setor, message_setor = validar_setor(setor_id)
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

            query_str = str(query.statement.compile(compile_kwargs={"literal_binds": True}))
            print(f"\n{'-' * 50}\n----> Query Final que foi executada: <----\n{query_str}\n{'-' * 50}\n")

            response_data = {
                "sql": query_str,
                "equipamentos": equipamentos_json
            }

            return response_data, None

        except OperationalError as e:
            return None, {"error": str(e)}
