import os

# ========== 配置区 ==========
IMG_WIDTH  = 1280
IMG_HEIGHT = 720
LABEL_DIR = r"D:\11ljx-work\BDD_contest\trainA\labels"
# ============================


def convert_bbox_to_yolo_format(x_min, y_min, x_max, y_max, img_w, img_h):
    x_center = ((x_min + x_max) / 2) / img_w
    y_center = ((y_min + y_max) / 2) / img_h
    width    = (x_max - x_min) / img_w
    height   = (y_max - y_min) / img_h
    return x_center, y_center, width, height


def is_valid(xc, yc, w, h):
    """检查转换结果是否在 0~1 之间"""
    return 0 <= xc <= 1 and 0 <= yc <= 1 and 0 < w <= 1 and 0 < h <= 1


def process_label_files(label_dir):
    files = [f for f in os.listdir(label_dir) if f.endswith('.txt')]
    total = len(files)
    print(f"共发现 {total} 个标签文件，开始转换...")

    converted = 0
    skipped_boxes = 0
    for idx, label_file in enumerate(files):
        file_path = os.path.join(label_dir, label_file)
        with open(file_path, 'r') as file:
            lines = file.readlines()

        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) != 5:
                continue
            try:
                cls, x_min, y_min, x_max, y_max = map(float, parts)

                # ⚠️ 关键检查：如果值已经小于 1，说明已经转换过了，跳过
                if max(x_min, y_min, x_max, y_max) <= 1.0:
                    print(f"[跳过] {label_file}：已经是归一化格式，无需再转")
                    return

                xc, yc, w, h = convert_bbox_to_yolo_format(
                    x_min, y_min, x_max, y_max, IMG_WIDTH, IMG_HEIGHT
                )

                if not is_valid(xc, yc, w, h):
                    skipped_boxes += 1
                    continue

                new_lines.append(f"{int(cls)} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}\n")
            except Exception as e:
                print(f"[警告] {label_file} 解析失败: {e}")

        with open(file_path, 'w') as file:
            file.writelines(new_lines)

        converted += 1
        if converted % 5000 == 0:
            print(f"已转换 {converted}/{total}")

    print(f"转换完成！跳过了 {skipped_boxes} 个越界框")


if __name__ == "__main__":
    process_label_files(LABEL_DIR)