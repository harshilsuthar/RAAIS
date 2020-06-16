from sqlalchemy import desc

from project import db
from project.com.vo.LoginVO import LoginVO


class LoginDAO:
    def validateLogin(self, loginVO):
        loginList = LoginVO.query.filter_by(loginUsername=loginVO.loginUsername,
                                            loginPassword=loginVO.loginPassword,
                                            loginStatus=loginVO.loginStatus)
        return loginList

    def insertLogin(self, loginVO):
        db.session.add(loginVO)
        db.session.commit()
        loginList = [LoginVO.query.order_by(desc(LoginVO.loginId)).first()]
        return loginList

    def viewLogin(self):
        loginList = LoginVO.query.all()
        return loginList

    def registerLogin(self, loginVO):
        loginList = LoginVO.query.filter_by(loginId=loginVO.loginId)
        return loginList

    def deleteLogin(self, loginVO):
        loginVOList = LoginVO.query.get(loginVO.loginId)
        db.session.delete(loginVOList)
        db.session.commit()

    def editLogin(self, loginVO):
        loginList = LoginVO.query.filter_by(loginId=loginVO.loginId).all()
        return loginList

    def updateLogin(self, loginVO):
        db.session.merge(loginVO)
        db.session.commit()

    def checkUsername(self, loginVO):
        loginList = LoginVO.query.filter_by(loginUsername=loginVO.loginUsername).all()
        return loginList
