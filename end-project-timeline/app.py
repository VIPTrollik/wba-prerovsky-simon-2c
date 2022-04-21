import imp
import flask as fl
import os
import json
import datetime
from dataclasses import dataclass, asdict
from secrets import token_urlsafe

os.environ['FLASK_ENV'] = "development"

app = fl.Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@dataclass
class TimelineItem:
    time: datetime.datetime
    content: str
    title: str
    id: str

#parses timeline data from json file
def load_timeline_json():
    with open('timeline.json') as json_file:
        data = json.load(json_file)
    for item in data:
        item["time"] = datetime.datetime.fromisoformat(item["time"])
    return [TimelineItem(**item) for item in data]
    
#saves timeline to json and converts "time" to isoformat
def save_timeline_json(data):
    data = [asdict(item) for item in data]
    for item in data:
        item["time"] = item["time"].isoformat()
    with open('timeline.json', 'w') as json_file:
        json.dump(data, json_file)

timeline_data = load_timeline_json()



@app.route('/')
def index():
    return fl.render_template('index.html', timeline_items=timeline_data, curr_time = datetime.datetime.now(), tlen = len(timeline_data))


@app.route("/newTimelineItem", methods=['POST'])
def timelinepostroute():
    title = fl.request.form['title']
    content = fl.request.form['content']
    time = fl.request.form['time']
    print(title, content, time)
    if time and content and title:
        timeline_data.append(TimelineItem(datetime.datetime.fromisoformat(time), content, title, token_urlsafe(16)))
        timeline_data.sort(key=lambda x: x.time, reverse=False)
        save_timeline_json(timeline_data)
        return fl.redirect('/')
    return "error", 400
            
@app.route("/deletetimelineitem/<id>", methods=['POST'])
def deletetimelineitem(id):
    if id:
        for item in timeline_data:
            if item.id == id:
                timeline_data.remove(item)
                save_timeline_json(timeline_data)
                return fl.redirect('/')
    return "error", 400

#timeline items:
# {title: "", time: datetime, content: htmlcontent}