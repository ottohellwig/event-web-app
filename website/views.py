from flask import Blueprint, render_template, request, redirect,url_for
from .models import Event
from datetime import datetime

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    events = Event.query.all()    
    return render_template('index.html', events=events)

@mainbp.route('/search')
def search():
    if request.args['search']:
        print(request.args['search'])
        eve = "%" + request.args['search'] + '%'
        # If event name is like the search, display that event 
        events = Event.query.filter(
            Event.name.like(eve)).all()
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.index'))

@mainbp.route('/filter_by_genre', methods=['POST'])
def filter_by_genre():
    selected_genre = request.form.get('genre')
    # If selected genre is equal to event's genre 
    if selected_genre:
        events = Event.query.filter_by(genre=selected_genre).all()
    else:
        events = Event.query.all()
    return render_template('index.html', events=events)

@mainbp.route('/filter_by_location')
def filter_by_location():
    if request.args['location']:
        print(request.args['location'])
        loc = "%" + request.args['location'] + '%'
        # If location is similar to event's location 
        events = Event.query.filter(
            Event.location.like(loc)).all()
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.index'))
    
@mainbp.route('/filter_by_date')
def filter_by_date():
    if request.args['date']:
        try:
            date_str = request.args['date']
            # Format datetime string 
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            date_formatted = date_obj.strftime('%d-%m-%Y')
            print(date_formatted)
            # If datetime is equal to event's datetime
            events = Event.query.filter(Event.date == date_formatted).all()
            return render_template('index.html', events=events)
        except ValueError:
            # Handle invalid date format
            print("Value error")
            return redirect(url_for('main.index'))
    else:
        print ("no args")
        return redirect(url_for('main.index'))

