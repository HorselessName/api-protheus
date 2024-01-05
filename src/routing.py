def initialize_routes(app):
    from routes.EquipamentoRoute import blueprint_equipamentos
    app.register_blueprint(blueprint_equipamentos)

    from routes.ManutencaoRoute import blueprint_manutencao
    app.register_blueprint(blueprint_manutencao)

    from routes.FilialRoute import blueprint_filial
    app.register_blueprint(blueprint_filial)

