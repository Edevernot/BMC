import datetime
import os
import cv2
from mediapipe.python.solutions import drawing_utils as mp_drawing
from mediapipe.python.solutions import pose as mp_pose

# 定义全局变量
output_dir = './video-output'
class_names = ['push_down', 'squat_down', 'pull_up']


def prepare_output_dir():
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir


def get_video_output_path(action_name):
    mkfile_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    return os.path.join(output_dir, f'{action_name}-sample-out-{mkfile_time}.mp4')


def setup_pose_processing():
    pose_tracker = mp_pose.Pose()
    return pose_tracker


def process_video_input(flag, video_input_path):
    prepare_output_dir()
    class_name = class_names[flag - 1] if flag in [1, 2, 3] else 'unknown'
    video_output_path = get_video_output_path(class_name)

    video_cap = cv2.VideoCapture(video_input_path)
    if not video_cap.isOpened():
        print("Error: Could not open video.")
        return

    video_fps = video_cap.get(cv2.CAP_PROP_FPS)
    video_width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out_video = cv2.VideoWriter(video_output_path, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), video_fps,
                                (video_width, video_height))

    pose_tracker = setup_pose_processing()

    while video_cap.isOpened():
        ret, frame = video_cap.read()
        if not ret:
            break

        # Convert the BGR image to RGB.
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image and draw landmarks
        results = pose_tracker.process(frame_rgb)
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        out_video.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_cap.release()
    out_video.release()
    print(f"Processed video saved at {video_output_path}")



