import cv2
import numpy as np
import pyrealsense2 as rs

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline.start(config)

def get_color(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        frame = param
        color = frame[y, x]
        hsv_color = cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_BGR2HSV)[0][0]
        print(f"HSV: {hsv_color}")

try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        frame = np.asanyarray(color_frame.get_data())

        cv2.imshow('RealSense', frame)

        cv2.setMouseCallback('RealSense', get_color, frame)

        if cv2.waitKey(1) == 27:  # ESC key to break
            break
finally:
    pipeline.stop()
    cv2.destroyAllWindows()
