from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone


db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=True)
    salt = db.Column(db.String(180), nullable=False)
    enterprise_id = db.Column(db.Integer ,db.ForeignKey("enterprises.id"), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now(timezone.utc), nullable=False)

    #relación con enterprises
    enterprise = db.relationship('Enterprises', back_populates='users')
    projects = db.relationship('Projects', back_populates='user')
    tasks = db.relationship('Tasks', back_populates='user')


    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role_id": self.role_id,
            "enterprise_id": self.enterprise_id,
            "created_at": self.created_at
        }

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False)
    description = db.Column(db.String(800), unique=False)
    start_date = db.Column(db.DateTime(), default=datetime.now(timezone.utc), unique=False)
    end_date = db.Column(db.DateTime(), unique=False)
    enterprise_id = db.Column(db.Integer, db.ForeignKey('enterprises.id'), unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=False)

    user = db.relationship('Users', back_populates='projects')
    enterprise = db.relationship('Enterprises', back_populates='projects')
    tasks = db.relationship('Tasks', back_populates='project', cascade='all, delete-orphan')
    members = db.relationship('ProjectMembers', back_populates='project')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "enterprise_id": self.enterprise_id,
            "user_id": self.user_id,
            "progress": self.calculate_progress()
        }
    
    def calculate_progress(self):
        total_tasks = len(self.tasks)
        if total_tasks == 0:
            return 0
        completed_tasks = sum(1 for task in self.tasks if task.status == "Completed")
        return (completed_tasks / total_tasks) * 100

class Enterprises(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(120), nullable=False)

    # Relación con Users
    users = db.relationship('Users', back_populates='enterprise')
    projects = db.relationship('Projects', back_populates='enterprise')

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "address": self.address
        }

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(120), unique=False)
    description = db.Column(db.String(120), unique=False)
    status = db.Column(db.String(120), unique=False)
    due_date = db.Column(db.DateTime(), unique=False)
    creation_date = db.Column(db.DateTime(), default=datetime.now(timezone.utc), unique=False)

    project = db.relationship('Projects', back_populates='tasks')
    user = db.relationship('Users', back_populates='tasks')
    subtasks = db.relationship('Sub_tasks', back_populates='task', cascade='all, delete-orphan')

    def serialize(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "due_date": self.due_date.isoformat(),
            "creation_date": self.creation_date.isoformat()
        }

class Sub_tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), unique=False)
    name = db.Column(db.String(120), unique=False)
    description = db.Column(db.String(120), unique=False)
    status = db.Column(db.String(120), unique=False)
    due_date = db.Column(db.DateTime(), unique=False)
    creation_date = db.Column(db.DateTime(), default=datetime.now(timezone.utc), unique=False)

    task = db.relationship('Tasks', back_populates='subtasks')

    def serialize(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "due_date": self.due_date,
            "creation_date": self.creation_date,
            
        }

class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    
class ProjectMembers(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    project = db.relationship('Projects', back_populates='members')
    user = db.relationship('Users')

    def serialize(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "user_id": self.user_id
        }
