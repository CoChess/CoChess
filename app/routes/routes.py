from app.controllers import auth_controller, user_controller

def configure_routes(app):
    app.add_url_rule('/', view_func=auth_controller.home)
    app.add_url_rule('/login', view_func=auth_controller.login, methods=['GET', 'POST'])
    app.add_url_rule('/create_account', view_func=auth_controller.create_account, methods=['GET', 'POST'])
    app.add_url_rule('/change_password', view_func=user_controller.change_password, methods=['GET', 'POST'])
    app.add_url_rule('/change_nickname', view_func=user_controller.change_nickname, methods=['GET', 'POST'])
    app.add_url_rule('/lobby', view_func=user_controller.lobby)
    app.add_url_rule('/lobby/train', view_func=user_controller.train)
    app.add_url_rule('/lobby/history', view_func=user_controller.history)
    app.add_url_rule('/lobby/game', view_func=user_controller.game, methods=['GET', 'POST'])
    app.add_url_rule('/game/move', view_func=user_controller.move, methods=['GET', 'POST'])
