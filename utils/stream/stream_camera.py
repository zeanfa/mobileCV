import cv2
import imagezmq
import socket

# gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 60fps
# Flip the image by setting the flip_method (most common values: 0 and 2)
# display_width and display_height determine the size of the window on the screen


def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=480,
    display_height=320,
    framerate=30,
    flip_method=0,
    sensor_id=0
):
    return (
        "nvarguscamerasrc sensor_id=%d ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def show_camera():
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=4))
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=4), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        # window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
        #sender = imagezmq.ImageSender(connect_to="tcp://192.168.1.12:5555")
        sender = imagezmq.ImageSender(connect_to="tcp://*:5555", REQ_REP=False)
        rpi_name = socket.gethostname()
        print(rpi_name)
        # Window
        while True:#cv2.getWindowProperty("CSI Camera", 0) >= 0:
            ret_val, img = cap.read()
            #cv2.imshow("CSI Camera", img)
            jpeg_quality = 80
            ret_code, jpg_img = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
            # This also acts as
            keyCode = cv2.waitKey(30) & 0xFF
            # Stop the program on the ESC key
            if keyCode == 27:
                break
            #sender.send_image(rpi_name, img)
            sender.send_jpg(rpi_name, jpg_img)
        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")


if __name__ == "__main__":
    show_camera()
