from datetime import datetime, date

from flask import request, render_template, redirect, url_for, session

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.PackageDAO import PackageDAO
from project.com.dao.PurchaseDAO import PurchaseDAO
from project.com.vo.PurchaseVO import PurchaseVO


@app.route('/user/loadPurchase')
def userLoadPurchase():
    try:

        if adminLoginSession() == 'user':
            packageDAO = PackageDAO()
            packageVOList = packageDAO.viewPackage()
            msg = request.args.get('msg')
            return render_template('user/addPurchase.html', packageVOList=packageVOList,msg=msg)

        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/insertPurchase', methods=['post'])
def adminInsertpurchase():
    try:
        if adminLoginSession() == 'user':
            purchaseDate = date.today()
            purchaseTime = datetime.now().strftime("%H:%M:%S")
            purchase_loginId = session['session_LoginId']
            packageId = request.form['packageId']
            purchaseVO = PurchaseVO()
            purchaseDAO = PurchaseDAO()

            purchaseVO.purchaseDate = purchaseDate
            purchaseVO.purchaseTime = purchaseTime
            purchaseVO.purchase_loginId = purchase_loginId
            purchaseVO.purchase_packageId = int(packageId)
            purchaseDAO.insertPurchase(purchaseVO)

            return redirect(url_for('userLoadPayment'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/admin/loadPayment', methods=['GET'])
def userLoadPayment():
    return render_template('user/payment.html')

@app.route('/admin/viewPurchase', methods=['GET'])
def adminViewPurchase():
    try:
        if adminLoginSession() == 'admin':
            purchaseDAO = PurchaseDAO()
            purchaseVOList = purchaseDAO.adminViewPurchase()

            return render_template('admin/viewPurchase.html', purchaseVOList=purchaseVOList)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/deletePurchase', methods=['GET'])
def adminDeletePurchase():
    try:
        if adminLoginSession() == 'admin':
            purchaseVO = PurchaseVO()

            purchaseDAO = PurchaseDAO()

            purchaseId = request.args.get('purchaseId')

            purchaseVO.purchaseId = purchaseId

            purchaseDAO.deletePurchase(purchaseVO)

            return redirect(url_for('adminViewPurchase'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/editPurchase', methods=['GET'])
def adminEditPurchase():
    try:
        if adminLoginSession() == 'admin':

            purchaseVO = PurchaseVO()

            purchaseDAO = PurchaseDAO()

            purchaseId = request.args.get('purchaseId')

            purchaseVO.purchaseId = purchaseId

            purchaseVOList = purchaseDAO.editPurchase(purchaseVO)

            return render_template('admin/editPurchase.html', purchaseVOList=purchaseVOList)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/updatePurchase', methods=['POST'])
def adminUpdatePurchase():
    try:
        if adminLoginSession() == 'admin':
            purchaseDate = date.today()
            purchaseTime = datetime.now().strftime("%H:%M:%S")
            purchase_loginId = session['session_LoginId']
            packageId = request.form['packageId']
            purchaseId = request.form['purchaseId']

            purchaseVO = PurchaseVO()
            purchaseDAO = PurchaseDAO()

            purchaseVO.purchaseId = purchaseId
            purchaseVO.purchaseDate = purchaseDate
            purchaseVO.purchaseTime = purchaseTime
            purchaseVO.purchase_loginId = purchase_loginId
            purchaseVO.purchase_packageId = packageId
            purchaseDAO.insertPurchase(purchaseVO)

            purchaseDAO.updatePurchase(purchaseVO)

            return redirect(url_for('adminViewPurchase'))
        else:
            adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/viewPurchase', methods=['GET'])
def userViewPurchase():
    try:
        if adminLoginSession() == 'user':
            purchaseDAO = PurchaseDAO()
            purchaseVO = PurchaseVO()

            purchaseVO.purchase_loginId = session['session_LoginId']
            purchaseVOList = purchaseDAO.viewUserPurchase(purchaseVO)
            return render_template('user/viewPurchase.html', purchaseVOList=purchaseVOList)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)
