from sqlalchemy.exc import OperationalError
from models.EquipamentoModel import Equipamento


class EquipamentoService:
    @staticmethod
    def fetch_equipamentos(filial_id=None, setor_id=None):
        try:
            query = Equipamento.query.filter(Equipamento.D_E_L_E_T_ != '*').filter(Equipamento.T9_STATUS == '01')

            if filial_id:
                query = query.filter(Equipamento.equipamento_filial == filial_id)

            if setor_id:
                query = query.filter(Equipamento.equipamento_setor == setor_id)

            equipamentos = query.order_by(Equipamento.equipamento_id).all()
            return [equipamento.to_dict() for equipamento in equipamentos], None
        except OperationalError as e:
            return None, str(e)
