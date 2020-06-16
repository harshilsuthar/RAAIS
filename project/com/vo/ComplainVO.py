from project import db
from project.com.vo.LoginVO import LoginVO


class ComplainVO(db.Model):
    __tablename__ = 'complainmaster'

    complainId = db.Column('complainId', db.Integer, primary_key=True, autoincrement=True)
    complainSubject = db.Column('complainSubject', db.String(100))
    complainDescription = db.Column('complainDescription', db.String(500))
    complainDate = db.Column('complainDate', db.Date)
    complainTime = db.Column('complainTime', db.Time)
    complainFilename = db.Column('complainFilename', db.String(500))
    complainFilePath = db.Column('complainFilePath', db.String(1000))
    complainStatus = db.Column('complainStatus', db.String(100))
    replysubject = db.Column('replysubject', db.String(100))
    replyDescription = db.Column('replyDescription', db.String(500))
    replyFilename = db.Column('replyFilename', db.String(500))
    replyFilePath = db.Column('replyFilePath', db.String(500))
    replyDate = db.Column('replyDate', db.Date)
    replyTime = db.Column('replyTime', db.Time)
    complainFrom_LoginId = db.Column('complainFrom_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))
    complainTo_LoginId = db.Column('complainTo_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'complainId': self.complainId,
            'complainSubject': self.complainSubject,
            'complainDescription': self.complainDescription,
            'complainDate': self.complainDate,
            'complainTime': self.complainTime,
            'complainFilename': self.complainFilename,
            'complainFilePath': self.complainFilePath,
            'complainStatus': self.complainStatus,
            'replysubject': self.replysubject,
            'replyDescription': self.replyDescription,
            'replyFilename': self.replyFilename,
            'replyFilePath': self.replyFilePath,
            'replyDate': self.replyDate,
            'replyTime': self.replyTime,
            'complainFrom_LoginId': self.complainFrom_LoginId,
            'complainTo_LoginId': self.complainTo_LoginId
        }


db.create_all()
