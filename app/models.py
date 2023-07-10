from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class FavoriteStreamer(db.Model):
    __bind_key__ = 'favorite'
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
    __bind_key__ = 'active'
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

