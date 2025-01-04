import pyrealsense2 as rs
import cv2
import numpy as np

# Define the color ranges and corresponding labels
color_ranges = {
    "1": ([0,  155, 200], [4, 190, 240]),
    "2": ([9, 145, 180], [16, 220, 255]),
    "3": ([20, 120, 150], [28, 240, 255]),
    "4": ([55, 120, 120], [70, 180, 200]),
    "5": ([100, 200, 190], [105, 255, 255]),
    "6": ([108, 120, 80], [119, 220, 160]),
    "7": ([120, 90, 100], [130, 140, 140]),
    "8": ([160, 40, 220], [170, 120, 255])
}


def merge_rectangles(rectangles):
    if not rectangles:
        return []

    # Convert to array for easy slicing
    rectangles = np.array(rectangles)
    x1 = rectangles[:, 0]
    y1 = rectangles[:, 1]
    x2 = rectangles[:, 2]
    y2 = rectangles[:, 3]

    # Find the coordinates of the merged rectangle
    x1_merged = np.min(x1)
    y1_merged = np.min(y1)
    x2_merged = np.max(x2)
    y2_merged = np.max(y2)

    return [(x1_merged, y1_merged, x2_merged, y2_merged)]

def detect_colors(frame, color_ranges):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    all_detections = {}

    for color_name, (lower, upper) in color_ranges.items():
        lower_np = np.array(lower)
        upper_np = np.array(upper)
        mask = cv2.inRange(hsv, lower_np, upper_np)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        detections = []
        for contour in contours:
            if cv2.contourArea(contour) > 100:  # filter out small areas
                x, y, w, h = cv2.boundingRect(contour)
                detections.append((x, y, x + w, y + h))

        all_detections[color_name] = detections

    return all_detections

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Detect colors
        all_detections = detect_colors(color_image, color_ranges)

        # Draw merged rectangles
        for color_name, detections in all_detections.items():
            merged_detections = merge_rectangles(detections)
            for (x1, y1, x2, y2) in merged_detections:
                # Draw rectangle
                #cv2.rectangle(color_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Calculate center point
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                # Draw center point
                cv2.circle(color_image, (center_x, center_y), 5, (0, 255, 0), -1)

                # Label at the center point
                cv2.putText(color_image, color_name, (center_x, center_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow('Color Detection', color_image)

        if cv2.waitKey(1) == 27:  # ESC key to break
            break
finally:
    # Stop streaming
    pipeline.stop()
    cv2.destroyAllWindows()
