class Config:
    SECRET_KEY = '91062784e313e6292e50dfe09b0ea33e'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///streamers.db'
    SQLALCHEMY_BINDS = {
        'favorite': 'sqlite:///favorite.db',
        'active': 'sqlite:///active.db'
    }
    CACHE_TYPE = 'simple'
