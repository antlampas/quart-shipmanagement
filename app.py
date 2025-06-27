#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

from jose            import jwt

from quart           import Quart
from quart           import url_for
from quart           import jsonify
from quart           import session
from quart           import redirect
from quart           import request
from quart_wtf       import CSRFProtect
from quart_session   import Session

from quart_keycloak  import Keycloak
from quart_keycloak  import KeycloakAuthToken
from quart_keycloak  import KeycloakLogoutRequest

from dotenv import load_dotenv

load_dotenv()

def create_app(mode='Development'):
    from config import Development
    from config import Production

    app = Quart(__name__)
    app.config.from_object(f"config.{mode}")

    Session(app)
    csrf = CSRFProtect(app)
    keycloak = Keycloak(app, **(app.config["OPENID_KEYCLOAK_CONFIG"]))

    from authorization import require_role,isTokenExpired
    from model         import db
    db.init_app(app)
    db.create_all()

    from indexView          import index_blueprint
    from crewView           import crew_blueprint
    from divisionsView      import divisions_blueprint
    from ranksView          import ranks_blueprint
    from dutiesView         import duties_blueprint
    from tasksView          import tasks_blueprint
    from missionsView       import missions_blueprint
    from crewOnboardLogView import crewOnboardLog_blueprint

    app.register_blueprint(index_blueprint)
    app.register_blueprint(crew_blueprint)
    app.register_blueprint(divisions_blueprint)
    app.register_blueprint(ranks_blueprint)
    app.register_blueprint(duties_blueprint)
    app.register_blueprint(tasks_blueprint)
    app.register_blueprint(missions_blueprint)
    app.register_blueprint(crewOnboardLog_blueprint)

    @app.before_request
    async def before_request_callback():
        if isTokenExpired() and (request.path != url_for('relogin')):
            return redirect(url_for('relogin'))

    @app.route("/login")
    async def login():
        login_url_keycloak = url_for(keycloak.endpoint_name_login)
        return redirect(login_url_keycloak)

    @keycloak.after_login()
    async def handle_user_login(auth_token: KeycloakAuthToken):
        session['auth_token']   = auth_token
        session['access_token'] = jwt.get_unverified_claims(session['auth_token'].access_token)
        return redirect(url_for('index.index'))

    @app.route("/logout")
    async def logout():
        logout_url = url_for(keycloak.endpoint_name_logout, redirect_uri=url_for("after_logout", _external=True))
        return redirect(logout_url)

    @app.route("/relogin")
    async def relogin():
        relogin_url_keycloak = url_for(keycloak.endpoint_name_logout, redirect_uri=url_for("after_relogin", _external=True))
        return redirect(relogin_url_keycloak)

    @app.route("/after_logout")
    async def after_logout():
        session.clear()
        return redirect(url_for('index.index'))

    @app.route("/after_relogin")
    async def after_relogin():
        session.clear()
        return redirect(url_for('login'))
    return app
