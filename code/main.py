from lijnherkennen import lijn_volger
import cv2
import controlsauto as ca
from time import sleep
import RPi.GPIO as IO
import numpy as np

from pycoral.adapters.common import input_size
from pycoral.adapters.detect import get_objects
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.edgetpu import run_inference

def main():
    model = '/home/dop/PWS/models/object_detection/data/model/v03-(werkt op coral)/efficientdet-lite-borden_edgetpu.tflite'
    labels = '/home/dop/PWS/models/object_detection/data/model/v03-(werkt op coral)/borden-labels.txt'
    threshold = 0.1
    top_k = 3

    print(f'Loading {model} with {labels} labels.')
    interpreter = make_interpreter(model)
    interpreter.allocate_tensors()
    labels = read_label_file(labels)
    inference_size = input_size(interpreter)

    minstuurhoek = -35
    maxstuurhoek = 29

    # initialiseren van auto
    print("auto aan het initialiseren")
    IO.setmode(IO.BCM)
    IO.setup(18, IO.OUT)
    t=IO.PWM(18,100)
    throttle = 14
    t.start(throttle)
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

        cv2_im_rgb = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
        cv2_im_rgb = cv2.resize(cv2_im_rgb, inference_size)
        run_inference(interpreter, cv2_im_rgb.tobytes())
        objs = get_objects(interpreter, threshold)[:top_k]
        auto_ziet_bord(objs, labels)
        cv2_im = append_objs_to_img(cv2_im, inference_size, objs, labels) #tekent viekant om de objecten met percentage

        """
        hoek sturen met opencv
        """
        stuurhoek, averaged_lines = hoek.stabhoek(cv2_im)

        lane_lines_image = display_lines(cv2_im, averaged_lines)
        stuurhoek_laten_zien(lane_lines_image, stuurhoek)

        cv2.imshow("frame", lane_lines_image)
        
        #zodat de servo niet te ver gaat en als de hoek wel zo groot is gaat de motor langzamer
        if stuurhoek < minstuurhoek:
            stuurhoek = minstuurhoek
            if gas != 16:
                gas = 16
                t.ChangeDutyCycle(gas)
        elif stuurhoek > maxstuurhoek:
            stuurhoek = maxstuurhoek
            if gas != 16:
                gas = 16
                t.ChangeDutyCycle(gas)
        elif gas == 16 and stuurhoek < maxstuurhoek and stuurhoek > minstuurhoek:    # om gas weer terug te zetten als de hoek weer in servo range zit
            gas = 20
            t.ChangeDutyCycle(gas)
        
        ca.Stuurhoek(stuurhoek)
        print("hoek:", stuurhoek, "gas:", gas)

        

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

def display_lines(frame, lines, line_color=(0, 255, 0), line_width=10):
    line_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
    line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    return line_image

def stuurhoek_laten_zien(frame, stuurhoek, line_color=(0,0,255), line_width=10):
    richting = np.zeros_like(frame)
    height, width, _ = frame.shape
    stuur_hoek_rad = (stuurhoek+90)/180*math.pi

    x1 = int(width / 2)
    y1 = height
    x2 = int(x1 - height / 2 / math.tan(stuur_hoek_rad))
    y2 = int(height / 2)

    cv2.line(frame, (x1, y1), (x2, y2), line_color, line_width)
    richting = cv2.addWeighted(frame, 0.8, richting, 1, 1)
    return richting

def auto_ziet_bord(objs, labels):
    for obj in objs:
        label = labels.get(obj.id, obj.id)

        if label == 'paard':
            print('paard')
        if label == 'parkeerbord':
            print('parkeerbord')
        if label == 'wegdicht':
            print('wegdicht')
        if label == 'mens':
            print('mens')
        if label == 'fietspad':
            print('fietspad')
        if label == 'zebrapad':
            print('zebrapad')
        if label == 'stopbord':
            print('stopbord')
        if label == 'groenlicht':
            print('groenlicht')
        if label == 'roodlicht':
            print('roodlicht')

if __name__ == '__main__':
    main()