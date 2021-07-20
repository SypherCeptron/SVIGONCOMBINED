import cv2
def ObjectDetector(Image):
    thres = 0.45 # Threshold to detect object



    classNames= []
    classFile = 'coco.names'
    with open(classFile,'rt') as f:
        classNames = f.read().rstrip('\n').split('\n')

    configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weightsPath = 'frozen_inference_graph.pb'

    net = cv2.dnn_DetectionModel(weightsPath,configPath)
    net.setInputSize(320,320)
    net.setInputScale(1.0/ 127.5)
    net.setInputMean((127.5, 127.5, 127.5))

    net.setInputSwapRB(True)
    classIds, confs, bbox = net.detect(Image,confThreshold=thres)
    ObjectInEnvironment = []
    if len(classIds) != 0:
            for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
                if round(confidence*100,2) > 60.00:
                    ObjectInEnvironment.append(classNames[classId-1])
    return ObjectInEnvironment