import os
import re
import pandas as pd

IMAGE_DIR = r"D:\11ljx-work\BDD_contest\datasets\images\val"
LABEL_DIR = r"C:\Users\WULIANG\runs\detect\predict\labels"    # ⚠️ 确认是 exp3
OUTPUT_CSV = r"D:\11ljx-work\BDD_contest\val_pred_yolo26.csv"


def natural_sort_key(s):
    return [int(t) if t.isdigit() else t.lower()
            for t in re.split(r'([0-9]+)', s)]


def main():
    files = [f for f in os.listdir(IMAGE_DIR)
             if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    names = sorted([os.path.splitext(f)[0] for f in files], key=natural_sort_key)
    results = []
    missing = 0
    for name in names:
        p = os.path.join(LABEL_DIR, name + '.txt')
        people_num = 0
        vehicle_num = 0
        if os.path.exists(p):
            with open(p, 'r') as fp:
                for line in fp:
                    parts = line.strip().split()
                    if len(parts) < 5:
                        continue
                    cls = int(float(parts[0]))
                    if cls in [3, 8]:
                        people_num += 1
                    elif cls in [0, 4, 5, 6, 7]:
                        vehicle_num += 1
        else:
            missing += 1
        results.append({'image_name': name,
                        'people_num': people_num,
                        'vehicle_num': vehicle_num})
    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"生成 {len(df)} 行（{missing} 张无目标）, 保存到 {OUTPUT_CSV}")
    print(df.head(10))


if __name__ == "__main__":
    main()