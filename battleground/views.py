from battleground import app
from battleground.database import *
from flask import (
    render_template,
    redirect,
    request,
    url_for
)
from wartanker import *
from datetime import date, datetime, timedelta

@app.route('/')
def home():
    today = date.today()
    base_data = {'labels': [], 'base16': [], 'base32': [], 'base64': []}
    base_data['labels'] = list(reversed([(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(0, 7)]))
    for label in base_data['labels']:
        for topic in ['base16', 'base32', 'base64']:
            base_data[topic].append(len(Log.query.filter_by(
                timestamp=label, 
                type=topic
            ).all()))
    return render_template('index.html', base_data=base_data)

@app.route('/decode/base', methods=['GET', 'POST'])  
def base_decode():
    if request.method == 'POST':
        try:
            query = request.form.get('enc')
            result, base = crypto.base_decode(query, question_base=True)
        except crypto.UnknownBaseError:
            return 'Unknown base'
        newlog = Log(
            type='base' + str(base),
            timestamp=datetime.now().strftime('%Y-%m-%d'),
            json={ 'query': query, 'result': result }
        )
        db.session.add(newlog)
        db.session.commit()
        return str((result, base))
    return render_template('decode/base.html')
