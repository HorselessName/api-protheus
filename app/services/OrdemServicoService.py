from sqlalchemy import func
from sqlalchemy.dialects import mssql

from db_context import db_sql
from models import OrdemServico, OrdemServicoInsumo, OrdemServicoComentario
from schemas import OrdemServicoSchema, OrdemServicoInsumoSchema, OrdemServicoComentarioSchema
from services.Utils import format_sql_query
from datetime import datetime, timedelta

import json

class OrdemServicoService:
    @staticmethod
    def get_ordens_por_solicitacao(ordem_codsolicitacao: str, ordem_filial: str):
        try:
            query_ordens_servico = OrdemServico.query.filter(
                OrdemServico.ordem_codsolicitacao == ordem_codsolicitacao,
                OrdemServico.ordem_filial == ordem_filial
            )
            query_ordens_servico_str = format_sql_query(query_ordens_servico)
            ordens_servico_schema = OrdemServicoSchema(many=True)
            ordens_servico_json = ordens_servico_schema.dump(query_ordens_servico.all())

            # PS: O `Dump` do Marshmallow só faz o `dump`, ou seja, permite os dados serem serializados para JSON.
            # Diferente do `Dumps`, que faz o `dump` e depois o `loads`, ou seja, que já retorna um JSON pronto.

            return ordens_servico_json, query_ordens_servico_str

        except Exception as e:
            return {"message": f"Erro ao buscar as ordens de serviço: {e}"}, 500

    @staticmethod
    def filtrar_ordens_servico(ordem_id, ordem_filial):
        """
        Aplica um filtro padrão às Ordens de Serviço.
        """
        return OrdemServico.query.filter(
            OrdemServico.ordem_excluida == '',
            OrdemServico.ordem_hora_previsto_inicio_manutencao != "00:00",
            OrdemServico.ordem_codsolicitacao != "",
            OrdemServico.ordem_situacao == "L",
            OrdemServico.ordem_id == ordem_id,
            OrdemServico.ordem_filial == ordem_filial
        )

    @staticmethod
    def get_todas_ordens_servico():
        # 1. Query para trazer as O.S. com os filtros de O.S.
        todas_ordens_servico = OrdemServico.query.filter(
            OrdemServico.ordem_excluida != '*',
            OrdemServico.ordem_codsolicitacao != '',
            OrdemServico.ordem_situacao == 'L',
            OrdemServico.ordem_horaco1 == '',
            OrdemServico.ordem_horaco2 == ''
        )

        # 2. Serialização das O.S. para JSON.
        todas_ordens_servico_schema = OrdemServicoSchema(many=True)
        todas_ordens_servico_json = todas_ordens_servico_schema.dump(todas_ordens_servico)

        # 3. Retorno dos dados em JSON.
        print("-" * 30)
        print("Get Todas O.s. - Ordens de Serviço Formatadas:")
        print(todas_ordens_servico_json, "\n\n", format_sql_query(todas_ordens_servico), '\n\n')

        # Para testes: Chama o metodo `adicionar_comentarios_na_observacao` para adicionar comentarios na observação
        # Atualiza o campo de Observação com a STRING informada.
        # OrdemServicoService.adicionar_comentarios_na_observacao()
        # OrdemServicoService.get_json_da_observacao_os()
        OrdemServicoService.get_comentarios_da_os()

        # 4. Agora passamos os dicionários JSON para o método pegar_observacao_os
        for ordem_json in todas_ordens_servico_json:
            OrdemServicoService.pegar_observacao_os_no_loop(ordem_json)

        return todas_ordens_servico_json, format_sql_query(todas_ordens_servico)

    @staticmethod
    def pegar_observacao_os_no_loop(ordem_json):
        print("##### Ordem - S.S. ID:", ordem_json['ordem_codsolicitacao'])
        observacao = ordem_json.get('ordem_observacao', None)

        if observacao:
            try:
                dados_json = json.loads(observacao)
                print("##### Ordem - O.S. Observação JSON:", dados_json)
            except json.JSONDecodeError as erro_ao_pegar_observacao:
                print(f"Erro ao decodificar JSON da observação na O.S. ID {ordem_json.get('ordem_codsolicitacao')}: "
                      f"{erro_ao_pegar_observacao}")
        else:
            print("##### Ordem - O.S. Observação: Vazio ou None")

    @staticmethod
    def adicionar_comentarios_na_observacao(ordem_id='014179'):
        """
        Adiciona comentários na Observação da O.S. com o ID informado.
        """
        ordem_servico = OrdemServico.query.filter_by(ordem_id=ordem_id).first()
        if ordem_servico:
            print(f"Encontrei a O.S. {ordem_id} que vou adicionar comentários na observação.")
            # Verifica se a observação atual é um JSON válido
            observacao_atual_json = OrdemServicoService.get_json_da_observacao_os(ordem_id)
            if observacao_atual_json is not None:
                try:
                    novo_comentario = json.dumps({"mensagem": "Alteração pelo APP"})

                    # Converte a STRING JSON para VARBINARY (Processo Inverso do que foi feito na Model)
                    ordem_servico.ordem_observacao_binario = novo_comentario.encode('latin1')
                    db_sql.session.commit()
                    print(f"Comentários adicionados com sucesso na O.S. {ordem_id}.")

                except Exception as e:
                    db_sql.session.rollback()
                    print(f"Erro ao adicionar comentários na observação da O.S. {ordem_id}: {e}")
            else:
                print(f"A observação atual da O.S. {ordem_id} não está em formato JSON válido. Atualização cancelada.")
        else:
            print(f"Não encontrei a O.S. {ordem_id} para adicionar comentários na observação.")

    @staticmethod
    def get_json_da_observacao_os(ordem_id='014179'):
        ordem_servico = OrdemServico.query.filter_by(ordem_id=ordem_id).first()
        if ordem_servico and ordem_servico.ordem_observacao_binario:
            observacao_texto = ordem_servico.ordem_observacao
            try:
                print(f"Verificando formato JSON da observação da O.S. {ordem_id}: {observacao_texto}")
                dados_json = json.loads(observacao_texto)
                print(f"Observação da O.S. {ordem_id} é um JSON válido: {dados_json}")
                return dados_json
            except json.JSONDecodeError:
                print(f"A observação da O.S. {ordem_id} não está em um formato JSON válido. Impossível desserializar.")
                return None
        else:
            print(f"Ordem de serviço {ordem_id} não encontrada ou sem observação.")
            return None

    @staticmethod
    def get_comentarios_da_os(ordem_id='014179', ordem_filial='020101'):
        """
        Faz um SELECT nos Comentários da O.S., serializa pra JSON com o Marshmallow.
        """
        comentarios = OrdemServicoComentario.query.filter_by(
            comentario_os_ordem=ordem_id,
            comentario_os_filial=ordem_filial
        ).all()

        if comentarios:
            schema = OrdemServicoComentarioSchema(many=True)
            comentarios_serializados = schema.dump(comentarios)

            print(f"Comentários encontrados para a O.S. {ordem_id}:")
            for comentario in comentarios_serializados:
                print(comentario)

            return comentarios_serializados
        else:
            print(f"Nenhum comentário encontrado para a O.S. {ordem_id}.")
            return []

    @staticmethod
    def adicionar_comentario_na_os(ordem_id, filial, texto_comentario, comentario_os_seq=None, recno=None):

        try:
            novo_comentario = OrdemServicoComentario(
                comentario_os_filial=filial,
                comentario_os_seq=comentario_os_seq,
                comentario_os_ordem=ordem_id,
                comentario_os_texto=texto_comentario,
                # TODO: Fix the date and time fields giving "Expected type 'Mapped[str]', got 'str' instead " error.
                comentario_os_data=datetime.now().strftime('%Y%m%d'),
                comentario_os_hora=datetime.now().strftime('%H:%M'),
                R_E_C_N_O_=recno
            )
            db_sql.session.add(novo_comentario)
            db_sql.session.commit()
            print(f"Comentário adicionado com sucesso na O.S. {ordem_id}.")
        except Exception as e:
            db_sql.session.rollback()
            print(f"Erro ao adicionar comentário na O.S. {ordem_id}: {e}")

    @staticmethod
    def get_ordem_servico(ordem_id: str, ordem_filial: str):
        """
        Retorna UMA Ordem de Serviço.
        """

        # 1. Query para trazer as O.S. com os filtros acima.
        uma_ordem_servico = OrdemServicoService.filtrar_ordens_servico(ordem_id, ordem_filial)

        # 2. Serialização das O.S. para JSON.
        uma_ordem_servico_schema = OrdemServicoSchema(many=True)
        uma_ordem_servico_json = uma_ordem_servico_schema.dump(uma_ordem_servico)

        # 3. Retorno dos dados em JSON.
        print("-" * 30)
        print("Get UMA O.S. - O.S. Formatada, filtro por Filial e Ordem ID:")
        print(uma_ordem_servico_json, "\n\n", format_sql_query(uma_ordem_servico))

        return uma_ordem_servico_json, format_sql_query(uma_ordem_servico)

    @staticmethod
    def get_insumos_por_ordem(ordem_id: str, ordem_filial: str):
        """
        Retorna os Insumos de UMA Ordem de Serviço. Retorno somente os campos mais relevantes, que são:

        - insumo_tipo
        - insumo_codigo
        - insumo_quantidade
        - insumo_unidade
        - insumo_data_inicio
        - insumo_hora_inicio

        """

        print("Pegando Insumos por Ordem...")

        # 1. Query para trazer os insumos da O.S.
        insumos_ordem_servico = OrdemServicoInsumo.query.filter(
            OrdemServicoInsumo.insumo_ordem_id == ordem_id,
            OrdemServicoInsumo.insumo_filial == ordem_filial
        )

        print("Insumos da O.S., QUERY Montada:", insumos_ordem_servico)

        # 2. Serialização dos insumos para JSON.
        insumos_ordem_servico_schema = OrdemServicoInsumoSchema(many=True)
        insumos_ordem_servico_json = insumos_ordem_servico_schema.dump(insumos_ordem_servico)

        # 3. Retorno dos dados em JSON
        print("-" * 30)
        print("Get Insumos - O.S. Formatada, filtro por Filial e Ordem ID:")
        print(insumos_ordem_servico_json, "\n\n", format_sql_query(insumos_ordem_servico))

        return insumos_ordem_servico_json, format_sql_query(insumos_ordem_servico)

    # noinspection PyTypeChecker
    @staticmethod
    def incluir_insumo_na_ordem(ordem_id, ordem_filial, insumo_dados: dict):
        """
        Inclui um novo Insumo para  OS e Filial Informada, utilizando o JSON enviado.
        Filtra pelo ID da Ordem e pela Filial.

        Campos:
        insumo_ordem_id (TL_ORDME)
        insumo_filial (TL_FILIAL)

        Ref: https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/queries/

        """
        try:

            # Obtendo o valor máximo atual da coluna R_E_C_N_O_
            max_rec_no = db_sql.session.query(func.max(OrdemServicoInsumo.R_E_C_N_O_)).scalar()
            if max_rec_no is None:
                max_rec_no = 1  # Caso não haja registros, comece do 1

            # Incrementando o valor máximo
            novo_rec_no = max_rec_no + 1

            # Criando uma nova instância de OrdemServicoInsumo
            novo_insumo = OrdemServicoInsumo(
                R_E_C_N_O_=novo_rec_no,
                insumo_ordem_id=ordem_id,
                insumo_filial=ordem_filial,
                insumo_codigo=insumo_dados["insumo_codigo"],
                insumo_quantidade=insumo_dados["insumo_quantidade"],
                insumo_tipo=insumo_dados["insumo_tipo"],
                insumo_unidade=insumo_dados["insumo_unidade"],

                # Campos Adicionais Necessários
                # Ref: https://tdn.totvs.com/pages/releaseview.action?pageId=543079696
                insumo_data_inicio=datetime.now().strftime('%Y%m%d'),
                insumo_hora_inicio=datetime.now().strftime('%H:%M'),

                # Incremento uma hora na hora/data acima com o `timedelta`
                insumo_data_fim=(datetime.now() + timedelta(hours=1)).strftime('%Y%m%d'),
                insumo_hora_fim=(datetime.now() + timedelta(hours=1)).strftime('%H:%M'),
            )

            # Gera uma lista de `OrderedDict`s com os insumos já existentes na O.S. Pega o primeiro, que é os insumos.
            insumos_existentes = OrdemServicoService.get_insumos_por_ordem(
                ordem_id, ordem_filial)[0]

            # Iterando sobre os insumos existentes
            for insumo in insumos_existentes:
                # Acessando o dicionário interno 'detalhes_insumo', se existir
                detalhes_insumo = insumo.get('detalhes_insumo', {})

                print("########## Detalhes do Insumo Existente:", detalhes_insumo)
                print("########## Insumo Existente Código:", detalhes_insumo.get("insumo_codigo"))
                print("########## Novo Insumo Código:", novo_insumo.insumo_codigo)

                # Removendo espaços em branco e convertendo para o mesmo caso para comparação
                codigo_insumo_existente = detalhes_insumo.get("insumo_codigo", "").strip().upper()
                codigo_novo_insumo = novo_insumo.insumo_codigo.strip().upper()

                if codigo_novo_insumo == codigo_insumo_existente:
                    print("########## Insumo já incluso na O.S.!")
                    return False, "Insumo já incluso na O.S."

            db_sql.session.add(novo_insumo)
            db_sql.session.commit()

            # Criando uma representação da consulta de inserção para fins de Logging
            insert_statement = db_sql.insert(OrdemServicoInsumo).values(
                R_E_C_N_O_=novo_rec_no,
                insumo_ordem_id=ordem_id,
                insumo_filial=ordem_filial,
                insumo_codigo=insumo_dados["insumo_codigo"],
                insumo_quantidade=insumo_dados["insumo_quantidade"],
                insumo_tipo=insumo_dados["insumo_tipo"],
                insumo_unidade=insumo_dados["insumo_unidade"],

                # Campos Adicionais Necessários
                # Ref: https://tdn.totvs.com/pages/releaseview.action?pageId=543079696
                insumo_data_inicio=datetime.now().strftime('%Y%m%d'),
                insumo_hora_inicio=datetime.now().strftime('%H:%M'),

                # Incremento uma hora na hora/data acima com o `timedelta`
                insumo_data_fim=(datetime.now() + timedelta(hours=1)).strftime('%Y%m%d'),
                insumo_hora_fim=(datetime.now() + timedelta(hours=1)).strftime('%H:%M'),
            )

            compiled_query = insert_statement.compile(dialect=mssql.dialect(), compile_kwargs={"literal_binds": True})
            sql_query_str = str(compiled_query)

            print("-" * 30)
            print("Query de Inserção do Insumo:", sql_query_str)

            return True, "Insumo incluído com sucesso."
        except Exception as e:
            print("Ocorreu um Erro no INSERT: ", e)
            # Em caso de erro, desfazer a transação e retornar False.
            db_sql.session.rollback()
            return False, "Erro ao incluir o insumo na O.S."
