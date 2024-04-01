import datetime
import os
import cv2
import numpy as np
from mediapipe.python.solutions import drawing_utils as mp_drawing
from mediapipe.python.solutions import pose as mp_pose
import poseembedding as pe
import poseclassifier as pc
import resultsmooth as rs
import counter
import visualizer as vs


def initialize_components(class_name):
    """初始化所需组件"""
    pose_tracker = mp_pose.Pose()
    pose_embedder = pe.FullBodyPoseEmbedder()
    pose_classifier = pc.PoseClassifier(
        pose_samples_folder='fitness_poses_csvs_out',
        class_name=class_name,
        pose_embedder=pose_embedder,
        top_n_by_max_distance=30,
        top_n_by_mean_distance=10)
    pose_classification_filter = rs.EMADictSmoothing(window_size=10, alpha=0.2)
    repetition_counter = counter.RepetitionCounter(class_name=class_name, enter_threshold=5, exit_threshold=4)
    pose_classification_visualizer = vs.PoseClassificationVisualizer(class_name=class_name, plot_y_max=10)

    return pose_tracker, pose_classifier, pose_classification_filter, repetition_counter, pose_classification_visualizer


def process_video(frame, components):
    """处理单帧视频"""
    pose_tracker, pose_classifier, pose_classification_filter, repetition_counter, pose_classification_visualizer = components
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose_tracker.process(image=frame_rgb)
    pose_landmarks = result.pose_landmarks
    output_frame = frame_rgb.copy()

    if pose_landmarks:
        mp_drawing.draw_landmarks(image=output_frame, landmark_list=pose_landmarks,
                                  connections=mp_pose.POSE_CONNECTIONS)
        pose_landmarks = np.array([[lmk.x * frame.shape[1], lmk.y * frame.shape[0], lmk.z * frame.shape[1]]
                                   for lmk in pose_landmarks.landmark], dtype=np.float32)
        pose_classification = pose_classifier(pose_landmarks)
        pose_classification_filtered = pose_classification_filter(pose_classification)
        repetitions_count = repetition_counter(pose_classification_filtered)
    else:
        pose_classification_filtered = None
        repetitions_count = repetition_counter.n_repeats

    output_frame = pose_classification_visualizer(frame=output_frame,
                                                  pose_classification=None,
                                                  pose_classification_filtered=pose_classification_filtered,
                                                  repetitions_count=repetitions_count)
    return cv2.cvtColor(np.array(output_frame), cv2.COLOR_RGB2BGR)


def process(flag):
    """主函数"""
    mkfile_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H-%M-%S')
    output_dir = './video-output'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    class_names = ['push_down', 'squat_down', 'pull_up']
    class_name = class_names[flag - 1]
    out_video_path = f'{output_dir}/{class_name}-sample-out-{mkfile_time}.mp4'

    video_cap = cv2.VideoCapture(0)
    out_video = cv2.VideoWriter(out_video_path, cv2.VideoWriter_fourcc(*'mp4v'), 24, (640, 480))
    components = initialize_components(class_name)

    while video_cap.isOpened():
        success, frame = video_cap.read()
        if not success:
            break

        processed_frame = process_video(frame, components)
        cv2.imshow('video', processed_frame)
        out_video.write(processed_frame)

        if cv2.waitKey(1) in [ord('q'), 27]:
            break

    video_cap.release()
    out_video.release()
    cv2.destroyAllWindows()
    for component in components[:-1]:  # MediaPipe pose tracker resource release
        component.close()
    print(f"视频处理结束，输出保存在{out_video_path}")


