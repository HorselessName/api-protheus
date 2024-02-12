def initialize_routes(app):
    from routes.EquipamentoRoute import blueprint_equipamentos
    app.register_blueprint(blueprint_equipamentos)

    from routes.SolicitacaoRoute import blueprint_manutencao
    app.register_blueprint(blueprint_manutencao)

    from routes.FilialRoute import blueprint_filial
    app.register_blueprint(blueprint_filial)

    from routes.ExecutorRoute import blueprint_executores
    app.register_blueprint(blueprint_executores)

    from routes.OrdemServicoRoute import blueprint_ordem_servico
    app.register_blueprint(blueprint_ordem_servico)

    from routes.ProdutoRoute import blueprint_produtos
    app.register_blueprint(blueprint_produtos)
