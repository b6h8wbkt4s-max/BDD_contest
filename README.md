# BDD_contest - 行人车辆检测与计数

2024 一带一路大赛训练项目：基于 BDD100K 数据集的行人与车辆检测及计数。

## 项目结构

- `scripts/` - 数据转换、划分、推理后处理脚本
- `config/` - YOLOv5 数据集配置文件
- `models/` - 训练好的模型权重
- `docs/` - 项目文档

## 环境

- Python 3.9
- PyTorch 1.8.2 + CUDA 11.1
- YOLOv5 v6.2
- NumPy 1.23
- Pillow 9.5.0

## 数据集

BDD100K trainA：35644 张训练图 + 1000 张测试图

## 流程

1. **标签转换**：`python scripts/labels_convert.py`
   - BDD100K 像素坐标 → YOLO 归一化格式
2. **数据集划分**：`python scripts/split_data.py`
   - 训练:验证:测试 = 8:1:1
3. **训练**：python train.py --data data/bdd_traina.yaml --epochs 30 --batch-size 12 --device 0 --workers 2
4. **推理**：
python detect.py --weights runs/train/exp11/weights/best.pt --source ../datasets/images/val --save-txt --save-conf
5. **统计 + 评分**：
python scripts/make_gt.py
python scripts/make_pred.py
python scripts/accuracy_val.py


## 结果

| 指标 | 值 |
|------|-----|
| mAP@.5 | 0.541 |
| mAP@.5:.95 | 0.293 |
| People 计数准确率 | 68.29% |
| Vehicle 计数准确率 | 20.96% |
| Overall accuracy | 14.06% |

## 改进方向

- 增加 epochs（30 → 100）
- 换更大模型（YOLOv5m/l/x）
- 数据增强
- YOLOv8 + DeepSORT 跟踪计数