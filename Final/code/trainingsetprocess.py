import poseembedding as pe                      # 姿态嵌入模块
import poseclassifier as pc                     # 姿态分类器
import extracttrainingsetkeypoints as ek        # 提取训练集关键点特征
import csv
import os

def process_training_set(flag):
    # 定义不同姿态的输出CSV文件夹路径
    csv_output_path = os.path.join(os.path.dirname(__file__), 'fitness_poses_csvs_out')
    pose_files = {
        1: ['push_up.csv', 'push_down.csv'],
        2: ['squat_up.csv', 'squat_down.csv'],
        3: ['pull_up.csv', 'pull_down.csv']
    }

    # 检查指定的CSV文件是否已存在，若存在则跳过重处理
    if all(os.path.isfile(os.path.join(csv_output_path, fname)) for fname in pose_files.get(flag, [])):
        return

    # 定义输入和输出数据的路径
    images_input_folder = 'fitness_poses_images_in'
    images_output_folder = 'fitness_poses_images_out'
    csv_output_folder = 'fitness_poses_csvs_out'

    # 初始化用于引导过程的辅助工具
    bootstrap_helper = ek.BootstrapHelper(
        images_in_folder=images_input_folder,
        images_out_folder=images_output_folder,
        csvs_out_folder=csv_output_folder,
    )

    # 显示输入图像的统计信息
    bootstrap_helper.print_images_in_statistics()

    # 对所有图像进行引导处理，调试目的设置为None以无限制
    bootstrap_helper.bootstrap(per_pose_class_limit=None)

    # 显示输出图像的统计信息，并对CSV与图像进行对齐，移除任何异常值
    bootstrap_helper.align_images_and_csvs(print_removed_items=False)
    bootstrap_helper.print_images_out_statistics()

    # 建议在此进行预测的手动验证以确保准确性

    # 根据姿态分类自动检测和移除异常值的过程
    pose_embedder = pe.FullBodyPoseEmbedder()
    pose_classifier = pc.PoseClassifier(
        pose_samples_folder=csv_output_folder,
        pose_embedder=pose_embedder,
        top_n_by_max_distance=30,
        top_n_by_mean_distance=10)

    outliers = pose_classifier.find_pose_sample_outliers()
    print('异常值数量: ', len(outliers))

    # 移除检测到的异常值，并重新对齐CSV与图像
    bootstrap_helper.remove_outliers(outliers)
    bootstrap_helper.align_images_and_csvs(print_removed_items=False)
    bootstrap_helper.print_images_out_statistics()

# `dump_for_the_app`函数用于演示，并当前被注释掉。
