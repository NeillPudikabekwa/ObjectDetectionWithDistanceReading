
import cv2

# variables
# distance from camera to object(face) measured
KNOWN_DISTANCE = 80.0 # centimeter

# width of face in the real world or Object Plane
KNOWN_WIDTH = 15.0 # centimeter

# Colors
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (36, 255, 255)
BLACK=(0,0,0)
fonts = cv2.FONT_HERSHEY_COMPLEX
font=cv2.FONT_HERSHEY_COMPLEX_SMALL = 5

# Capture the video
#cam="http://192.168.1.100/wmf/#/uni/channel"
cam=0
cap = cv2.VideoCapture(cam)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# face detector object
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


# focal length finder function
def focal_length(measured_distance, real_width, width_in_rf_image):
    focal_length_value = (width_in_rf_image * measured_distance) / real_width
    return focal_length_value


# distance estimation function
def distance_finder(focal_length, real_face_width, face_width_in_frame):
    distance = (real_face_width * focal_length) / face_width_in_frame
    if distance >= 181.0:
            cv2.putText(
                frame, f"[WARNING]", (10, 50), fonts, 1, (GREEN), 2
            )
            cv2.putText(
                frame, "PGN 0b000", (1000, 20), font, 1, (GREEN), 2
            )
            cv2.putText(
                frame, "NORMAL OPERATION", (1000, 50), font, 1, (GREEN), 2
            )
    if distance >= 101.0 and distance <= 180.0:
                    cv2.putText(
                        frame, f"[SLOW]", (10, 50), fonts, 1, (YELLOW), 2
                    )
                    cv2.putText(
                        frame, "PGN 0b011", (1000, 20), font, 1, (YELLOW), 2
                    )
                    cv2.putText(
                        frame, "SLOW_DOWN", (1000, 50), font, 1, (YELLOW), 2
                    )
    if distance <= 100.0:
            cv2.putText(
                frame, f"[STOP!!]", (10, 50), fonts, 1, (RED), 2
            )
            cv2.putText(
                frame, "PGN 0b001", (1000, 20), font, 1, (RED), 2
            )
            cv2.putText(
                frame, "EMERGENCY_STOP", (1000, 50), font, 1, (RED), 2
            )

    return distance


# face detector function
def face_data(image):

    face_width = 0
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)
    for (x, y, h, w) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), BLACK, 1)
        face_width = w

    return face_width


# reading reference image from directory
ref_image = cv2.imread("Ref_image.png")
ref_image_face_width = face_data(ref_image)
focal_length_found = focal_length(KNOWN_DISTANCE, KNOWN_WIDTH, ref_image_face_width)

while True:
    _, frame = cap.read()

    # calling face_data function
    face_width_in_frame = face_data(frame)

    # finding the distance by calling function Distance
    if face_width_in_frame != 0:
     Distance = distance_finder(focal_length_found, KNOWN_WIDTH, face_width_in_frame)
        # Drwaing Text on the screen
     if Distance >=181:
        cv2.putText(
            frame, f"D={round(Distance,2)}cm", (10, 100), fonts, 1, (GREEN), 2
        )
     if Distance >=101 and Distance <=180:
        cv2.putText(
            frame, f"D={round(Distance,2)}cm", (10, 100), fonts, 1, (YELLOW), 2
        )
     if Distance <=100:
        cv2.putText(
            frame, f"D={round(Distance,2)}cm", (10, 100), fonts, 1, (RED), 2
        )
    cv2.imshow("[System Warning]", frame)
    if cv2.waitKey(1) == ord("t"):
        break
cap.release()
cv2.destroyAllWindows()
