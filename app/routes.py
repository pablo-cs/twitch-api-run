from flask import Flask, render_template, request
from .twitch_api import generate_headers, get_user_data, update_sql

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    user_name = request.form.get('search') 
    headers = generate_headers()
    user_data = get_user_data(user_name, headers)
    if user_data:
        videos = user_data['video_data'][:5]
        return render_template('results.html',
                            streamer=user_data['name'],
                            description=user_data['description'],
                            followers=format(user_data['follower_count'], ","),
                            broadcaster_type=user_data['broadcaster_type'],
                            last_played=user_data['last_game_played'],
                            created_at=user_data['created_at'],
                            img_src=user_data['pfp_url'],
                            videos=videos)
    else:
        return render_template('results.html', streamer=None, description=None)

@app.route('/add', methods=['POST'])
def add():
    user_name = request.form.get('search')
    headers = generate_headers()
    user_data = get_user_data(user_name, headers)
    if user_data:
        
        update_sql([user_data])
        return render_template('add.html', user_data=user_data)
    else:
        return render_template('add.html', user_data=None)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
