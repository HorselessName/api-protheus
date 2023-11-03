# == Equipamento Service ==

from sqlalchemy.exc import OperationalError
from models import Equipamento
from .utils import validar_filial, validar_setor
from schemas import EquipamentoSchema


class EquipamentoService:

    @staticmethod
    def fetch_equipamentos(filial_id=None, setor_id=None):
        """
        Lista todos os equipamentos cadastrados com base na filial e no setor fornecidos.
        Exemplo do SQL gerado:
        SELECT
            T9_CODBEM	as equipamento_id,
            T9_FILIAL	as equipamento_filial,
            T9_CODFAMI	as equipamento_setor,
            T9_NOME		as equipamento_nome,
            T9_CCUSTO	as equipamento_ccusto
        FROM ST9010 AS EQUIPAMENTO WHERE
            EQUIPAMENTO.D_E_L_E_T_	<> '*' AND
            EQUIPAMENTO.T9_STATUS	= '01' AND
            EQUIPAMENTO.T9_FILIAL	= '020101' AND
            EQUIPAMENTO.T9_CODFAMI	= 'GENERI';

        :param filial_id:
        :param setor_id:
        :return:
        """
        is_valid, message = validar_filial(filial_id)
        if not is_valid:
            return None, message

        is_valid, message = validar_setor(setor_id)
        if not is_valid:
            return None, message

        try:
            query = Equipamento.query.filter(Equipamento.D_E_L_E_T_ != '*').filter(Equipamento.T9_STATUS == '01')

            if filial_id:
                query = query.filter(Equipamento.equipamento_filial == filial_id)

            if setor_id:
                query = query.filter(Equipamento.equipamento_setor == setor_id)

            equipamentos = query.order_by(Equipamento.equipamento_id).all()
            print(f"----- Equipamentos: Passo 1 -----\n"
                  f"Usando o @DataClass para converter os equipamentos para JSON...\n"
                  f"Biblioteca: Flask JSONify.\n"
                  f"Equipamentos brutos: {equipamentos}")

            if not equipamentos:
                return None, "Não existe nenhum equipamento para o setor ou filial fornecida."

            try:
                print(f"Serializando os equipamentos...: {equipamentos}")
                equipamento_schema = EquipamentoSchema(many=True)
                equipamentos_json = equipamento_schema.dump(equipamentos, many=True)
                print("-" * 30)
                print(f"Equipamentos serializados...: {equipamentos_json}")

            except ValueError as ve:
                print(f"Erro ao serializar os equipamentos: {ve}")
                return None, f"Erro ao serializar os equipamentos: {ve}"

            return equipamentos_json, None

        except OperationalError as e:
            return None, str(e)

