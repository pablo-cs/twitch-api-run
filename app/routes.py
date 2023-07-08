import git
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
try:
    from .twitch_api import generate_headers, get_user_data, get_popular_users, update_sql
except ImportError:
    from twitch_api import generate_headers, get_user_data, get_popular_users, update_sql

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///streamers.db'
app.config['SQLALCHEMY_BINDS'] = {
    'favorites': 'sqlite:///favorites.db',
    'popular': 'sqlite:///popular_users.db'
}
db = SQLAlchemy(app)

class FavoriteStreamer(db.Model):
    __bind_key__ = 'favorites'
    id = db.Column(db.String, primary_key=True)
    url = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    follower_count = db.Column(db.String(120), nullable=False)
    broadcaster_type = db.Column(db.String(20), nullable=False)
    last_played = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.String(120), nullable=False)
    img_src = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"Streamer(id={self.id}, name='{self.name}', follower_count='{self.follower_count}')"

class PopularStreamer(db.Model):
    __bind_key__ = 'popular'
    id = db.Column(db.String, primary_key=True)
    url = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    follower_count = db.Column(db.String(120), nullable=False)
    broadcaster_type = db.Column(db.String(20), nullable=False)
    last_played = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.String(120), nullable=False)
    img_src = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"Streamer(id={self.id}, name='{self.name}', follower_count='{self.follower_count}')"

with app.app_context():
  db.create_all()

def add_pop():
    with app.app_context():
        headers = generate_headers()
        pop_data = get_popular_users(headers)
        for user_data in pop_data:
            if user_data:
                existing_streamer = PopularStreamer.query.filter_by(name=user_data['name']).first()
                if not existing_streamer:
                    streamer = PopularStreamer(
                        id=user_data['id'],
                        url=user_data['url'],
                        name=user_data['name'],
                        description=user_data['description'],
                        follower_count=format(user_data['follower_count'], ","),
                        broadcaster_type=user_data['broadcaster_type'],
                        last_played=user_data['last_game_played'],
                        created_at=user_data['created_at'],
                        img_src=user_data['pfp_url']
                    )
                    db.session.add(streamer)
                    db.session.commit()

add_pop()

@app.route('/')
def home():

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
    if request.form.get('search'):
        user_name = request.form.get('search') 
    headers = generate_headers()
    user_data = get_user_data(user_name, headers)
    if user_data:
        existing_streamer = FavoriteStreamer.query.filter_by(name=user_data['name']).first()
        streamer_exists = bool(existing_streamer)
        videos = user_data['video_data'][:5]
        return render_template('results.html',
                            streamer=user_data['name'],
                            url=user_data['url'],
                            description=user_data['description'],
                            followers=format(user_data['follower_count'], ","),
                            broadcaster_type=user_data['broadcaster_type'],
                            last_played=user_data['last_game_played'],
                            created_at=user_data['created_at'],
                            img_src=user_data['pfp_url'],
                            videos=videos,
                            in_db=streamer_exists)
    else:
        return render_template('results.html', streamer=None, description=None)

@app.route('/add', methods=['POST'])
def add():
    user_name = request.form.get('added_user')
    headers = generate_headers()
    user_data = get_user_data(user_name, headers)
    if user_data:
        existing_streamer = FavoriteStreamer.query.filter_by(name=user_data['name']).first()
        if not existing_streamer:
            streamer = FavoriteStreamer(
                id=user_data['id'],
                url=user_data['url'],
                name=user_data['name'],
                description=user_data['description'],
                follower_count=format(user_data['follower_count'], ","),
                broadcaster_type=user_data['broadcaster_type'],
                last_played=user_data['last_game_played'],
                created_at=user_data['created_at'],
                img_src=user_data['pfp_url']
            )
            db.session.add(streamer)
            db.session.commit()
    return redirect(url_for('view_fav'))

@app.route('/remove', methods=['POST'])
def remove():
    name_to_remove = request.form.get('removed_user')
    streamer = FavoriteStreamer.query.filter_by(name=name_to_remove).first()
    if streamer:
        db.session.delete(streamer)
        db.session.commit()
        streamers = get_streamers('fav')
        return render_template('users.html', streamers=streamers)
    else:
        streamers = get_streamers('pop')
        return render_template('index.html', streamers=streamers)

@app.route('/view_fav', methods=['GET','POST'])
def view_fav():
    return view('fav')

@app.route('/view_pop', methods=['GET','POST'])
def view_pop():
    return view('pop')

@app.route('/view', methods=['GET','POST'])
def view(streamer_type):
    streamers = get_streamers(streamer_type)
    if streamer_type == 'fav':
         return render_template('users.html', streamers=streamers)
    else:
        return render_template('index.html', streamers=streamers)

def get_streamers(streamer_type):
    if streamer_type == 'fav':
        streamers = FavoriteStreamer.query.all()
    else:
        streamers = PopularStreamer.query.all()
    streamer_list = []
    for streamer in streamers:
        streamer_data = {
            'id': streamer.id,
            'url': streamer.url,
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
