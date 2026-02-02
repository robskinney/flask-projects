from flask import Flask, render_template
from flask_session import Session

def create_app():
    app = Flask(__name__)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # import and register blueprints
    from celebguessr.routes import celebguessr
    from gorillacarts.routes import gorillacarts
    from autotrackr.routes import autotrackr
    
    app.register_blueprint(celebguessr, url_prefix='/celebguessr')
    app.register_blueprint(gorillacarts, url_prefix='/gorillacarts')
    app.register_blueprint(autotrackr, url_prefix='/autotrackr')

    @app.route('/')
    def index():
        return render_template('directory.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
