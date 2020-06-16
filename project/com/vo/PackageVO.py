from project import db


class PackageVO(db.Model):
    __tablename__ = 'packagemaster'
    packageId = db.Column('packageId', db.Integer, primary_key=True, autoincrement=True)
    packageName = db.Column('packageName', db.String(100))
    packagePrice = db.Column('packagePrice', db.Integer)
    packageDuration = db.Column('packageDuration', db.String(100))

    def as_dict(self):
        return {
            'packageId': self.packageId,
            'packageName': self.packageName,
            'packagePrice': self.packagePrice,
            'packageDuration': self.packageDuration
        }


db.create_all()
