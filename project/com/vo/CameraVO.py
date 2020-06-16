from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.CrossroadVO import CrossroadVO


class CameraVO(db.Model):
    __tablename__ = 'cameramaster'
    cameraId = db.Column('cameraId', db.Integer, primary_key=True, autoincrement=True)
    cameraCode = db.Column('cameraCode', db.Integer)
    camera_AreaId = db.Column('camera_AreaId', db.Integer, db.ForeignKey(AreaVO.areaId))
    camera_CrossroadId = db.Column('camera_CrossroadId', db.Integer, db.ForeignKey(CrossroadVO.crossroadId))
    x1 = db.Column('x1', db.Integer)
    y1 = db.Column('y1', db.Integer)
    x2 = db.Column('x2', db.Integer)
    y2 = db.Column('y2', db.Integer)

    def as_dict(self):
        return {
            'cameraId': self.cameraId,
            'cameraCode': self.cameraCode,
            'camera_AreaId': self.camera_AreaId,
            'camera_CrossroadId': self.camera_CrossroadId,
            'x1': self.x1,
            'y1': self.y1,
            'x2': self.x2,
            'y2': self.y2
        }


db.create_all()
