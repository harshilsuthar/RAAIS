import logging
import math
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import request, render_template, session, redirect, url_for

from project import app
from project.com.dao.AreaDAO import AreaDAO
from project.com.dao.CameraDAO import CameraDAO
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.dao.FeedbackDAO import FeedbackDAO
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.TrafficPoliceStationDAO import TrafficPoliceStationDAO
from project.com.vo.LoginVO import LoginVO


@app.route('/')
def adminLoadLogin():
    try:
        session.clear()
        return render_template('admin/login.html')
    except Exception as ex:
        print(ex)


@app.route('/admin/validateLogin', methods=['post'])
def adminValidateLogin():
    try:
        loginUsername = request.form['loginUsername']
        loginPassword = request.form['loginPassword']

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword
        loginVO.loginStatus = 'active'

        loginVOList = loginDAO.validateLogin(loginVO)

        loginDictList = [i.as_dict() for i in loginVOList]

        if len(loginDictList) == 0:
            msg = 'username or password is incorrent !'
            return render_template('admin/login.html', msg=msg)

        else:
            for row in loginDictList:
                loginId = row['loginId']
                loginUsername = row['loginUsername']
                loginRole = row['loginRole']

                session['session_LoginId'] = loginId
                session['session_LoginUsername'] = loginUsername
                session['session_LoginRole'] = loginRole
                session['session_LoginPassword'] = loginPassword

                session.permenent = True
                if loginRole == 'user':
                    return redirect(url_for('userLoadDashboard'))
                if loginRole == 'admin':
                    return redirect(url_for('adminLoadDashboard'))
    except Exception as ex:
        print(ex)


@app.route('/admin/loadDashboard')
def adminLoadDashboard():
    try:
        if adminLoginSession() == 'admin':
            feedbackDAO = FeedbackDAO()
            feedbackCount = feedbackDAO.adminFeedbackCount()

            complainDAO = ComplainDAO()
            complainCount = complainDAO.adminComplainCount()

            areaDAO = AreaDAO()
            areaCount = areaDAO.adminAreaCount()

            cameraDAO = CameraDAO()
            camaraCount = cameraDAO.adminCameraCount()

            trafficPoliceStationDAO = TrafficPoliceStationDAO()
            trafficPoliceStationVOList = trafficPoliceStationDAO.viewTrafficPoliceStation()
            print('TPSL >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ', trafficPoliceStationVOList)
            return render_template('admin/index.html', trafficPoliceStationVOList=trafficPoliceStationVOList,
                                   feedbackCount=feedbackCount,complainCount=complainCount, areaCount=areaCount,
                                   camaraCount=camaraCount)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/loadDashboard')
def userLoadDashboard():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/index.html')
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/loginSession')
def adminLoginSession():
    try:
        if 'session_LoginId' and 'session_LoginRole' in session:

            if session['session_LoginRole'] == 'admin':

                return 'admin'

            elif session['session_LoginRole'] == 'user':

                return 'user'

        else:
            return False
    except Exception as ex:
        print(ex)


@app.route("/admin/logoutSession", methods=['GET'])
def adminLogoutSession():
    session.clear()
    try:
        logging.basicConfig(filename=r"project/static/adminResources/log/logfilename.log", level=logging.info,
                            format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    except Exception as ex:
        print(ex)
    return redirect('/')


@app.route("/admin/loadForgotPassword", methods=['GET'])
def adminLoadForgotPassword():
    return render_template('admin/addForgetPassword.html')


@app.route("/admin/checkUsername", methods=['POST'])
def adminLoadUsername():
    username = request.form['username']
    session['session_Username'] = username
    loginVO = LoginVO()
    loginDAO = LoginDAO()

    loginVO.loginUsername = username
    loginVOList = loginDAO.checkUsername(loginVO)
    if len(loginVOList) == 1:
        session['session_LoginId'] = loginVOList[0].loginId
        return redirect(url_for('adminloadOTP'))
    else:
        return render_template('admin/addForgetPassword.html', msg='Invalid Username')


@app.route("/admin/loadOTP")
def adminloadOTP():
    username = session['session_Username']
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    session['session_OTP'] = OTP

    sender = "sharshil07@gmail.com"
    receiver = str(username)

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "TRAFFIC POLICE STATION OTP"
    msg.attach(MIMEText(OTP, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, "harshil3632")
    text = msg.as_string()
    server.sendmail(sender, receiver, text)
    return render_template('admin/addOTP.html')


@app.route("/admin/checkOTP", methods=['POST'])
def adminCheckOTP():
    OTP = request.form['OTP']
    if OTP == session['session_OTP']:
        return redirect(url_for('adminResetPassword'))
    else:
        return render_template('admin/addOTP.html', msg="Wrong OTP")


@app.route('/admin/loadResetPassword')
def adminResetPassword():
    return render_template('admin/resetPassword.html')


@app.route('/admin/updatePassword', methods=['POST'])
def adminUpdatePassword():
    loginVO = LoginVO()
    loginDAO = LoginDAO()
    password1 = request.form['password1']
    password2 = request.form['password2']

    if password1 == password2:
        loginVO.loginId = session['session_LoginId']
        loginVO.loginPassword = password1
        loginDAO.updateLogin(loginVO)
        return render_template('admin/login.html', msg="Password Reset")
    else:
        return render_template('admin/resetPassword.html', msg="Password Mismatch")


@app.route('/user/loadResetPassword')
def userResetPassword():
    if adminLoginSession() == 'user':
        return render_template('user/resetPassword.html')
    else:
        adminLogoutSession()


@app.route('/user/checkPassword', methods=['post'])
def userCheckPassword():
    if adminLoginSession() == 'user':
        oldPassword = request.form['oldPassword']
        newPassword1 = request.form['newPassword1']
        newPassword2 = request.form['newPassword2']
        loginVO = LoginVO()
        loginDAO = LoginDAO()
        if oldPassword == session['session_LoginPassword']:
            if newPassword1 == newPassword2:
                loginVO.loginId = session['session_LoginId']
                loginVO.loginPassword = newPassword1
                loginDAO.updateLogin(loginVO)
                return render_template('admin/login.html', msg="Password Reset")
            else:
                return render_template('user/resetPassword.html', msg="Password Mismatch")
        else:
            return render_template('user/resetPassword.html', msg="Current Password not Valid")

    else:
        adminLogoutSession()
