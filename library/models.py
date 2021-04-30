from library import db

class Member(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    rent = db.Column(db.Integer(), nullable=True, default=0)
    books = db.relationship('Books', backref='owned_book', lazy=True)

    def __init__(self, name, rent):
        self.name = name
        self.rent = rent

class Books(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=150), nullable=False, unique=True)
    author = db.Column(db.String(length=50), nullable=False, unique=False)
    fee = db.Column(db.Integer(), nullable=False)
    count = db.Column(db.Integer(), nullable=False, default=1)
    owned = db.Column(db.Integer(), db.ForeignKey('member.id'))

    def __init__(self, name, author, fee, count):
        self.name = name
        self.author = author
        self.fee = fee
        self.count = count

    def __repr__(self):
        return f'Books {self.name}'