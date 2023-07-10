from flask import current_app
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


def add_pop():
    """
    Adds the currently active streamers to the ActiveStreamer database
    """
    with current_app.app_context():
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


def get_streamers(streamer_type):
    """
    Gets the streamers from a given database and return
    as a list of dictionaries
    """
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
