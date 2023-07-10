from flask import Flask, render_template, request, redirect, url_for
from flask_behind_proxy import FlaskBehindProxy
from flask_caching import Cache
try:
    from .twitch_api import (
        generate_headers,
        get_streamer_data,
        get_active_streamers
    )
    from .config import Config
    from .models import db, FavoriteStreamer, ActiveStreamer
    from .routes import (
        home,
        webhook,
        search,
        add,
        remove,
        view_fav,
        view_pop,
        view
    )
    from .helpers import add_pop, get_streamers
except ImportError:
    from twitch_api import (
        generate_headers,
        get_streamer_data,
        get_active_streamers
    )
    from config import Config
    from models import db, FavoriteStreamer, ActiveStreamer
    from routes import (
        home,
        webhook,
        search,
        add,
        remove,
        view_fav,
        view_pop,
        view
    )
    from helpers import add_pop, get_streamers

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

cache = Cache(app)
cache.init_app(app)

cache.cached(timeout=3600)(add_pop)
app.route('/')(home)
app.route('/update_server', methods=['POST'])(webhook)
app.route('/search', methods=['POST'])(search)
app.route('/add', methods=['POST'])(add)
app.route('/remove', methods=['POST'])(remove)
app.route('/view_fav', methods=['GET', 'POST'])(view_fav)
app.route('/view_pop', methods=['GET', 'POST'])(view_pop)
app.route('/view', methods=['GET', 'POST'])(lambda: view('fav'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")