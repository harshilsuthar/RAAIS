import os
from datetime import datetime, date

from flask import request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.vo.ComplainVO import ComplainVO


# loading add complain template at user side
@app.route('/user/loadComplain')
def userLoadComplain():
    try:
        if adminLoginSession() == 'user':
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            complainVO.complainFrom_LoginId = session['session_LoginId']
            complainVOList = complainDAO.viewUserComplain(complainVO)

            return render_template('user/addComplain.html', complainVOList=complainVOList)

        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


# inserting data in database from user side
@app.route('/user/insertComplain', methods=['POST'])
def userInsertComplain():
    try:
        if adminLoginSession() == 'user':
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainSubject = request.form['complainSubject']
            complainDescription = request.form['complainDescription']
            complainFile = request.files['complainFile']
            uploadTime = datetime.now().strftime("%H:%M:%S")
            uploadDate = date.today()
            # setting complain attachment folder
            UPLOAD_FOLDER = 'project/static/userResources/complain/'  # setting path of storage data
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # update config path of folder
            complainFilename = secure_filename(complainFile.filename)
            complainFilePath = os.path.join(app.config['UPLOAD_FOLDER'])  # setting value in variable
            complainFile.save(os.path.join(complainFilePath, complainFilename))
            complainFilePath = complainFilePath.replace("project", "..")

            complainVO.complainSubject = complainSubject
            complainVO.complainDescription = complainDescription
            complainVO.complainFilename = complainFilename
            complainVO.complainFilePath = str(complainFilePath)
            complainVO.complainDate = uploadDate
            complainVO.complainTime = uploadTime
            complainVO.complainStatus = 'pending'
            complainVO.complainFrom_LoginId = session['session_LoginId']
            complainDAO.insertComplain(complainVO)

            return redirect(url_for('userLoadComplain'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)

# user delete complain and data delete from database
@app.route('/user/deleteComplain', methods=['GET'])
def userDeleteComplain():
    try:
        if adminLoginSession() == 'user':
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainId = request.args.get('complainId')
            complainVO.complainId = complainId
            complainVOList = complainDAO.viewComplain(complainVO)
            complainDictList = [i.as_dict() for i in complainVOList]
            complainFilePath = complainDictList[0]['complainFilePath']
            complainFilename = complainDictList[0]['complainFilename']
            replyFilePath = complainDictList[0]['replyFilePath']
            replyFilename = complainDictList[0]['replyFilename']

            try:
                path = complainFilePath.replace('..', 'project') + complainFilename
                os.remove(path)
            except Exception as ex:
                print("complain file not deleted")

            try:
                path = replyFilePath.replace('..', 'project') + replyFilename
                os.remove(path)
            except Exception as ex:
                print("reply file not deleted")

            complainDAO.deleteComplain(complainVO)
            return redirect(url_for('userLoadComplain'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


# admin insert reply to database
@app.route('/admin/insertReply', methods=['POST'])
def adminInsertReply():
    try:
        if adminLoginSession() == 'admin':
            complainId = request.form['complainId']
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()
            replysubject = request.form['replysubject']
            replyDescription = request.form['replyDescription']
            replyFile = request.files['replyFile']
            uploadTime = datetime.now().strftime("%H:%M:%S")
            uploadDate = date.today()
            # settting path of admin reply attachment
            UPLOAD_FOLDER = 'project/static/userResources/reply/'  # setting path of storage data
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # update config path of folder
            replyFilename = secure_filename(replyFile.filename)
            replyFilepath = os.path.join(app.config['UPLOAD_FOLDER'])  # setting value in variable
            replyFile.save(os.path.join(replyFilepath, replyFilename))
            replyFilepath = replyFilepath.replace("project", "..")

            complainVO.complainId = complainId
            complainVO.replysubject = replysubject
            complainVO.replyDescription = replyDescription
            complainVO.replyFilename = replyFilename
            complainVO.replyFilePath = replyFilepath
            complainVO.replyDate = uploadDate
            complainVO.replyTime = uploadTime
            complainVO.complainStatus = "replied"
            complainVO.complainTo_LoginId = session['session_LoginId']

            complainDAO.updateComplain(complainVO)

            return redirect(url_for('adminViewComplain'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


# admin view complain loading template
@app.route('/admin/viewComplain')
def adminViewComplain():
    complainDAO = ComplainDAO()
    complainVO = ComplainVO()
    complainVO.complainTo_LoginId = session['session_LoginId']
    complainVOList = complainDAO.viewAdminComplain(complainVO)
    return render_template('admin/viewComplain.html', complainVOList=complainVOList)


# admin load reply template
@app.route('/admin/replyComplain')
def adminReplyComplain():
    try:
        if adminLoginSession() == 'admin':

            complainVO = ComplainVO()

            complainDAO = ComplainDAO()

            complainId = request.args.get('complainId')

            complainVO.complainId = complainId

            complainVOList = complainDAO.editComplain(complainVO)

            return render_template('admin/addReply.html', complainVOList=complainVOList)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


# user view reply template load
@app.route('/user/viewReply', methods=['GET'])
def userViewReply():
    try:
        if adminLoginSession() == 'user':
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            complainId = request.args.get('complainId')
            complainVO.complainId = complainId
            replyVOList = complainDAO.viewComplain(complainVO)

            return render_template('user/viewReply.html', replyVOList=replyVOList)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)
