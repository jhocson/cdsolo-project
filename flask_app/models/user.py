from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from datetime import date
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
  db = 'connectable'
  def __init__(self,data):
    self.id = data['id']
    self.first_name = data['first_name']
    self.last_name = data['last_name']
    self.email = data['email']
    self.password = data['password']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']

  @classmethod
  def save(cls,data):
    query = """INSERT INTO users (first_name,last_name,email,password) 
    VALUES(%(first_name)s,%(last_name)s,%(email)s, %(password)s)
    ;"""
    return connectToMySQL(cls.db).query_db(query,data)

  @classmethod
  def get_all(cls):
    query = "SELECT * FROM users;"
    result = connectToMySQL(cls.db).query_db(query)
    emails = []
    for row in result:
      emails.append(cls(row))
    return result

  @classmethod
  def get_by_email(cls, data):
    query = "SELECT * FROM users WHERE email = %(email)s;"
    results = connectToMySQL(cls.db).query_db(query,data)
    if len(results) < 1:
      return False
    return cls(results[0])

  @classmethod
  def get_by_id(cls,data):
    query = "SELECT * FROM users WHERE id = %(id)s;"
    results = connectToMySQL(cls.db).query_db(query,data)
    return cls(results[0])
  
  @staticmethod
  def validate_user( user ):
    is_valid = True
    query = "SELECT * FROM users WHERE email = %(email)s;"
    results = connectToMySQL('connectable').query_db(query,user)

    if len(user['first_name']) < 2:
      flash("First name must be at least 2 characters","register")
      is_valid= False
    if len(user['last_name']) < 2:
      flash("Last name must be at least 2 characters","register")
      is_valid= False
    if len(results) >= 1:
      flash("Email already taken.","register")
      is_valid=False
    if not EMAIL_REGEX.match(user['email']):
      flash("Invalid Email","register")
      is_valid=False
    if len(user['password']) < 8:
      flash("Password must be at least 8 characters","register")
      is_valid= False
    if user['password'] != user['password_confirm']:
      flash("Passwords don't match","register")
      is_valid= False
    return is_valid


# BACKLOG DOB Validation 
#    born = date(user['dob'])
#    today = date.today()
#    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
#    if age <18:
#      is_valid = False
    # if User.get_by_email(user['email']):
    #   flash('this email is already in use!', "register")
    #   is_valid = False
#    return is_valid
  
#  @staticmethod
#  def calculate_age(born):
#    today = date.today()
#    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))