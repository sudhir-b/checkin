from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    devices = db.relationship(
        "Device", backref="owner", lazy="dynamic", cascade="all, delete, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.name}>"


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    mac_addr = db.Column(db.String(17), index=True, unique=True)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    last_known_ip = db.Column(db.String(46))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Device {self.name}>"

