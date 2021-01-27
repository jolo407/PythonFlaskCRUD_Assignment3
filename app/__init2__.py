import os
from flask import Flask

def create_app(test_config=None):
    app = FLASK(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=b'\xd6\x04\xbdj\xfe\xed$c\x1e@\xad\x0f\x13,@G',
        DATABASE=os.path.join(app.instance_path, "app.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
        except OSError:
            password

    from . import db
    db.init_app2(app)

    from . import auth
    app.register_blueprint(auth.app)

    from . import reviewapp.register_blueprint(review.app)
    app.add_url_rule("/", endpoint="home")

    return app