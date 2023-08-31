from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db=SQLAlchemy()
app=Flask(__name__)

def create_app():
    
    bootstrap = Bootstrap5(app)

    # Create secret key for session object
    app.secret_key='wWW07KyIZIx2lDnaK5LYeHmtEXORydZa'

    # Configure and initialise DB
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///eventdb.sqlite'
    db.init_app(app)
    
    # Initialize the login manager
    login_manager = LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    # Create a user loader function takes userid and returns User
    from .models import User  # Importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Add Blueprints
    from . import views
    app.register_blueprint(views.mainbp)
    from . import event
    app.register_blueprint(event.bp)
    from . import auth
    app.register_blueprint(auth.bp)

    return app

@app.errorhandler(404) 

def not_found(e): 
  return render_template("404.html")

@app.errorhandler(500)

def internal_server_error(e):
    return render_template('500.html')

