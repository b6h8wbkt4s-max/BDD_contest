import pandas as pd

gt = pd.read_csv(r"D:\11ljx-work\BDD_contest\val_gt.csv")
pred = pd.read_csv(r"D:\11ljx-work\BDD_contest\val_pred_yolo26.csv")

# 按 image_name 对齐
merged = pd.merge(gt, pred, on='image_name', suffixes=('_gt', '_pred'))
print(f"对比图片数: {len(merged)}")

total = len(merged)
mp = (merged['people_num_gt'] == merged['people_num_pred']).sum()
mv = (merged['vehicle_num_gt'] == merged['vehicle_num_pred']).sum()
mb = ((merged['people_num_gt'] == merged['people_num_pred']) &
      (merged['vehicle_num_gt'] == merged['vehicle_num_pred'])).sum()

print(f"People 匹配: {mp}/{total} = {mp/total:.2%}")
print(f"Vehicle 匹配: {mv}/{total} = {mv/total:.2%}")
print(f"Overall accuracy: {mb/total:.2%}")