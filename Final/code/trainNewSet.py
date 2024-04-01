# TrainNewSet.py

from extracttrainingsetkeypoints import BootstrapHelper


# 在给定文件夹中引导图像
# 文件夹中的所需图像:
# squat_up /
#     image_001.jpg
#     image_002.jpg
#     ...
#
# squat_down /
#     image_001.jpg
#     image_002.jpg
#     ...

# 生成的CSV输出文件夹：
#     pushups_up.csv
#     pushups_down.csv

# 生成的带有姿势的3D landmarks的CSV结构：
#     sample_00001, x1, y1, z1, x2, y2, z2, ....
#     sample_00002, x1, y1, z1, x2, y2, z2, ....
def train_new_set(images_in_folder, images_out_folder, csvs_out_folder):
    # 初始化 BootstrapHelper
    bootstrap_helper = BootstrapHelper(
        images_in_folder=images_in_folder,
        images_out_folder=images_out_folder,
        csvs_out_folder=csvs_out_folder
    )

    # 引导训练集
    bootstrap_helper.bootstrap()

    # 生成统计信息以验证处理结果
    bootstrap_helper.print_images_in_statistics()
    bootstrap_helper.print_images_out_statistics()

    # 确保图像文件夹和 CSV 文件具有相同的样本
    bootstrap_helper.align_images_and_csvs(print_removed_items=True)


if __name__ == "__main__":
    # 指定图像和CSV文件的输入输出路径
    bootstrap_images_in_folder = 'fitness_poses_images_in'  # 输入图片文件夹路径
    bootstrap_images_out_folder = 'fitness_poses_images_out'  # 输出图片文件夹路径
    bootstrap_csvs_out_folder = 'fitness_poses_csvs_out'  # 输出CSV 文件夹路径

    train_new_set(bootstrap_images_in_folder, bootstrap_images_out_folder, bootstrap_csvs_out_folder)
