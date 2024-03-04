from models import Produto
from schemas import ProdutoSchema
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError


class ProdutoService:
    @staticmethod
    def trazer_produtos(tipos, pagina=1, itens_por_pagina=5000):
        try:
            print("#" * 50)
            print("# Iniciando a busca de produtos com paginação")
            if isinstance(tipos, str):
                tipos = [tipos]

            print("#" * 50)
            print(f"# Filtrando produtos pelos tipos: {tipos}, página: {pagina}, itens por página: {itens_por_pagina}")

            produtos_paginados = Produto.query.filter(Produto.produto_tipo.in_(tipos))

            print("#" * 50)
            print(f"# Consulta SQL antes da paginação: {produtos_paginados}")

            produtos_paginados = Produto.query.filter(Produto.produto_tipo.in_(tipos)).order_by(
                Produto.produto_codigo).paginate(page=pagina, per_page=itens_por_pagina, error_out=False)

            produto_schema = ProdutoSchema(many=True)
            produtos = produto_schema.dump(produtos_paginados.items)

            print("#" * 50)
            print(f"# Produtos obtidos com sucesso. Lista de Produtos: {produtos}")
            return produtos

        except SQLAlchemyError as e:
            print("#" * 50)
            print(f"# Erro na consulta ao banco de dados: {str(e)}")
            return {"erro": f"Erro na consulta ao banco de dados: {str(e)}"}

        except ValidationError as e:
            print("#" * 50)
            print(f"# Erro de validação dos dados: {str(e)}")
            return {"erro": f"Erro de validação dos dados: {str(e)}"}

        except Exception as e:
            print("#" * 50)
            print(f"# Erro inesperado: {str(e)}")
            return {"erro": f"Erro inesperado: {str(e)}"}

        finally:
            print("#" * 50)
            print("# Finalizando a execução do método trazer_produtos")
