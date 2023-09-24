from coordinates_processing import buf_rect, warning
import cv2
from ultralytics import YOLO
from threading import Thread

class ThreadedCamera(object):
    def __init__(self, source = 0):

        self.capture = cv2.VideoCapture(source)

        self.thread = Thread(target = self.update, args = ())
        self.thread.daemon = True
        self.thread.start()

        self.status = False
        self.frame = None

    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()

    def grab_frame(self):
        if self.status:
            return self.frame
        return None


if __name__ == '__main__':
    DANGER = False
    count = 0
    model = YOLO("best_weights_25epochs_add_data.pt")
    camera = 'video_samples/04_44_54.mp4'
    threaded_camera = ThreadedCamera(camera)
    capture = cv2.VideoCapture(camera)

    while True:
        frame = threaded_camera.grab_frame()

        results = model.predict(frame)
        for result in results:

            bboxes = result.boxes.xyxy.cpu().numpy().astype('int')

            for bbox in bboxes:

                (x, y, x2, y2) = bbox
                cv2.rectangle(frame, (x, y), (x2, y2), (0, 255, 0), 2)

            for i in range(len(result.boxes.data)):
                object_class = int(result.boxes.data[i][5].item())

                if object_class == 0:
                    rail_box = result.boxes.data[i][:4].clone()
                    buf_rectangle = buf_rect(rail_box)
                    cv2.rectangle(frame, (int(buf_rectangle[0]), int(buf_rectangle[1])), (int(buf_rectangle[2]), int(buf_rectangle[3])),
                                  (255, 0, 0), 2)
                try:
                    if object_class == 4:
                        person_box = result.boxes.data[i][:4]
                        DANGER = warning(person_box, buf_rectangle)

                        if DANGER:
                            count += 1
                            cv2.imwrite(f"dangerous_situation_detected_samples/dangerous_sit_{count}_{camera}.jpg", frame)
                            print('DANGER')

                except Exception as ex:
                    print(ex)

                DANGER = False



        cv2.imshow('Video', frame)
        cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()


