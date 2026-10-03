import os
import re
import pandas as pd

LABEL_DIR = r"D:\11ljx-work\BDD_contest\datasets\labels\val"
OUTPUT_CSV = r"D:\11ljx-work\BDD_contest\val_gt.csv"


def natural_sort_key(s):
    return [int(t) if t.isdigit() else t.lower()
            for t in re.split(r'([0-9]+)', s)]


def main():
    files = [f for f in os.listdir(LABEL_DIR) if f.endswith('.txt')]
    files = sorted(files, key=natural_sort_key)
    results = []
    for f in files:
        people_num = 0
        vehicle_num = 0
        with open(os.path.join(LABEL_DIR, f), 'r') as fp:
            for line in fp:
                parts = line.strip().split()
                if len(parts) < 5:
                    continue
                cls = int(float(parts[0]))
                if cls in [3, 8]:
                    people_num += 1
                elif cls in [0, 4, 5, 6, 7]:
                    vehicle_num += 1
        results.append({
            'image_name': os.path.splitext(f)[0],
            'people_num': people_num,
            'vehicle_num': vehicle_num
        })
    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"生成 {len(df)} 行, 保存到 {OUTPUT_CSV}")
    print(df.head(10))


if __name__ == "__main__":
    main()