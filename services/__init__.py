import re
from sqlalchemy.exc import OperationalError
from models import Equipamento, Filial, Solicitacao


# == Validações ==

def validar_filial(filial: str) -> (bool, str):
    if not bool(re.match("^[0-9]+$", filial)):
        return False, "A filial deve conter apenas números."
    return True, ""


def validar_setor(setor: str) -> (bool, str):
    if " " in setor or not re.match("^[a-zA-Z0-9]*$", setor):
        return False, "O setor não deve conter espaços ou caracteres especiais."
    return True, setor.upper()


def validar_equipamento(equipamento: str) -> (bool, str):
    if not bool(re.match("^[a-zA-Z0-9]+$", equipamento)):
        return False, "O equipamento não deve conter caracteres especiais ou espaços."
    return True, equipamento.upper()


# == Equipamento Service ==

class EquipamentoService:

    @staticmethod
    def fetch_equipamentos(filial_id=None, setor_id=None):
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

            if not equipamentos:
                return None, "Não existe nenhum equipamento para o setor ou filial fornecida."

            return [equipamento.to_dict() for equipamento in equipamentos], None
        except OperationalError as e:
            return None, str(e)


# == Filial Service ==

class FilialService:

    @staticmethod
    def buscar_todas_filiais():
        filiais = Filial.query.filter(Filial.D_E_L_E_T_ != '*').all()
        return [filial.to_dict() for filial in filiais], None


# == Manutenção Service ==

class ManutencaoService:

    @staticmethod
    def buscar_solicitacoes_abertas(filial: str, equipamento: str):
        valido, msg_filial = validar_filial(filial)
        if not valido:
            return None, msg_filial, None

        valido, msg_equipamento = validar_equipamento(equipamento)
        if not valido:
            return None, msg_equipamento, None

        solicitacoes = Solicitacao.query.filter(
            Solicitacao.solicitacao_filial == filial,
            Solicitacao.solicitacao_equipamento == equipamento,
            Solicitacao.solicitacao_status == 'A',
            Solicitacao.D_E_L_E_T_ != '*'
        ).all()

        possui_ss_aberta = len(solicitacoes) > 0
        return [s.to_dict() for s in solicitacoes], None, possui_ss_aberta
