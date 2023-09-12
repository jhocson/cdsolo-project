from flask import render_template,request, redirect, flash, session
from flask_app import app
from flask_app.models.event import Event
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# CREATE

@app.route('/event/create', methods=['POST'])
def create_event():
  if 'user_id' not in session:
    return redirect('/logout')
  if not Event.validate_event(request.form):
    return redirect('/event/dashboard')
  data = {
    "name": request.form["name"],
    "location": request.form["location"],
    "description": request.form["description"],
    "slots": int(request.form["slots"]),
    "date_made": request.form["date_made"] + " " + request.form["time_made"] ,
    "user_id": session["user_id"],
  }
  Event.create_event(data)
  return redirect('/dashboard')

@app.route('/join', methods=['POST'])
def join_event():
  if 'user_id' not in session:
      return redirect('/logout')
  data = {
    "event_id": request.form["event_id"],
    "user_id": request.form["user_id"],
  }
  Event.join_event(data)
  return redirect('/dashboard')


# READ
@app.route('/browse')
def event_browse():
  if 'user_id' not in session:
    return redirect('/logout')
  data = {
    'id' : session['user_id']
  }
  return render_template('browse.html', user=User.get_by_id(data), events=Event.get_attendable_events(session['user_id']))

@app.route('/event/dashboard')
def event_dashboard():
  if 'user_id' not in session:
    return redirect('/logout')
  data = {
    'id' : session['user_id']
  }
  return render_template('events_new.html', user=User.get_by_id(data))

@app.route('/event/<int:id>')
def show_event(id):
  if 'user_id' not in session:
    return redirect('/logout')
  data = {
    "id":id
  }
  user_data = {
    "id":session['user_id']
  }
  return render_template("events.html", event=Event.get_one_event(data), user=User.get_by_id(user_data))

# UPDATE

@app.route('/event/update/<int:id>', methods=['POST'])
def update_event(id):
  if 'user_id' not in session:
      return redirect('/logout')
  if not Event.validate_event(request.form):
    return redirect(f'/event/update/form/{id}')  
  data = {
    "name": request.form["name"],
    "location": request.form["location"],
    "description": request.form["description"],
    "slots": int(request.form["slots"]),
    "date_made": request.form["date_made"] + " " + request.form["time_made"] ,
    "id" : id
  }
  Event.update(data)
  return redirect('/dashboard')

@app.route('/event/update/form/<int:id>')
def event_update_form(id):
  if 'user_id' not in session:
    return redirect('/logout')
  data = {
    "id":id
  }
  user_data = {
    "id" : session['user_id']
  }
  return render_template("events_edit.html", event=Event.get_one_event(data), user=User.get_by_id(user_data))

# DELETE

@app.route('/event/delete/<int:id>')
def delete_event(id):
  if 'user_id' not in session:
    return redirect('/logout')
  data = {
    "id" : id
  }
  Event.delete(data)
  return redirect('/dashboard')

@app.route('/unjoin', methods=['POST'])
def unjoin_event():
  if 'user_id' not in session:
      return redirect('/logout')
  data = {
    "event_id": request.form["event_id"],
    "user_id": request.form["user_id"],
  }
  Event.unjoin_event(data)
  return redirect('/dashboard')