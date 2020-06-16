from project import db
from project.com.controller.LoginController import session
from project.com.vo.AreaVO import AreaVO
from project.com.vo.CameraVO import CameraVO
from project.com.vo.CrossroadVO import CrossroadVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.TrafficPoliceStationVO import TrafficPoliceStationVO
from project.com.vo.VideoVO import VideoVO


class VideoDAO:
    def insertVideo(self, videoVO):
        db.session.add(videoVO)
        db.session.commit()

    def adminViewVideo(self):
        videoList = db.session.query(VideoVO, LoginVO, AreaVO, CrossroadVO, CameraVO). \
            join(LoginVO, VideoVO.video_LoginId == LoginVO.loginId). \
            join(AreaVO, AreaVO.areaId == VideoVO.video_AreaId). \
            join(CrossroadVO, CrossroadVO.crossroadId == VideoVO.video_CrossroadId). \
            join(CameraVO, CameraVO.cameraId == VideoVO.video_CameraId).all()
        return videoList

    def deleteVideo(self, videoVO):
        videoList = VideoVO.query.get(videoVO.videoId)
        db.session.delete(videoList)
        db.session.commit()

        return videoList

    def viewLocalData(self):
        videoList = db.session.query(CameraVO, CrossroadVO). \
            join(CrossroadVO, CrossroadVO.crossroadId == CameraVO.camera_CrossroadId). \
            filter(CameraVO.camera_AreaId == TrafficPoliceStationVO.trafficPoliceStation_AreaId). \
            filter(TrafficPoliceStationVO.trafficPoliceStation_LoginId == session['session_LoginId']).all()
        return videoList

    def userViewVideo(self):
        videoList = db.session.query(VideoVO, AreaVO, CrossroadVO, CameraVO). \
            join(AreaVO, AreaVO.areaId == VideoVO.video_AreaId). \
            join(CrossroadVO, CrossroadVO.crossroadId == VideoVO.video_CrossroadId). \
            join(CameraVO, CameraVO.cameraId == VideoVO.video_CameraId). \
            filter(VideoVO.video_LoginId == session['session_LoginId']).all()
        return videoList

    def ajaxDateAdminIndex(self, videoVO):
        videoList = VideoVO.query \
            .filter_by(video_LoginId=videoVO.video_LoginId).all()
        return videoList

    def ajaxGetGraphData(self, videoVO):
        videoList = VideoVO.query \
            .filter_by(videoId=videoVO.videoId).all()
        return videoList
