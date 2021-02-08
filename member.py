from settings import *
import json


db = SQLAlchemy(app)


class Member(db.Model):
    __tablename__ = 'members'

    _id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    def json(self):
        return {
            'id': self._id,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }

    def get_members():
        return [Member.json(member) for member in Member.query.all()]

    def get_member(_id):
        return [Member.json(Member.query.filter_by(_id=_id).first())]

    def add_member(first_name, last_name):
        new_member = Member(first_name=first_name, last_name=last_name)
        db.session.add(new_member)
        db.session.commit()

    def update_member(_id, first_name, last_name):
        member_to_update = Member.query.filter_by(_id=_id).first()

        if first_name:
            member_to_update.first_name = first_name
        if last_name:
            member_to_update.last_name = last_name

        db.session.commit()

    def delete_member(_id):
        Member.query.filter_by(_id=_id).delete()
        db.session.commit()
        

    