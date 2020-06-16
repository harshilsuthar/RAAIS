from project import db
from project.com.vo.LoginVO import LoginVO
from project.com.vo.PackageVO import PackageVO
from project.com.vo.PurchaseVO import PurchaseVO


class PurchaseDAO:

    def insertPurchase(self, purchaseVO):
        db.session.add(purchaseVO)
        db.session.commit()

    def adminViewPurchase(self):
        purchaseList = db.session.query(PurchaseVO, PackageVO, LoginVO).join(PackageVO,
                                                                             PackageVO.packageId == PurchaseVO.purchase_packageId).join(
            LoginVO, PurchaseVO.purchase_loginId == LoginVO.loginId).all()
        return purchaseList

    def deletePurchase(self, purchaseVO):
        purchaseList = PurchaseVO.query.get(purchaseVO.purchaseId)
        db.session.delete(purchaseList)
        db.session.commit()

    def editPurchase(self, purchaseVO):
        purchaseList = PurchaseVO.query.filter_by(purchaseId=purchaseVO.purchaseId).all()
        return purchaseList

    def updatePurchase(self, purchaseVO):
        db.session.merge(purchaseVO)
        db.session.commit()

    def viewUserPurchase(self, purchaseVO):
        purchaseList = db.session.query(PurchaseVO, PackageVO).filter_by(
            purchase_loginId=purchaseVO.purchase_loginId).join(PackageVO,
                                                               PackageVO.packageId == PurchaseVO.purchase_packageId).all()
        return purchaseList
