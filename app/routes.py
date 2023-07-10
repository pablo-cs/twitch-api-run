import git
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from flask_behind_proxy import FlaskBehindProxy
try:
    from .twitch_api import (
        generate_headers,
        get_streamer_data,
        get_active_streamers
    )
    from .models import db, FavoriteStreamer, ActiveStreamer
except ImportError:
    from twitch_api import (
        generate_headers,
        get_streamer_data,
        get_active_streamers
    )
    from models import db, FavoriteStreamer, ActiveStreamer
from helpers import add_pop, get_streamers

def home():
    add_pop()
    return render_template('index.html', streamers=get_streamers('pop'))


def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/pcrisostomosuarez/twitch-api-run')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


def search():
    # Route to search for a streamer using Twitch API
    user_name = request.form.get('search')
    if user_name:
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
                    in_db=streamer_exists
                )
    return render_template('results.html', streamer=None, description=None)


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


def view_fav():
    return view('fav')


def view_pop():
    return view('pop')


def view(streamer_type):
    streamers = get_streamers(streamer_type)
    if streamer_type == 'fav':
        return render_template('users.html', streamers=streamers)
    else:
        return redirect(url_for('home'))
