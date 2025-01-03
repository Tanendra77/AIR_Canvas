import cv2
import numpy as np
import streamlit as st
from collections import deque

# Streamlit App Title
st.title("Virtual Painter")
st.sidebar.header("Marker and Brush Settings")

# Sidebar controls
upper_hue = st.sidebar.slider("Upper Hue", 0, 180, 153)
upper_saturation = st.sidebar.slider("Upper Saturation", 0, 255, 255)
upper_value = st.sidebar.slider("Upper Value", 0, 255, 255)
lower_hue = st.sidebar.slider("Lower Hue", 0, 180, 64)
lower_saturation = st.sidebar.slider("Lower Saturation", 0, 255, 72)
lower_value = st.sidebar.slider("Lower Value", 0, 255, 49)

colors = [
    (255, 0, 0),  # Blue
    (0, 255, 0),  # Green
    (0, 0, 255),  # Red
    (0, 255, 255),  # Yellow
]
color_names = ["Blue", "Green", "Red", "Yellow"]

# Update the selected color and sync with session state
selected_color = st.sidebar.radio("Brush Color", color_names, index=0)
st.session_state.colorIndex = color_names.index(selected_color)

# Initialize persistent states
if "paintWindow" not in st.session_state:
    st.session_state.paintWindow = np.ones((471, 636, 3), dtype=np.uint8) * 255

if "points" not in st.session_state:
    st.session_state.points = [deque(maxlen=1024) for _ in range(4)]

# Clear painting action
if st.sidebar.button("Clear Painting"):
    st.session_state.paintWindow[:, :] = 255  # Reset the paint window
    st.session_state.points = [deque(maxlen=1024) for _ in range(4)]  # Clear all points

paintWindow = st.session_state.paintWindow
points = st.session_state.points

# Webcam capture function
def process_frame(cap):
    ret, frame = cap.read()
    if not ret:
        return None
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create mask for marker detection
    lower_hsv = np.array([lower_hue, lower_saturation, lower_value])
    upper_hsv = np.array([upper_hue, upper_saturation, upper_value])
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # Detect contours
    cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center = None

    if len(cnts) > 0:
        cnt = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        M = cv2.moments(cnt)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # Toolbar actions
        if center[1] <= 65:
            if 40 <= center[0] <= 140:  # Clear button (toolbar)
                st.session_state.points = [deque(maxlen=1024) for _ in range(4)]
                paintWindow[:, :] = 255

        else:
            points[st.session_state.colorIndex].appendleft(center)

    # Draw on the paint window
    for i, point_set in enumerate(points):
        for j in range(1, len(point_set)):
            if point_set[j - 1] is not None and point_set[j] is not None:
                cv2.line(frame, point_set[j - 1], point_set[j], colors[i], 2)
                cv2.line(paintWindow, point_set[j - 1], point_set[j], colors[i], 2)

    return frame, mask

# Streamlit video capture display
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    st.error("Could not access the webcam. Please check your device.")
else:
    frame_data = st.empty()  # Placeholder for video feed
    mask_data = st.empty()  # Placeholder for mask
    paint_data = st.empty()  # Placeholder for painting

    stop_webcam = st.sidebar.button("Stop Webcam", key="stop_webcam_button")  # Add a unique key

    while True:
        processed_frame = process_frame(cap)
        if processed_frame is None:
            st.warning("No frame data available. Exiting loop.")
            break

        frame, mask = processed_frame

        # Display outputs with use_container_width
        frame_data.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), caption="Webcam Feed", use_container_width=True)
        mask_data.image(mask, caption="Mask", use_container_width=True)
        paint_data.image(cv2.cvtColor(paintWindow, cv2.COLOR_BGR2RGB), caption="Paint Window", use_container_width=True)

        # Break on Streamlit button or stop condition
        if stop_webcam:
            break

cap.release()
