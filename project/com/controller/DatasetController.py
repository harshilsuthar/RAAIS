import os
from datetime import date, datetime

from flask import request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.DatasetDAO import DatasetDAO
from project.com.vo.DatasetVO import DatasetVO


@app.route('/admin/loadDataset')
def adminLoadDataset():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/addDataset.html')
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertDataset', methods=['POST'])
def adminInsertDataset():
    try:
        if adminLoginSession() == 'admin':

            UPLOAD_FOLDER = 'project/static/adminResources/dataset/'  # setting path of storage data
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # update config path of folder
            datasetVO = DatasetVO()
            datasetDAO = DatasetDAO()

            file = request.files['file']  # getting filename from addDataset
            datasetFilename = secure_filename(file.filename)
            datasetFilepath = os.path.join(app.config['UPLOAD_FOLDER'])  # setting value in variable
            file.save(os.path.join(datasetFilepath, datasetFilename))  # saving file in dataset folder with filename

            datasetVO.datasetFilename = datasetFilename  # saving filename in database
            todayDate = date.today()
            datasetVO.uploadDate = todayDate  # saving current date in database
            nowTime = datetime.now()
            datasetVO.uploadTime = nowTime.strftime("%H:%M:%S")  # saving current date in database
            filepath = datasetFilepath.replace("project", "..")
            datasetVO.datasetFilePath = str(filepath)  # saving filepath in database

            datasetDAO.insertDataset(datasetVO)

            return redirect(url_for('adminViewDataset'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewDataset', methods=['GET'])
def adminViewDataset():
    try:
        if adminLoginSession() == 'admin':
            datasetDAO = DatasetDAO()
            datasetVOList = datasetDAO.viewDataset()
            return render_template('admin/viewDataset.html', datasetVOList=datasetVOList)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteDataset', methods=['GET'])
def adminDeleteDataset():
    try:
        if adminLoginSession() == 'admin':
            datasetVO = DatasetVO()

            datasetDAO = DatasetDAO()

            datasetId = request.args.get('datasetId')

            datasetVO.datasetId = datasetId

            datasetlist = datasetDAO.deleteDataset(datasetVO)

            path = datasetlist.datasetFilePath.replace('..', 'project') + datasetlist.datasetFilename
            try:
                os.remove(path)
            except Exception as ex:
                print(ex)

            return redirect(url_for('adminViewDataset'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/userInsertDataset', methods=['POST'])
def userInsertDataset(file):
    try:
        if adminLoginSession() == 'user':
            datasetVO = DatasetVO()
            datasetDAO = DatasetDAO()

            file = file  # getting filename from addDataset
            datasetFilename = secure_filename(file.filename)
            datasetFilepath = os.path.join(app.config['UPLOAD_FOLDER'])  # setting value in variable
            file.save(os.path.join(datasetFilepath, datasetFilename))

            datasetVO.datasetFilename = datasetFilename  # saving filename in database
            todayDate = date.today()
            datasetVO.uploadDate = todayDate  # saving current date in database
            nowTime = datetime.now()
            datasetVO.uploadTime = nowTime.strftime("%H:%M:%S")  # saving current date in database
            filepath = datasetFilepath.replace("project", "..")
            datasetVO.datasetFilePath = str(filepath)  # saving filepath in database
            filepath = str(filepath)

            datasetDAO.insertDataset(datasetVO)
            return datasetFilename, filepath
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)
