import os
import shutil

TRAIN_A = r"D:\11ljx-work\BDD_contest\trainA"

# 图片多套了一层：trainA\images\trainA\*.jpg  ->  trainA\images\*.jpg
NESTED_IMG_DIR = os.path.join(TRAIN_A, "images", "trainA")
TARGET_IMG_DIR = os.path.join(TRAIN_A, "images")

print("=" * 50)
print("整理图片：把嵌套的 jpg 提上来")
print("=" * 50)

if os.path.exists(NESTED_IMG_DIR):
    moved = 0
    for f in os.listdir(NESTED_IMG_DIR):
        if f.lower().endswith((".jpg", ".jpeg", ".png")):
            src = os.path.join(NESTED_IMG_DIR, f)
            dst = os.path.join(TARGET_IMG_DIR, f)
            if not os.path.exists(dst):
                shutil.move(src, dst)
                moved += 1
    print(f"移动了 {moved} 张图片")

    # 删掉空文件夹
    if not os.listdir(NESTED_IMG_DIR):
        os.rmdir(NESTED_IMG_DIR)
        print("已删除空文件夹 trainA\\images\\trainA")
else:
    print(f"未找到嵌套文件夹: {NESTED_IMG_DIR}")
    print("可能已经整理过，跳过")

print("\n" + "=" * 50)
print("整理后数量统计")
print("=" * 50)

img_dir = os.path.join(TRAIN_A, "images")
lbl_dir = os.path.join(TRAIN_A, "labels")
test_dir = os.path.join(TRAIN_A, "test")

img_count = len([f for f in os.listdir(img_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))])
lbl_count = len([f for f in os.listdir(lbl_dir) if f.endswith(".txt")])
test_count = len([f for f in os.listdir(test_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]) if os.path.exists(test_dir) else 0

print(f"images: {img_count} 张")
print(f"labels: {lbl_count} 个")
print(f"test:   {test_count} 张")