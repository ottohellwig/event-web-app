from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event, Comment, Book
from .forms import EventForm, CommentForm
from . import db, app
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from datetime import datetime, time

bp = Blueprint('event', __name__, url_prefix='/events')

# ID
@bp.route('/<id>')
def show(id):
    event = Event.query.filter_by(id=id).first()
    cform = CommentForm()
    ticket_count = 0
    return render_template('showEvent.html', event=event, form=cform, ticket_count=ticket_count)

# Event creation
@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = EventForm()
    if form.validate_on_submit():
        try:
            db_file_path = check_upload_file(form)
            event_date = datetime.strptime(form.date.data, '%d-%m-%Y').strftime('%d-%m-%Y')
            # Create new event object 
            event = Event(
                name=form.name.data,
                description=form.description.data,
                image=db_file_path,
                location=form.location.data,
                genre=form.genre.data,
                artist=form.artist.data,
                date=event_date,
                ticket_price=form.ticket_price.data,
                number_of_tickets=form.number_of_tickets.data,
                user_id=current_user.id  # Assign the user_id
            )
            db.session.add(event)
            # Commit to the DB
            db.session.commit()
            flash('Event created successfully', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            flash('An error occurred while creating the event. Please try again later.', 'danger')
            app.logger.error(f'Error creating event: {str(e)}')

    return render_template('createEvent.html', form=form)

# Image file upload checker
def check_upload_file(form):
    fp = form.image.data
    filename = fp.filename
    BASE_PATH = os.path.dirname(__file__)
    upload_path = os.path.join(
        BASE_PATH, 'static/images/', secure_filename(filename))
    db_upload_path = 'static/images/' + secure_filename(filename)
    fp.save(upload_path)
    return db_upload_path

# Event commenting
@bp.route('/<event>/comment', methods=['GET', 'POST'])
@login_required
def comment(event):
    form = CommentForm()
    event_obj = Event.query.filter_by(id=event).first()
    if form.validate_on_submit():
        try:
            # Create a new comment object 
            comment = Comment(text=form.text.data,
                              event=event_obj,
                              user=current_user)
            db.session.add(comment)
            db.session.commit()

            flash('Your comment has been added', 'success')
        except Exception as e:
            flash('An error occurred while adding your comment. Please try again later.', 'danger')
            app.logger.error(f'Error adding comment: {str(e)}')

    return redirect(url_for('event.show', id=event))


# Event booking
@bp.route('/<event>/book', methods=['GET', 'POST'])
@login_required
def book(event):
    event_obj = Event.query.filter_by(id=event).first()

    # Extract the number of tickets from the request
    number_of_bought_tickets = int(request.args.get('number_of_tickets'))
    total_cost = float(request.args.get('total_cost'))

    current_number_of_tickets = event_obj.number_of_tickets

    if current_number_of_tickets >= number_of_bought_tickets:
        # Update the number of tickets in the event table
        event_obj.number_of_tickets = current_number_of_tickets - number_of_bought_tickets
        if event_obj.number_of_tickets == 0:
            event_obj.status = 'SOLD OUT'
        db.session.commit()

        # Create the booking record
        booking = Book(
            number_of_tickets=number_of_bought_tickets,
            user_id=current_user.id,
            event_id=event_obj.id,
            total_cost=total_cost
        )
        db.session.add(booking)
        db.session.commit()

        flash('You have successfully booked this event', 'success')
        return redirect(url_for('event.show', id=event_obj.id))
    else:
        flash('You cannot purchase more tickets than available', 'error')
        return redirect(url_for('event.show', id=event_obj.id))

# Booking history
@bp.route('/bookings')
@login_required
def bookings():
    try:
        bookings = Book.query.filter_by(user_id=current_user.id).all()
        return render_template('bookings.html', bookings=bookings)
    except Exception as e:
        flash('An error occurred while retrieving your bookings. Please try again later.', 'danger')
        app.logger.error(f'Error retrieving user bookings: {str(e)}')
        return redirect(url_for('home'))

# My events 
@bp.route('/my-events')
@login_required
def my_events():
    try:
        user_events = Event.query.filter_by(user_id=current_user.id).all()
        return render_template('myEvents.html', events=user_events)
    except Exception as e:
        flash('An error occurred while retrieving your events. Please try again later.', 'danger')
        app.logger.error(f'Error retrieving user events: {str(e)}')
        return redirect(url_for('home'))

@bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Update event
@bp.route('/update/<id>', methods=['GET', 'POST'])
@login_required
def update(id):
    event = Event.query.get_or_404(id)
    form = EventForm()

    if current_user.id != event.user_id:
        flash('You are not authorized to update this event', 'danger')
        return redirect(url_for('event.my_events'))

    if form.validate_on_submit():
        db_file_path = check_upload_file(form)
        event.name = form.name.data
        event.location = form.location.data
        event.genre = form.genre.data
        event.artist = form.artist.data
        event.date = form.date.data
        event.description = form.description.data
        event.image = db_file_path
        event.ticket_price = form.ticket_price.data
        event.number_of_tickets = form.number_of_tickets.data
        db.session.commit()
        flash('Event updated successfully', 'success')
        return redirect(url_for('event.show', id=id))
    else:
        flash('Failed to update event. Please check the form for errors.', 'danger')

    return render_template('updateEvent.html', form=form, event=event)


# Delete event
@bp.route('/delete/<id>', methods=['POST'])
@login_required
def delete(id):
    event = Event.query.get_or_404(id)
    if event:
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted successfully', 'success')
    else:
        flash('Event not found', 'error')
    return redirect(url_for('event.my_events'))

# Cancel event
@bp.route('/cancel/<id>', methods=['POST'])
@login_required
def cancel_event(id):
    event = Event.query.filter(Event.id == id).first()
    if event:
        event.status = 'CANCELLED'
        db.session.commit()
        flash('Event cancelled successfully', 'success')
    else:
        flash('Event not found', 'error')
    return redirect(url_for('event.my_events'))

