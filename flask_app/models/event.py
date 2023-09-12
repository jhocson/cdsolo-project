from urllib import request
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from datetime import datetime

class Event:
  db = 'connectable'

  def __init__(self,data):
    self.id = data['id']
    self.name = data['name']
    self.location = data['location']
    self.description = data['description']
    self.slots = data['slots']
    self.attendees = data['attendees']    
    self.date_made = data['date_made']
    self.user_id = data['user_id']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']
    self.creator = None

  # CREATE

  @classmethod
  def create_event(cls,data):
    query = """
    INSERT INTO events (name, location, description, slots, date_made, user_id) 
    VALUES (%(name)s, %(location)s,%(description)s,%(slots)s, %(date_made)s,%(user_id)s)
    ;"""
    return connectToMySQL(cls.db).query_db(query,data)

  @classmethod
  def join_event(cls,data):
    query = """
    INSERT INTO attendees (user_id, event_id) 
    VALUES (%(user_id)s, %(event_id)s)
    ;"""
    return connectToMySQL(cls.db).query_db(query,data)
    

  # READ

  @classmethod
  def get_all(cls, user_id):
    query = """
    SELECT events.*, COUNT(attendees.id) as attendees
    FROM events
    JOIN attendees ON events.id = attendees.event_id
    WHERE attendees.user_id = %(user_id)s
    GROUP BY events.id
    """
    data = {
        "user_id": user_id
    }
    results = connectToMySQL(cls.db).query_db(query, data)
    events = []
    for event in results:
        event['attendees'] = event['attendees']
        events.append(cls(event))
    return events
  
  
  @classmethod
  def get_user_events(cls, user_id):
    query = """
    SELECT events.*, COUNT(attendees.id) as attendees
    FROM events
    LEFT JOIN attendees ON events.id = attendees.event_id
    WHERE events.user_id = %(user_id)s
    GROUP BY events.id
    """  

    data = {
        "user_id": user_id
    }

    results = connectToMySQL(cls.db).query_db(query, data)
    events = []
    for event in results:
        event['attendees'] = event['attendees']
        events.append(cls(event))
    return events

  @classmethod
  def get_attendable_events(cls, user_id):
    query = """
    SELECT events.*, COUNT(attendees.id) as attendees
    FROM events
    LEFT JOIN attendees ON events.id = attendees.event_id
    WHERE events.user_id != %(user_id)s
    GROUP BY events.id
    """  

    data = {
        "user_id": user_id
    }

    results = connectToMySQL(cls.db).query_db(query, data)
    events = []
    for event in results:
        event['attendees'] = event['attendees']
        events.append(cls(event))
    return events



  @classmethod
  def get_one_event(cls, data):
    query = """
    SELECT events.*, COUNT(attendees.id) as attendees
    FROM events
    LEFT JOIN attendees ON events.id = attendees.event_id
    WHERE events.id = %(id)s
    GROUP BY events.id
    """  

    results = connectToMySQL(cls.db).query_db(query, data)
    events = []
    for event in results:
        event['attendees'] = event['attendees']
        events.append(cls(event))
    return events[0]

  @classmethod
  def get_by_id(cls, data):
    events = []
    query = "SELECT * FROM events WHERE user_id = %(id)s;"
    results = connectToMySQL(cls.db).query_db(query, data)
    for row in results:
      events.append(cls(row))
    
    return events

  # UPDATE

  @classmethod
  def update(cls, data):
    query = """
    UPDATE events 
    SET name=%(name)s, location=%(location)s, description=%(description)s, slots=%(slots)s, date_made=%(date_made)s,updated_at=NOW() 
    WHERE id = %(id)s
    ;"""
    return connectToMySQL(cls.db).query_db(query,data)
  
  @classmethod
  def attend(cls, data):
    query = """
    UPDATE events 
    SET attendees = attendees + 1
    WHERE id = %(id)s
    ;"""
    return connectToMySQL(cls.db).query_db(query, data)


  # DELETE

  @classmethod
  def delete(cls, data):
    query = "DELETE FROM events WHERE id = %(id)s;"
    return connectToMySQL(cls.db).query_db(query,data)
  
  @classmethod
  def unjoin_event(cls,data):
    query = """
    DELETE from attendees WHERE user_id 
    = (%(user_id)s ) AND event_id = %(event_id)s 
    ;"""
    return connectToMySQL(cls.db).query_db(query,data)
    


  @staticmethod
  def validate_event( event ):
    is_valid = True
    if len(event['name']) < 3:
      flash("Name must be longer than 2 characters", 'event')
      is_valid = False

    if len(event['location']) < 3:
      flash("Location must be longer than 2 characters", 'event')
      is_valid = False

    if len(event['description']) < 3:
      flash("Description must be longer than 2 characters", 'event')
      is_valid = False

    if int(event['slots']) < 1:
      flash("number of slots must be greater than 0", 'event')
      is_valid = False



    return is_valid