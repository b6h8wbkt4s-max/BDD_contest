import os
import random
from shutil import copyfile

# ========== 配置区 ==========
# 转换后的图片和标签路径（原始位置）
IMAGE_FOLDER = r"D:\11ljx-work\BDD_contest\trainA\images"
TXT_FOLDER   = r"D:\11ljx-work\BDD_contest\trainA\labels"

# 输出路径（划分后放这里）
OUTPUT_FOLDER = r"D:\11ljx-work\BDD_contest\datasets"

# 划分比例：训练 80% / 验证 10% / 测试 10%
SPLIT_RATIO = (0.8, 0.1, 0.1)

# 随机种子，保证每次划分结果一致
RANDOM_SEED = 42
# ============================

random.seed(RANDOM_SEED)


def split_dataset(image_folder, txt_folder, output_folder, split_ratio):
    # 创建输出目录
    for phase in ['train', 'val', 'test']:
        os.makedirs(os.path.join(output_folder, 'images', phase), exist_ok=True)
        os.makedirs(os.path.join(output_folder, 'labels', phase), exist_ok=True)

    # 只取同时有图片和标签的样本
    image_files = [f for f in os.listdir(image_folder)
                   if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    # 过滤掉没有对应标签的图片
    valid_files = []
    for img in image_files:
        txt_name = os.path.splitext(img)[0] + '.txt'
        if os.path.exists(os.path.join(txt_folder, txt_name)):
            valid_files.append(img)

    print(f"图片总数: {len(image_files)}，有对应标签的: {len(valid_files)}")

    random.shuffle(valid_files)
    num_images = len(valid_files)
    num_train = int(split_ratio[0] * num_images)
    num_val   = int(split_ratio[1] * num_images)

    train_images = valid_files[:num_train]
    val_images   = valid_files[num_train:num_train + num_val]
    test_images  = valid_files[num_train + num_val:]

    print(f"训练集: {len(train_images)}")
    print(f"验证集: {len(val_images)}")
    print(f"测试集: {len(test_images)}")

    for phase, images_list in zip(['train', 'val', 'test'],
                                  [train_images, val_images, test_images]):
        for idx, image_file in enumerate(images_list):
            # 复制图片
            src_img = os.path.join(image_folder, image_file)
            dst_img = os.path.join(output_folder, 'images', phase, image_file)
            copyfile(src_img, dst_img)

            # 复制标签
            txt_name = os.path.splitext(image_file)[0] + '.txt'
            src_txt  = os.path.join(txt_folder, txt_name)
            dst_txt  = os.path.join(output_folder, 'labels', phase, txt_name)
            if os.path.exists(src_txt):
                copyfile(src_txt, dst_txt)

            if (idx + 1) % 2000 == 0:
                print(f"[{phase}] 已复制 {idx + 1}/{len(images_list)}")


if __name__ == "__main__":
    split_dataset(IMAGE_FOLDER, TXT_FOLDER, OUTPUT_FOLDER, SPLIT_RATIO)
    print("划分完成！")