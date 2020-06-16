from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.CameraVO import CameraVO
from project.com.vo.CrossroadVO import CrossroadVO
from project.com.vo.LoginVO import LoginVO


class VideoVO(db.Model):
    __tablename__ = "videomaster"
    videoId = db.Column('videoId', db.Integer, primary_key=True, autoincrement=True)
    video_LoginId = db.Column('video_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))
    video_AreaId = db.Column('video_AreaId', db.Integer, db.ForeignKey(AreaVO.areaId))
    video_CrossroadId = db.Column('video_CrossroadId', db.Integer, db.ForeignKey(CrossroadVO.crossroadId))
    video_CameraId = db.Column('video_CameraId', db.Integer, db.ForeignKey(CameraVO.cameraId))
    inputVideoFilename = db.Column('inputVideoFilename', db.String(100))
    inputVideoFilePath = db.Column('inputVideoFilePath', db.String(1000))
    uploadDate = db.Column('uploadDate', db.Date)
    uploadTime = db.Column('uploadTime', db.Time)
    outputVideoFilename = db.Column('outputVideoFilename', db.String(100))
    outputVideoFilePath = db.Column('outputVideoFilePath', db.String(1000))
    illegalCarCount = db.Column('illegalCarCount', db.Integer)
    legalCarCount = db.Column('legalCarCount', db.Integer)
    def as_dict(self):
        return {
            'videoId': self.videoId,
            'video_LoginId': self.video_LoginId,
            'video_AreaId': self.video_AreaId,
            'video_CrossroadId': self.video_CrossroadId,
            'video_CameraId': self.video_CameraId,
            'inputVideoFilename': self.inputVideoFilename,
            'inputVideoFilePath': self.inputVideoFilePath,
            'uploadDate': self.uploadDate,
            'uploadTime': self.uploadTime,
            'outputVideoFilename': self.outputVideoFilename,
            'outputVideoFilePath': self.outputVideoFilePath,
            'illegalCarCount': self.illegalCarCount,
            'legalCarCount': self.legalCarCount
        }


db.create_all()
