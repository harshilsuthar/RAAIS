from flask import request, render_template, redirect, url_for

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.AreaDAO import AreaDAO
from project.com.dao.CameraDAO import CameraDAO
from project.com.dao.CrossroadDAO import CrossroadDAO
from project.com.vo.CameraVO import CameraVO

# loading loadcamera template
@app.route('/admin/loadCamera')
def adminLoadCamera():
    try:
        if adminLoginSession() == 'admin':
            areaDAO = AreaDAO()
            crossroadDAO = CrossroadDAO()
            areaVOList = areaDAO.viewArea()
            crossroadVOList = crossroadDAO.viewCrossroad()
            return render_template('admin/addCamera.html', crossroadVOList=crossroadVOList, areaVOList=areaVOList)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)

# insert data in database
@app.route('/admin/insertCamera', methods=['POST'])
def adminInsertCamera():
    try:
        if adminLoginSession() == 'admin':
            # getting data from template
            cameraCode = request.form['cameraCode']
            camera_AreaId = request.form['camera_AreaId']
            camera_CrossroadId = request.form['camera_CrossroadId']
            x1 = request.form['x1']
            y1 = request.form['y1']
            x2 = request.form['x2']
            y2 = request.form['y2']

            cameraVO = CameraVO()
            cameraDAO = CameraDAO()
            # setting VO object
            cameraVO.cameraCode = cameraCode
            cameraVO.camera_AreaId = camera_AreaId
            cameraVO.camera_CrossroadId = camera_CrossroadId
            cameraVO.x1 = x1
            cameraVO.y1 = y1
            cameraVO.x2 = x2
            cameraVO.y2 = y2
            # inserting method call of cameraDAO file
            cameraDAO.insertCamera(cameraVO)

            return redirect(url_for('adminViewCamera'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)

# loading viewCamera template
@app.route('/admin/viewCamera', methods=['GET'])
def adminViewCamera():
    try:
        if adminLoginSession() == 'admin':
            cameraDAO = CameraDAO()
            cameraVOList = cameraDAO.viewCamera()

            return render_template('admin/viewCamera.html', cameraVOList=cameraVOList)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)

# delete data from database
@app.route('/admin/deleteCamera', methods=['GET'])
def adminDeleteCamera():
    try:
        if adminLoginSession() == 'admin':
            cameraVO = CameraVO()

            cameraDAO = CameraDAO()

            cameraId = request.args.get('cameraId')

            cameraVO.cameraId = cameraId

            cameraDAO.deleteCamera(cameraVO)

            return redirect(url_for('adminViewCamera'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)

# loading edit camera template
@app.route('/admin/editCamera', methods=['GET'])
def adminEditCamera():
    try:
        if adminLoginSession() == 'admin':

            cameraVO = CameraVO()

            cameraDAO = CameraDAO()

            # getting data from template cameraId
            cameraId = request.args.get('cameraId')

            cameraVO.cameraId = cameraId
            cameraVOList = cameraDAO.editCamera(cameraVO)
            # getting data of Area from database
            areaDAO = AreaDAO()
            crossroadDAO = CrossroadDAO()
            areaVOList = areaDAO.viewArea()
            crossroadVOList = crossroadDAO.viewCrossroad()
            return render_template('admin/editCamera.html', cameraVOList=cameraVOList, crossroadVOList=crossroadVOList,
                                   areaVOList=areaVOList)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)

# update data of database cameramaster
@app.route('/admin/updateCamera', methods=['POST'])
def adminUpdateCamera():
    try:
        if adminLoginSession() == 'admin':
            cameraId = request.form['cameraId']
            cameraCode = request.form['cameraCode']
            camera_AreaId = request.form['camera_AreaId']
            camera_CrossroadId = request.form['camera_CrossroadId']
            x1 = request.form['x1']
            y1 = request.form['y1']
            x2 = request.form['x2']
            y2 = request.form['y2']

            cameraVO = CameraVO()
            cameraDAO = CameraDAO()

            cameraVO.cameraId = cameraId
            cameraVO.cameraCode = cameraCode
            cameraVO.camera_AreaId = camera_AreaId
            cameraVO.camera_CrossroadId = camera_CrossroadId
            cameraVO.x1 = x1
            cameraVO.y1 = y1
            cameraVO.x2 = x2
            cameraVO.y2 = y2
            cameraDAO.updateCamera(cameraVO)

            return redirect(url_for('adminViewCamera'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)
