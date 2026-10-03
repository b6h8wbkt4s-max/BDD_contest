import os
import re
import pandas as pd

# ========== 配置区 ==========
IMAGE_DIR = r"D:\11ljx-work\BDD_contest\datasets\images\test"
LABEL_DIR = r"D:\11ljx-work\BDD_contest\yolov5-6.2\runs\detect\exp2\labels"
OUTPUT_CSV = r"D:\11ljx-work\BDD_contest\test_submission.csv"
# ============================


def natural_sort_key(s):
    """自然排序，让 train_A_2 排在 train_A_10 前面"""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'([0-9]+)', s)]


def summarize_labels(image_dir, label_dir, output_csv):
    # 1. 拿到所有测试图片名（不带后缀），并按自然序排
    image_files = [f for f in os.listdir(image_dir)
                   if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    image_names = sorted([os.path.splitext(f)[0] for f in image_files],
                         key=natural_sort_key)

    print(f"测试集图片总数: {len(image_names)}")

    results = []
    missing = 0
    for image_name in image_names:
        label_path = os.path.join(label_dir, image_name + '.txt')
        people_num = 0
        vehicle_num = 0

        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) < 5:
                        continue
                    cls = int(float(parts[0]))
                    # people = person(3) + rider(8)
                    if cls in [3, 8]:
                        people_num += 1
                    # vehicle = bus(0) + bike(4) + truck(5) + motor(6) + car(7)
                    elif cls in [0, 4, 5, 6, 7]:
                        vehicle_num += 1
        else:
            missing += 1  # 没检测到目标的图，计数为 0

        results.append({
            'image_name': image_name,
            'people_num': people_num,
            'vehicle_num': vehicle_num
        })

    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)
    print(f"共处理 {len(results)} 张图，其中 {missing} 张图无检测目标（计数为 0）")
    print(f"CSV 已保存到: {output_csv}")
    print(df.head(10))


if __name__ == "__main__":
    summarize_labels(IMAGE_DIR, LABEL_DIR, OUTPUT_CSV)