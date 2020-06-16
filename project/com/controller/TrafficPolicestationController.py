import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template, request, redirect, url_for

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.AreaDAO import AreaDAO
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.TrafficPoliceStationDAO import TrafficPoliceStationDAO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.TrafficPoliceStationVO import TrafficPoliceStationVO


@app.route('/admin/loadTrafficPoliceStation', methods=['GET'])
def adminLoadRegister():
    try:
        if adminLoginSession() == 'admin':
            areaDAO = AreaDAO()
            areaVOList = areaDAO.viewArea()
            return render_template("admin/addTrafficPoliceStation.html", areaVOList=areaVOList)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertTrafficPoliceStation', methods=['post'])
def adminInsertRegister():
    try:
        if adminLoginSession() == 'admin':
            loginVO = LoginVO()
            loginDAO = LoginDAO()
            trafficPoliceStationVO = TrafficPoliceStationVO()
            trafficPoliceStationDAO = TrafficPoliceStationDAO()

            trafficPoliceStationUsername = request.form['trafficPoliceStationUsername']
            trafficPoliceStationName = request.form['trafficPoliceStationName']
            trafficPoliceStation_AreaId = request.form['trafficPoliceStation_AreaId']
            trafficPoliceStationAddress = request.form['trafficPoliceStationAddress']
            trafficPoliceStationContact = request.form['trafficPoliceStationContact']

            loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))


            sender = "sharshil07@gmail.com"

            receiver = trafficPoliceStationUsername

            msg = MIMEMultipart()

            msg['From'] = sender

            msg['To'] = receiver

            msg['Subject'] = "TRAFFIC POLICE STATION LOGIN PASSWORD"

            msg.attach(MIMEText(loginPassword, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender, "harshil3632")

            text = msg.as_string()

            server.sendmail(sender, receiver, text)

            loginVO.loginUsername = trafficPoliceStationUsername
            loginVO.loginPassword = loginPassword
            loginVO.loginRole = "user"
            loginVO.loginStatus = "active"
            loginVOList = loginDAO.insertLogin(loginVO)
            loginDictList = [i.as_dict() for i in loginVOList]

            trafficPoliceStationVO.trafficPoliceStationName = trafficPoliceStationName
            trafficPoliceStationVO.trafficPoliceStationContact = trafficPoliceStationContact
            trafficPoliceStationVO.trafficPoliceStationAddress = trafficPoliceStationAddress
            trafficPoliceStationVO.trafficPoliceStation_AreaId = int(trafficPoliceStation_AreaId)
            trafficPoliceStationVO.trafficPoliceStation_LoginId = loginDictList[0]['loginId']

            trafficPoliceStationDAO.insertTrafficPoliceStation(trafficPoliceStationVO)
            server.quit()
            return redirect(url_for('adminViewTrafficPoliceStation'))
        else:
            adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/viewTrafficPoliceStation', methods=['get'])
def adminViewTrafficPoliceStation():
    try:

        trafficPoliceStationDAO = TrafficPoliceStationDAO()
        trafficPoliceStationVOList = trafficPoliceStationDAO.viewTrafficPoliceStation()
        return render_template('admin/viewTrafficPoliceStation.html',
                               trafficPoliceStationVOList=trafficPoliceStationVOList)
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteTrafficPoliceStation', methods=['get'])
def adminDeleteTrafficPoliceStation():
    try:
        if adminLoginSession() == 'admin':
            trafficPoliceStationId = request.args.get('trafficPoliceStationId')
            trafficPoliceStation_LoginId = request.args.get('trafficPoliceStation_LoginId')

            trafficPoliceStationVO = TrafficPoliceStationVO()
            trafficPoliceStationDAO = TrafficPoliceStationDAO()
            loginVO = LoginVO()
            loginDAO = LoginDAO()

            trafficPoliceStationVO.trafficPoliceStationId = trafficPoliceStationId
            loginVO.loginId = trafficPoliceStation_LoginId

            trafficPoliceStationDAO.deleteTrafficPoliceStation(trafficPoliceStationVO)
            loginDAO.deleteLogin(loginVO)
            return redirect(url_for('adminViewTrafficPoliceStation'))
        else:
            adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/editTrafficPoliceStation')
def adminEditTrafficPoliceStation():
    try:
        if adminLoginSession() == 'admin':
            trafficPoliceStationVO = TrafficPoliceStationVO()
            trafficPoliceStationDAO = TrafficPoliceStationDAO()
            loginVO = LoginVO()
            loginDAO = LoginDAO()
            areaDAO = AreaDAO()

            trafficPoliceStationId = request.args.get('trafficPoliceStationId')
            trafficPoliceStation_LoginId = request.args.get('trafficPoliceStation_LoginId')

            trafficPoliceStationVO.trafficPoliceStationId = trafficPoliceStationId
            loginVO.loginId = trafficPoliceStation_LoginId

            trafficPoliceStationVOList = trafficPoliceStationDAO.editTrafficPoliceStation(trafficPoliceStationVO)
            loginVOList = loginDAO.editLogin(loginVO)
            areaVOList = areaDAO.viewArea()

            return render_template('admin/editTrafficPoliceStation.html',
                                   trafficPoliceStationVOList=trafficPoliceStationVOList, areaVOList=areaVOList,
                                   loginVOList=loginVOList)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/updateTrafficPoliceStation', methods=['post'])
def adminUpdateTrafficPoliceStation():
    try:
        if adminLoginSession() == 'admin':
            trafficPoliceStationId = request.form['trafficPoliceStationId']
            trafficPoliceStationUsername = request.form['trafficPoliceStationUsername']
            trafficPoliceStationName = request.form['trafficPoliceStationName']
            trafficPoliceStation_AreaId = request.form['trafficPoliceStation_AreaId']
            trafficPoliceStationAddress = request.form['trafficPoliceStationAddress']
            trafficPoliceStationContact = request.form['trafficPoliceStationContact']
            trafficPoliceStation_LoginId = request.form['trafficPoliceStation_LoginId']

            trafficPoliceStationVO = TrafficPoliceStationVO()
            trafficPoliceStationDAO = TrafficPoliceStationDAO()

            loginVO = LoginVO()
            loginDAO = LoginDAO()

            loginVO.loginId = trafficPoliceStation_LoginId
            loginVOList = loginDAO.registerLogin(loginVO)
            loginDictList = [i.as_dict() for i in loginVOList]

            loginVO.loginId = loginDictList[0]['loginId']
            loginVO.loginUsername = trafficPoliceStationUsername
            loginVO.loginPassword = loginDictList[0]['loginPassword']
            loginVO.loginStatus = loginDictList[0]['loginStatus']
            loginVO.loginRole = loginDictList[0]['loginRole']
            loginDAO.updateLogin(loginVO)
            trafficPoliceStationVO.trafficPoliceStationId = trafficPoliceStationId
            trafficPoliceStationVO.trafficPoliceStationName = trafficPoliceStationName
            trafficPoliceStationVO.trafficPoliceStationAddress = trafficPoliceStationAddress
            trafficPoliceStationVO.trafficPoliceStationContact = trafficPoliceStationContact
            trafficPoliceStationVO.trafficPoliceStation_AreaId = trafficPoliceStation_AreaId
            trafficPoliceStationVO.trafficPoliceStation_LoginId = trafficPoliceStation_LoginId
            trafficPoliceStationDAO.updateTrafficPoliceStation(trafficPoliceStationVO)

            return redirect(url_for('adminViewTrafficPoliceStation'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)
