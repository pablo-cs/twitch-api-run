import git
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask import Flask, render_template, request, redirect, url_for
from flask_behind_proxy import FlaskBehindProxy
try:
    from .twitch_api import (
        generate_headers,
        get_streamer_data,
        get_active_streamers
    )
except ImportError:
    from twitch_api import (
        generate_headers,
        get_streamer_data,
        get_active_streamers
    )
app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = '91062784e313e6292e50dfe09b0ea33e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///streamers.db'
app.config['SQLALCHEMY_BINDS'] = {
    'favorites': 'sqlite:///favorites.db',
    'popular': 'sqlite:///popular_users.db'
}
db = SQLAlchemy(app)
cache = Cache(app)


class FavoriteStreamer(db.Model):
    __bind_key__ = 'favorites'
    id = db.Column(db.String, primary_key=True)
    url = db.Column(db.String(120), nullable=False)
    login = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    follower_count = db.Column(db.String(120), nullable=False)
    broadcaster_type = db.Column(db.String(20), nullable=False)
    last_played = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.String(120), nullable=False)
    img_src = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return (
            f"Streamer(id={self.id}, "
            f"name='{self.name}', "
            f"follower_count='{self.follower_count}')"
        )


class ActiveStreamer(db.Model):
    __bind_key__ = 'popular'
    id = db.Column(db.String, primary_key=True)
    url = db.Column(db.String(120), nullable=False)
    login = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    follower_count = db.Column(db.String(120), nullable=False)
    broadcaster_type = db.Column(db.String(20), nullable=False)
    last_played = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.String(120), nullable=False)
    img_src = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return (
            f"Streamer(id={self.id}, "
            f"name='{self.name}', "
            f"follower_count='{self.follower_count}')"
        )


with app.app_context():
    db.create_all()


@cache.cached(timeout=3600)
def add_pop():
    with app.app_context():
        headers = generate_headers()
        pop_data = get_active_streamers(headers)
        for streamer_data in pop_data:
            if streamer_data:
                existing_streamer = ActiveStreamer.query.filter_by(
                                    name=streamer_data['name']).first()
                followers = format(streamer_data['follower_count'], ",")
                if not existing_streamer:
                    streamer = ActiveStreamer(
                        id=streamer_data['id'],
                        url=streamer_data['url'],
                        login=streamer_data['login'],
                        name=streamer_data['name'],
                        description=streamer_data['description'],
                        follower_count=followers,
                        broadcaster_type=streamer_data['broadcaster_type'],
                        last_played=streamer_data['last_game_played'],
                        created_at=streamer_data['created_at'],
                        img_src=streamer_data['pfp_url']
                    )
                    db.session.add(streamer)
                    db.session.commit()


@app.route('/')
def home():
    add_pop()
    return render_template('index.html', streamers=get_streamers('pop'))


@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/pcrisostomosuarez/twitch-api-run')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


@app.route('/search', methods=['POST'])
def search():
    "Route to search for a streamer using Twitch API"
    if request.form.get('search'):
        user_name = request.form.get('search')
    headers = generate_headers()
    streamer_data = get_streamer_data(user_name, headers)
    if streamer_data:
        existing_streamer = FavoriteStreamer.query.filter_by(
                            name=streamer_data['name']).first()
        streamer_exists = bool(existing_streamer)
        videos = streamer_data['video_data'][:5]
        followers = format(streamer_data['follower_count'], ",")
        return render_template(
                'results.html',
                streamer=streamer_data['name'],
                url=streamer_data['url'],
                login=streamer_data['login'],
                description=streamer_data['description'],
                followers=followers,
                broadcaster_type=streamer_data['broadcaster_type'],
                last_played=streamer_data['last_game_played'],
                created_at=streamer_data['created_at'],
                img_src=streamer_data['pfp_url'],
                videos=videos,
                in_db=streamer_exists)
    else:
        return render_template('results.html', streamer=None, description=None)


@app.route('/add', methods=['POST'])
def add():
    "Route to add streamer to FavoriteStreamer database"
    user_name = request.form.get('added_user')
    headers = generate_headers()
    streamer_data = get_streamer_data(user_name, headers)
    if streamer_data:
        existing_streamer = FavoriteStreamer.query.filter_by(
                            name=streamer_data['name']).first()
        if not existing_streamer:
            streamer = FavoriteStreamer(
                id=streamer_data['id'],
                url=streamer_data['url'],
                login=streamer_data['login'],
                name=streamer_data['name'],
                description=streamer_data['description'],
                follower_count=format(streamer_data['follower_count'], ","),
                broadcaster_type=streamer_data['broadcaster_type'],
                last_played=streamer_data['last_game_played'],
                created_at=streamer_data['created_at'],
                img_src=streamer_data['pfp_url']
            )
            db.session.add(streamer)
            db.session.commit()
    return redirect(url_for('view_fav'))


@app.route('/remove', methods=['POST'])
def remove():
    "Route to remove a streamer from the FavoriteStreamer database"
    name_to_remove = request.form.get('removed_user')
    streamer = FavoriteStreamer.query.filter_by(name=name_to_remove).first()
    if streamer:
        db.session.delete(streamer)
        db.session.commit()
        streamers = get_streamers('fav')
        return render_template('users.html', streamers=streamers)
    else:
        return redirect(url_for('home'))


@app.route('/view_fav', methods=['GET', 'POST'])
def view_fav():
    return view('fav')


@app.route('/view_pop', methods=['GET', 'POST'])
def view_pop():
    return view('pop')


@app.route('/view', methods=['GET', 'POST'])
def view(streamer_type):
    streamers = get_streamers(streamer_type)
    if streamer_type == 'fav':
        return render_template('users.html', streamers=streamers)
    else:
        return redirect(url_for('home'))


def get_streamers(streamer_type):
    if streamer_type == 'fav':
        streamers = FavoriteStreamer.query.all()
    else:
        streamers = ActiveStreamer.query.all()
    streamer_list = []
    for streamer in streamers:
        streamer_data = {
            'id': streamer.id,
            'url': streamer.url,
            'login': streamer.login,
            'name': streamer.name,
            'description': streamer.description,
            'follower_count': streamer.follower_count,
            'broadcaster_type': streamer.broadcaster_type,
            'last_played': streamer.last_played,
            'created_at': streamer.created_at,
            'img_src': streamer.img_src
        }
        streamer_list.append(streamer_data)
    return streamer_list


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
