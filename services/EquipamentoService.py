# == Equipamento Service ==

from sqlalchemy.exc import OperationalError
from models import Equipamento
from .utils import validar_filial, validar_setor
from schemas import EquipamentoSchema


class EquipamentoService:

    @staticmethod
    def fetch_equipamentos(filial_id=None, setor_id=None):
        is_valid_filial, message_filial = validar_filial(filial_id)
        if not is_valid_filial:
            return None, {"error": f"Erro na filial: {message_filial}"}

        is_valid_setor, message_setor = validar_setor(setor_id)
        if not is_valid_setor:
            return None, {"error": f"Erro no setor: {message_setor}"}

        try:
            query = Equipamento.query.filter(Equipamento.D_E_L_E_T_ != '*').filter(Equipamento.T9_STATUS == '01')

            if filial_id:
                query = query.filter(Equipamento.equipamento_filial == filial_id)

            if setor_id:
                query = query.filter(Equipamento.equipamento_setor == setor_id)

            equipamentos = query.order_by(Equipamento.equipamento_id).all()

            if not equipamentos:
                return None, {"error": "Não existe nenhum equipamento para o setor ou filial fornecida."}

            equipamento_schema = EquipamentoSchema(many=True)
            equipamentos_json = equipamento_schema.dump(equipamentos, many=True)

            # Converte a consulta para uma string, substituindo os placeholders pelas strings informadas
            query_str = str(query.statement.compile(compile_kwargs={"literal_binds": True}))

            response_data = {
                "sql": query_str,
                "equipamentos": equipamentos_json
            }

            return response_data, None

        except OperationalError as e:
            return None, {"error": str(e)}
