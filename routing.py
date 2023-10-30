from routes.EquipamentosRoutes import equipamentos_routes
from routes.ManutencaoRoutes import manutencao_routes
from routes.FilialRoutes import filial_routes


def initialize_routes(app):
    equipamentos_routes(app)
    manutencao_routes(app)
    filial_routes(app)
