import os
from collections import OrderedDict
from datetime import date, datetime

import cv2 as cv
import numpy as np
from flask import request, render_template, redirect, url_for, jsonify
from flask import session
from numpy import ones, vstack
from numpy.linalg import lstsq
from scipy.spatial import distance
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.CameraDAO import CameraDAO
from project.com.dao.PurchaseDAO import PurchaseDAO
from project.com.dao.VideoDAO import VideoDAO
from project.com.vo.CameraVO import CameraVO
from project.com.vo.PurchaseVO import PurchaseVO
from project.com.vo.VideoVO import VideoVO


@app.route('/user/loadVideo')
def userLoadVideo():
    try:
        if adminLoginSession() == 'user':
            videoDAO = VideoDAO()

            videoVOList = videoDAO.viewLocalData()
            purchaseVO = PurchaseVO()
            purchaseDAO = PurchaseDAO()
            purchaseVO.purchase_loginId = session['session_LoginId']
            purchaseVOList = purchaseDAO.viewUserPurchase(purchaseVO)
            purchaseVODict = [[i[0].as_dict(), i[1].as_dict()] for i in [j for j in purchaseVOList]]
            purchaseDate = [i[0]['purchaseDate'] for i in purchaseVODict]
            if len(purchaseDate) > 0:
                dateMax = max(purchaseDate)
                index = purchaseDate.index(dateMax)
                purchaseDuration = purchaseVODict[index][1]['packageDuration']
                purchaseDuration, _ = purchaseDuration.split(' ')
                currentDate = date.today()
                dateDifference = currentDate - dateMax
                if int(purchaseDuration) * 28 > int(dateDifference.days):
                    return render_template('user/addVideo.html', videoVOList=videoVOList)
                else:
                    return redirect(
                        url_for('userLoadPurchase',
                                msg='Current Package Is Expired, Purchase Package To Continue using System'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/userProcessVideo', methods=['POST'])
def userProcessVideo():
    try:
        if adminLoginSession() == 'user':
            UPLOAD_FOLDER = 'project/static/userResources/inputVideo/'  # setting path of storage data
            outputFolder = 'project/static/userResources/outputVideo/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # update config path of folder
            file = request.files['file']  # getting filename from addVideo
            videoFilename = secure_filename(file.filename)  # make it secure from werkzeug
            videoFilepath = os.path.join(app.config['UPLOAD_FOLDER'])  # setting value in variable
            file.save(os.path.join(videoFilepath, videoFilename))  # saving file in video folder with filename
            renameFilename = session['session_LoginUsername'].split('@')
            renameFilename = renameFilename[0] + '_' + str(date.today()) + '_' + str(
                datetime.now().strftime("%H.%M.%S")) + '.mp4'
            try:
                # videoFilepath = videoFilepath.replace('project', '../..')
                os.rename(os.path.join(videoFilepath, videoFilename), os.path.join(videoFilepath, renameFilename))
                videoFilename = renameFilename
            except Exception as ex:
                print(ex)

            video_data = request.form['video_CameraId']
            cameraId = video_data.split(',')[0]
            cameraDAO = CameraDAO()
            cameraVO = CameraVO()
            cameraVO.cameraId = cameraId
            cameraVOList = cameraDAO.editCamera(cameraVO)
            cameraVODict = [i.as_dict() for i in cameraVOList]

            class Tracker:
                def __init__(self, maxLost=30):  # maxLost: maximum object lost counted when the object is being tracked
                    self.nextObjectID = 0  # ID of next object
                    self.objects = OrderedDict()  # stores ID:Locations
                    self.lost = OrderedDict()  # stores ID:Lost_count
                    self.dt = OrderedDict()
                    self.maxLost = maxLost  # maximum number of frames object was not detected.

                def addObject(self, new_object_location, ls):
                    self.objects[self.nextObjectID] = new_object_location  # store new object location
                    self.dt[self.nextObjectID] = ls
                    self.lost[self.nextObjectID] = 0  # initialize frame_counts for when new object is undetected
                    self.nextObjectID += 1

                def removeObject(self, objectID):  # remove tracker data after object is lost
                    del self.objects[objectID]
                    del self.lost[objectID]
                    del self.dt[objectID]

                @staticmethod
                def getLocation(bounding_box):
                    xlt, ylt, xrb, yrb = bounding_box
                    return (int((xlt + xrb) / 2.0), int((ylt + yrb) / 2.0)), [xlt, ylt, xrb, yrb]

                def update(self, detections):
                    if len(detections) == 0:  # if no object detected in the frame
                        lost_ids = list(self.lost.keys())
                        for objectID in lost_ids:
                            self.lost[objectID] += 1
                            if self.lost[objectID] > self.maxLost: self.removeObject(objectID)

                        return self.objects, self.dt

                    new_object_locations = np.zeros((len(detections), 2), dtype="int")  # current object locations
                    ls = list()
                    for (i, detection) in enumerate(detections):
                        new_object_locations[i], temp = self.getLocation(detection)
                        ls.insert(i, temp)

                    if len(self.objects) == 0:
                        for i in range(0, len(detections)):
                            self.addObject(new_object_locations[i], ls[i])
                    else:
                        objectIDs = list(self.objects.keys())
                        previous_object_locations = np.array(list(self.objects.values()))
                        D = distance.cdist(previous_object_locations,
                                           new_object_locations)  # pairwise distance between previous and current
                        row_idx = D.min(
                            axis=1).argsort()  # (minimum distance of previous from current).sort_as_per_index
                        cols_idx = D.argmin(axis=1)[row_idx]  # index of minimum distance of previous from current

                        assignedRows, assignedCols = set(), set()

                        for (row, col) in zip(row_idx, cols_idx):

                            if row in assignedRows or col in assignedCols:
                                continue

                            objectID = objectIDs[row]
                            self.objects[objectID] = new_object_locations[col]
                            self.lost[objectID] = 0
                            self.dt[objectID] = ls[col]
                            assignedRows.add(row)
                            assignedCols.add(col)

                        unassignedRows = set(range(0, D.shape[0])).difference(assignedRows)
                        unassignedCols = set(range(0, D.shape[1])).difference(assignedCols)

                        if D.shape[0] >= D.shape[1]:
                            for row in unassignedRows:
                                objectID = objectIDs[row]
                                self.lost[objectID] += 1

                                if self.lost[objectID] > self.maxLost:
                                    self.removeObject(objectID)

                        else:
                            for col in unassignedCols:
                                self.addObject(new_object_locations[col], ls[col])

                    return self.objects, self.dt

            yolomodel = {"config_path": "project/static/userResources/model/yolo_dir/yolov3.cfg",
                         "model_weights_path": "project/static/userResources/model/yolo_dir/yolov3.weights",
                         "coco_names": "project/static/userResources/model/yolo_dir/coco.names",
                         "confidence_threshold": 0.6,
                         "threshold": 0.6
                         }

            net = cv.dnn.readNetFromDarknet(yolomodel["config_path"], yolomodel["model_weights_path"])
            np.random.seed(12345)
            layer_names = net.getLayerNames()
            layer_names = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
            maxLost = 5  # maximum number of object losts counted when the object is being tracked
            tracker = Tracker(maxLost=maxLost)

            video_src = videoFilepath + videoFilename
            cap = cv.VideoCapture(video_src)
            (H, W) = (None, None)  # input image height and width for the network
            writer = None
            ct = 0
            error = 0
            frames = 4
            timeframe = 1
            ls = list()
            alertct = 0
            flag = False
            speed = 2
            countFlag = False
            properCarCount = 0
            while True:
                ok, image = cap.read()
                alertflag = False
                if ct % frames == 0:
                    if not ok:
                        print("Cannot read the video feed.")
                        break

                    if W is None or H is None:
                        (H, W) = image.shape[:2]

                    blob = cv.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
                    net.setInput(blob)
                    detections_layer = net.forward(layer_names)  # detect objects using object detection model

                    detections_bbox = []  # bounding box for detections

                    boxes, confidences, classIDs = [], [], []
                    for out in detections_layer:
                        for detection in out:
                            scores = detection[5:]
                            classID = np.argmax(scores)
                            if classID == 2:
                                confidence = scores[classID]
                            else:
                                confidence = 0

                            if confidence > yolomodel['confidence_threshold']:
                                box = detection[0:4] * np.array([W, H, W, H])
                                (centerX, centerY, width, height) = box.astype("int")
                                x = int(centerX - (width / 2))
                                y = int(centerY - (height / 2))

                                boxes.append([x, y, int(width), int(height)])
                                confidences.append(float(confidence))
                                classIDs.append(classID)

                    idxs = cv.dnn.NMSBoxes(boxes, confidences, yolomodel["confidence_threshold"],
                                           yolomodel["threshold"])
                    if len(idxs) > 0:
                        for i in idxs.flatten():
                            (x, y) = (boxes[i][0], boxes[i][1])
                            (w, h) = (boxes[i][2], boxes[i][3])
                            detections_bbox.append((x, y, x + w, y + h))

                    objects, dt = tracker.update(
                        detections_bbox)  # update tracker based on the newly detected objects
                    if ct == frames:
                        dt1 = dict(dt)
                    if ct % (frames * timeframe) == 0 and ct >= (frames * timeframe):
                        kls = dict()
                        dt2 = dict(dt)
                        for key in dt1.keys():
                            if key in dt2.keys():
                                xlt, ylt, xrb, yrb = dt1[key]
                                x1, y1 = (int((xlt + xrb) / 2.0), int((ylt + yrb) / 2.0))
                                xlt, ylt, xrb, yrb = dt2[key]
                                x2, y2 = (int((xlt + xrb) / 2.0), int((ylt + yrb) / 2.0))
                                dist = int(((y2 - y1) ** 2 + (x2 - x1) ** 2) ** .5)
                                kls[key] = dist
                                flag = True
                        dt1 = dict(dt)
                    if flag:
                        lineX1 = cameraVODict[0]['x1']
                        lineX2 = cameraVODict[0]['x2']
                        lineY1 = cameraVODict[0]['y1']
                        lineY2 = cameraVODict[0]['y2']
                        points = [(lineX1, lineY1), (lineX2, lineY2)]
                        x_coords, y_coords = zip(*points)
                        A = vstack([x_coords, ones(len(x_coords))]).T
                        m, c = lstsq(A, y_coords)[0]
                        print(m)
                        cv.line(image, (lineX1, lineY1), (lineX2, lineY2), (0, 255, 255))
                        properCarCount = 0
                        ilegalCarCount = 0
                        print(error)
                        for key, value in dt.items():
                            if key in kls.keys():
                                x3 = (((value[3] + value[1]) / 2) - c) / m
                                if (value[2]) < x3:
                                    properCarCount += 1
                                    cv.rectangle(image, (value[0], value[1]), (value[2], value[3]), (255, 255, 255),
                                                 2)
                                elif (value[2]) >= x3 and kls[key] > speed:
                                    cv.rectangle(image, (value[0], value[1]), (value[2], value[3]), (255, 0, 0), 2)
                                else:
                                    ilegalCarCount += 1
                                    cv.rectangle(image, (value[0], value[1]), (value[2], value[3]), (0, 0, 255), 2)
                                    alertflag = True
                                    # carCount += 1
                    if alertflag:
                        alertct += 1
                    else:
                        alertct = 0

                    if alertct == 20:
                        countFlag = True
                        totalIllegalCarCount = ilegalCarCount
                        totalLegalCarCount = properCarCount

                    if countFlag == False:
                        totalIllegalCarCount = 0
                        totalLegalCarCount = properCarCount

                    ob = dict(objects)
                    ls.append([ob])

                    for (objectID, centroid) in objects.items():
                        text = "ID {}".format(objectID)
                        cv.putText(image, text, (centroid[0] - 10, centroid[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                                   (0, 255, 0),
                                   2)
                        cv.circle(image, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
                    image = cv.resize(image, (1366, 762))
                    cv.imshow("image", image)

                    if cv.waitKey(1) & 0xFF == ord('q'):
                        break

                    if writer is None:
                        fourcc = cv.VideoWriter_fourcc(*'VP80')
                        outputVideoFilename = videoFilename.replace('.mp4', '.webm')
                        writer = cv.VideoWriter(outputFolder + outputVideoFilename, fourcc, 30, (1366, 762), True)
                    writer.write(image)
                ct += 1
            writer.release()
            cap.release()
            cv.destroyWindow("image")
            return redirect(
                url_for("userInsertVideo", videoFilename=videoFilename, outputVideoFilename=outputVideoFilename,
                        videoFilepath=videoFilepath,
                        video_data=video_data, outputFolder=outputFolder, totalIllegalCarCount=totalIllegalCarCount,
                        totalLegalCarCount=totalLegalCarCount))
        else:
            adminLogoutSession()
    except Exception as e:
        print(e)


@app.route('/user/insertVideo', methods=['GET'])
def userInsertVideo():
    try:
        if adminLoginSession() == 'user':

            inputvideoFilename = request.args.get('videoFilename')
            inputvideoFilepath = request.args.get('videoFilepath')
            video_data = request.args.get('video_data')
            outputvideoFilename = request.args.get('outputVideoFilename')
            outputvideoFilePath = request.args.get('outputFolder')
            totalIllegalCarCount = request.args.get('totalIllegalCarCount')
            totalLegalCarCount = request.args.get('totalLegalCarCount')
            videoVO = VideoVO()
            videoDAO = VideoDAO()
            # saving filename in database
            todayDate = date.today()  # saving current date in database
            nowTime = datetime.now()  # saving current date in database
            inputvideoFilepath = inputvideoFilepath.replace("project", "..")  # saving filepath in database
            outputvideoFilePath = outputvideoFilePath.replace("project", "..")
            videoVO.video_CameraId = video_data.split(',')[0]
            videoVO.video_CrossroadId = video_data.split(',')[1]
            videoVO.video_AreaId = video_data.split(',')[2]
            videoVO.video_LoginId = session['session_LoginId']
            videoVO.inputVideoFilename = inputvideoFilename
            videoVO.inputVideoFilePath = str(inputvideoFilepath)
            videoVO.uploadTime = nowTime.strftime("%H:%M:%S")
            videoVO.uploadDate = todayDate
            videoVO.outputVideoFilename = outputvideoFilename
            videoVO.outputVideoFilePath = outputvideoFilePath
            videoVO.illegalCarCount = totalIllegalCarCount
            videoVO.legalCarCount = totalLegalCarCount
            videoDAO.insertVideo(videoVO)

            return redirect(url_for('userViewVideo'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/viewVideo', methods=['GET'])
def userViewVideo():
    try:
        if adminLoginSession() == 'user':
            videoDAO = VideoDAO()
            videoVOList = videoDAO.userViewVideo()
            return render_template('user/viewVideo.html', videoVOList=videoVOList)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewVideo', methods=['GET'])
def adminViewVideo():
    try:
        if adminLoginSession() == 'admin':
            videoDAO = VideoDAO()
            videoVOList = videoDAO.adminViewVideo()
            return render_template('admin/viewVideo.html', videoVOList=videoVOList)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteVideo', methods=['GET'])
def adminDeleteVideo():
    try:
        if adminLoginSession() == 'admin':
            videoVO = VideoVO()

            videoDAO = VideoDAO()

            videoId = request.args.get('videoId')

            videoVO.videoId = videoId

            videoVOList = videoDAO.deleteVideo(videoVO)

            inputPath = videoVOList.inputVideoFilePath.replace('..', 'project') + videoVOList.inputVideoFilename
            outputPath = videoVOList.outputVideoFilePath.replace('..', 'project') + videoVOList.outputVideoFilename

            try:
                os.remove(inputPath)
                os.remove(outputPath)

            except Exception as ex:
                print(ex)

            return redirect(url_for('adminViewVideo'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/deleteVideo', methods=['GET'])
def userDeleteVideo():
    try:
        if adminLoginSession() == 'user':
            videoVO = VideoVO()
            videoDAO = VideoDAO()

            videoId = request.args.get('videoId')
            videoVO.videoId = videoId
            videoVOList = videoDAO.deleteVideo(videoVO)

            inputPath = videoVOList.inputVideoFilePath.replace('..', 'project') + videoVOList.inputVideoFilename
            outputPath = videoVOList.outputVideoFilePath.replace('..', 'project') + videoVOList.outputVideoFilename

            try:
                os.remove(inputPath)
                os.remove(outputPath)

            except Exception as ex:
                print(ex)

            return redirect(url_for('userViewVideo'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/ajaxLoadDateRegister')
def adminAjaxLoadDateRegister():
    videoVO = VideoVO()
    videoDAO = VideoDAO()

    index_LoginId = request.args.get('index_LoginId')

    videoVO.video_LoginId = index_LoginId

    ajaxAdminIndexDateVOList = videoDAO.ajaxDateAdminIndex(videoVO)

    print("ajaxAdminIndexDateVOList >>>>>>>>>>>>>>>>>> ", ajaxAdminIndexDateVOList)

    ajaxDateDictList = [i.as_dict() for i in ajaxAdminIndexDateVOList]
    print("ajaxDateDictList >>>>>>>>>>>>>>>>>> ", ajaxDateDictList)

    ajaxAdminIndexDateList = []
    for i in ajaxDateDictList:
        ajaxAdminIndexDateList.append({"videoId": i['videoId'], "uploadDate": i['uploadDate'].strftime('%d/%m/%Y')})

    print("ajaxAdminIndexDateList >>>>>>>>>>>>>>>>>> ", ajaxAdminIndexDateList)

    return jsonify(ajaxAdminIndexDateList)


@app.route('/admin/ajaxGetGraphData')
def adminAjaxGetGraphData():
    videoVO = VideoVO()
    videoDAO = VideoDAO()

    index_VideoId = request.args.get('index_VideoId')

    videoVO.videoId = index_VideoId

    ajaxGraphDataList = videoDAO.ajaxGetGraphData(videoVO)

    print("ajaxGraphDataList >>>>>>>>>>>>>>>>>> ", ajaxGraphDataList)

    graphDict = {}
    counter = False
    if len(ajaxGraphDataList) != 0:
        counter = True

        dict1 = {}
        for i in ajaxGraphDataList:
            dict1['illegalCarCount'] = i.illegalCarCount
            dict1['legalCarCount'] = i.legalCarCount

            graphDict.update(dict1)

    print('graphDict>>>', graphDict)
    if counter:
        response = {'responseKey': graphDict}
        print('response>>>>>>>>', response)

    else:
        response = {'responseKey': 'Error'}

    return jsonify(response)
