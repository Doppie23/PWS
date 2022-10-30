from lijnherkennen import lijn_volger
import cv2
import controlsauto as ca
from time import sleep
import RPi.GPIO as IO
import numpy as np
import math

from pycoral.adapters.common import input_size
from pycoral.adapters.detect import get_objects
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.edgetpu import run_inference

def main():
    model = '/home/dop/PWS/models/object_detection/data/model/v04/efficientdet-lite-bordenv02_edgetpu.tflite'
    labels = '/home/dop/PWS/models/object_detection/data/model/v04/borden-labels.txt'
    threshold = 0.8
    top_k = 3

    print(f'Loading {model} with {labels} labels.')
    interpreter = make_interpreter(model)
    interpreter.allocate_tensors()
    labels = read_label_file(labels)
    inference_size = input_size(interpreter)


    # initialiseren van auto
    print("auto aan het initialiseren")
    IO.setmode(IO.BCM)
    IO.setup(18, IO.OUT)
    t=IO.PWM(18,100)
    gas = 14
    t.start(gas)
    input("licht op esc aan?")

    cap = cv2.VideoCapture(0)

    ca.Stuurhoek(0)
    hoek = lijn_volger() #0 is de begin hoek van de servo
    input("klaar om te gaan druk op enter")
    gas = 20
    t.ChangeDutyCycle(gas)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2_im = frame

        """
        object herkenning
        """
        cv2_im_rgb = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
        cv2_im_rgb = cv2.resize(cv2_im_rgb, inference_size)
        run_inference(interpreter, cv2_im_rgb.tobytes())
        objs = get_objects(interpreter, threshold)[:top_k]
        print(f"objs: {objs}")
        stoppen, gas = auto_ziet_bord(objs, labels, gas)
        t.ChangeDutyCycle(gas)
        cv2_im = append_objs_to_img(cv2_im, inference_size, objs, labels) #tekent viekant om de objecten met percentage

        """
        cleanup (esc om te stoppen)
        """
        key = cv2.waitKey(1)
        if key == 27:
            break
    ca.cleanup()
    cap.release()
    cv2.destroyAllWindows()

def append_objs_to_img(cv2_im, inference_size, objs, labels):
    height, width, channels = cv2_im.shape
    scale_x, scale_y = width / inference_size[0], height / inference_size[1]
    for obj in objs:
        bbox = obj.bbox.scale(scale_x, scale_y)
        x0, y0 = int(bbox.xmin), int(bbox.ymin)
        x1, y1 = int(bbox.xmax), int(bbox.ymax)

        percent = int(100 * obj.score)
        label = '{}% {}'.format(percent, labels.get(obj.id, obj.id))

        cv2_im = cv2.rectangle(cv2_im, (x0, y0), (x1, y1), (0, 255, 0), 2)
        cv2_im = cv2.putText(cv2_im, label, (x0, y0+30),
                             cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)
    return cv2_im

def auto_ziet_bord(objs, labels, gas):
    if len(objs) >= 1:
        for obj in objs:
            label = labels.get(obj.id, obj.id)

            if label in ['paard', 'wegdicht', 'mens', 'stopbord', 'roodlicht']:
                print('stoppen')
                stoppen = True
                gas = 14
            elif label == 'groenlicht':
                stoppen = False
                gas = 20
                print('weer gaan')
            else:
                gas = 20
                stoppen = False
    else:
        gas = 20
        stoppen = False

    return stoppen, gas

if __name__ == '__main__':
    main()