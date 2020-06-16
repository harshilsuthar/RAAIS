from flask import request, render_template, redirect, url_for

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.AreaDAO import AreaDAO
from project.com.dao.CrossroadDAO import CrossroadDAO
from project.com.vo.CrossroadVO import CrossroadVO


@app.route('/admin/loadCrossroad')
def adminLoadCrossroad():
    try:
        if adminLoginSession() == 'admin':
            areaDAO = AreaDAO()
            areaVOList = areaDAO.viewArea()
            return render_template('admin/addCrossroad.html', areaVOList=areaVOList)  # ,registerVOList
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertCrossroad', methods=['POST'])
def adminInsertCrossroad():
    try:
        if adminLoginSession() == 'admin':
            crossroadName = request.form['crossroadName']
            crossroadLandmark = request.form['crossroadLandmark']
            crossroad_AreaId = request.form['crossroad_AreaId']
            crossroadVO = CrossroadVO()
            crossroadDAO = CrossroadDAO()

            crossroadVO.crossroadName = crossroadName
            crossroadVO.crossroadLandmark = crossroadLandmark
            crossroadVO.crossroad_AreaId = crossroad_AreaId

            crossroadDAO.insertCrossroad(crossroadVO)

            return redirect(url_for('adminViewCrossroad'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewCrossroad', methods=['GET'])
def adminViewCrossroad():
    try:
        if adminLoginSession() == 'admin':
            crossroadDAO = CrossroadDAO()
            crossroadVOList = crossroadDAO.viewCrossroad()

            return render_template('admin/viewCrossroad.html', crossroadVOList=crossroadVOList)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteCrossroad', methods=['GET'])
def adminDeleteCrossroad():
    try:
        if adminLoginSession() == 'admin':
            crossroadVO = CrossroadVO()

            crossroadDAO = CrossroadDAO()

            crossroadId = request.args.get('crossroadId')

            crossroadVO.crossroadId = crossroadId

            crossroadDAO.deleteCrossroad(crossroadVO)

            return redirect(url_for('adminViewCrossroad'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/editCrossroad', methods=['GET'])
def adminEditCrossroad():
    try:
        if adminLoginSession() == 'admin':

            crossroadVO = CrossroadVO()

            crossroadDAO = CrossroadDAO()

            areaDAO = AreaDAO()

            crossroadId = request.args.get('crossroadId')

            crossroadVO.crossroadId = crossroadId

            crossroadVOList = crossroadDAO.editCrossroad(crossroadVO)

            areaVOList = areaDAO.viewArea()

            return render_template('admin/editCrossroad.html', crossroadVOList=crossroadVOList, areaVOList=areaVOList)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/updateCrossroad', methods=['POST'])
def adminUpdateCrossroad():
    try:
        if adminLoginSession() == 'admin':
            crossroadId = request.form['crossroadId']
            crossroad_AreaId = request.form['crossroad_AreaId']
            crossroadName = request.form['crossroadName']
            crossroadLandmark = request.form['crossroadLandmark']

            crossroadVO = CrossroadVO()
            crossroadDAO = CrossroadDAO()

            crossroadVO.crossroadId = crossroadId
            crossroadVO.crossroad_AreaId = crossroad_AreaId
            crossroadVO.crossroadName = crossroadName
            crossroadVO.crossroadLandmark = crossroadLandmark

            crossroadDAO.updateCrossroad(crossroadVO)

            return redirect(url_for('adminViewCrossroad'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)
