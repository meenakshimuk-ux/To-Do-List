from app import db
from datetime import datetime

PRIORITY_ORDER = {'high': 0, 'medium': 1, 'low': 2}

CATEGORIES = [
    ('general', 'General'),
    ('work', 'Work'),
    ('personal', 'Personal'),
    ('shopping', 'Shopping'),
    ('health', 'Health'),
]


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    done = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(10), default='medium')
    category = db.Column(db.String(20), default='general')
    due_date = db.Column(db.Date, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, content, priority='medium', due_date=None, category='general', notes=None):
        self.content = content
        self.priority = priority
        self.due_date = due_date
        self.category = category
        self.notes = notes

    @property
    def is_overdue(self):
        if self.done or not self.due_date:
            return False
        return self.due_date < datetime.utcnow().date()

    @property
    def is_due_today(self):
        if not self.due_date:
            return False
        return self.due_date == datetime.utcnow().date()

    @property
    def priority_label(self):
        return self.priority.capitalize()

    @property
    def category_label(self):
        labels = dict(CATEGORIES)
        return labels.get(self.category, self.category.capitalize())

    def __repr__(self):
        return f'<Task {self.id}: {self.done}>'
