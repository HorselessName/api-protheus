import json

from models import EspecialidadesDoExecutor, Executor, DetalhesEspecialidade
from services.Utils import verificar_asterisco
from sqlalchemy.orm import aliased


class ExecutorService:

    @staticmethod
    def validar_executor(executor):
        """
        Valida se o Executor recebido é válido.
        Para ser válido:

        1. Deve conter o código do usuário vinculado ao executor.
        """

        if executor.get('executor_usuario'):
            return True
        else:
            return False

    @staticmethod
    def especialidade_para_dict(especialidade_do_executor):
        """
        Converte um objeto EspecialidadesDoExecutor para um dicionário.
        """
        return {
            'especialidade_codigo': especialidade_do_executor.especialidade_codigo,
            'especialidade_nome': especialidade_do_executor.detalhes_especialidade.especialidade_nome
        }

    @staticmethod
    def especialidades_dos_executores(executante_codigo):
        """
        Retorna uma lista de dicionários representando as especialidades de um executor.
        """
        query_especialidades_do_executor = (EspecialidadesDoExecutor.query
                                            .filter_by(executante_codigo=executante_codigo).all())
        especialidades_do_executor = [ExecutorService
                                      .especialidade_para_dict(especialidade)
                                      for especialidade in query_especialidades_do_executor]

        print("Especialidades do Executor: ", especialidades_do_executor)
        return especialidades_do_executor

    @staticmethod
    def get_executor_por_matricula(executante_codigo):
        """
        Retorna uma lista de dicionários representando os executores.
        """
        executor = Executor.query.filter_by(executor_matricula=executante_codigo).first()

        if executor:
            # Preparar o dicionário do executor
            executor_dict = {
                "executor_matricula": executor.executor_matricula,
                "executor_filial": executor.executor_filial,
                "executor_nome": executor.executor_nome,
                "executor_email": executor.executor_email,
                "executor_usuario": executor.executor_usuario,
                "executor_ccusto": executor.exeutor_ccusto,
                "executor_turno": executor.executor_turno,
                "especialidades": [
                    {
                        "especialidade_codigo": especialidade.especialidade_codigo,
                        "especialidade_nome": especialidade.detalhes_especialidade.especialidade_nome
                    }
                    for especialidade in executor.executor_especialidades
                ]
            }

            print(json.dumps(executor_dict, indent=4))
            return executor_dict
        else:
            print("Executor não encontrado.")
            return None

    @staticmethod
    def get_executores_por_especialidade(especialidade_nome):
        """
        Retorna uma lista de dicionários representando os executores.
        Neste método é possível trazer TODOS os Executores, passando `*` como parâmetro.
        Ou, para filtrar executores por tipos de especialidades, passar o nome da especialidade, que o filtro
        consegue acessar a dependência e fazer o filtro de executores que possuem aquela especialidade.
        """
        if verificar_asterisco(especialidade_nome):
            query_executores = Executor.query.join(EspecialidadesDoExecutor).all()
        else:
            especialidades_alias = aliased(EspecialidadesDoExecutor)
            query_executores = (Executor.query
                                .join(especialidades_alias)
                                .join(DetalhesEspecialidade)
                                .filter(DetalhesEspecialidade.especialidade_nome == especialidade_nome)
                                .all())

        # Serialização dos executores
        executores = [
            {
                "executor_matricula": executor.executor_matricula,
                "executor_filial": executor.executor_filial,
                "executor_nome": executor.executor_nome,
                "executor_email": executor.executor_email,
                "executor_usuario": executor.executor_usuario,
                "executor_ccusto": executor.exeutor_ccusto,
                "executor_turno": executor.executor_turno,
                "especialidades": [
                    {
                        "especialidade_codigo": especialidade.especialidade_codigo,
                        "especialidade_nome": especialidade.detalhes_especialidade.especialidade_nome
                    }
                    for especialidade in executor.executor_especialidades
                ]
            }
            for executor in query_executores
        ]

        print(json.dumps(executores, indent=4))
        return executores
