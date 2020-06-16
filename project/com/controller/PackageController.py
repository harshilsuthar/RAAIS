from flask import request, render_template, redirect, url_for

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.PackageDAO import PackageDAO
from project.com.vo.PackageVO import PackageVO


@app.route('/admin/loadPackage')
def adminLoadPackage():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/addPackage.html')
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertPackage', methods=['POST'])
def adminInsertpackage():
    try:
        if adminLoginSession() == 'admin':
            packageName = request.form['packageName']
            packagePrice = request.form['packagePrice']
            packageDuration = request.form['packageDuration']

            packageVO = PackageVO()
            packageDAO = PackageDAO()

            packageVO.packageName = packageName
            packageVO.packagePrice = packagePrice
            packageVO.packageDuration = packageDuration

            packageDAO.insertPackage(packageVO)

            return redirect(url_for('adminViewPackage'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewPackage', methods=['GET'])
def adminViewPackage():
    try:
        if adminLoginSession() == 'admin':
            packageDAO = PackageDAO()
            packageVOList = packageDAO.viewPackage()

            return render_template('admin/viewPackage.html', packageVOList=packageVOList)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/deletePackage', methods=['GET'])
def adminDeletePackage():
    try:
        if adminLoginSession() == 'admin':
            packageVO = PackageVO()

            packageDAO = PackageDAO()

            packageId = request.args.get('packageId')

            packageVO.packageId = packageId

            packageDAO.deletePackage(packageVO)

            return redirect(url_for('adminViewPackage'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/editPackage', methods=['GET'])
def adminEditPackage():
    try:
        if adminLoginSession() == 'admin':

            packageVO = PackageVO()

            packageDAO = PackageDAO()

            packageId = request.args.get('packageId')

            packageVO.packageId = packageId

            packageVOList = packageDAO.editPackage(packageVO)
            return render_template('admin/editPackage.html', packageVOList=packageVOList)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/updatePackage', methods=['POST'])
def adminUpdatePackage():
    try:
        if adminLoginSession() == 'admin':
            packageId = request.form['packageId']
            packageName = request.form['packageName']
            packagePrice = request.form['packagePrice']
            packageDuration = request.form['packageDuration']

            packageVO = PackageVO()
            packageDAO = PackageDAO()

            packageVO.packageId = packageId
            packageVO.packageName = packageName
            packageVO.packagePrice = packagePrice
            packageVO.packageDuration = packageDuration

            packageDAO.updatePackage(packageVO)

            return redirect(url_for('adminViewPackage'))
        else:
            adminLogoutSession()

    except Exception as ex:
        print(ex)
