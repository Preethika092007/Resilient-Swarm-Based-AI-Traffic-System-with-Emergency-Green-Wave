import os
import shutil
from collections import defaultdict

dataset_root = r'D:\urban swarm\datasets\emergency_vehicle_dataset'
train_images = os.path.join(dataset_root, 'train', 'images')
train_labels = os.path.join(dataset_root, 'train', 'labels')

# Create balanced backup folder
balanced_backup = os.path.join(dataset_root, 'train_imbalanced_backup')
os.makedirs(os.path.join(balanced_backup, 'images'), exist_ok=True)
os.makedirs(os.path.join(balanced_backup, 'labels'), exist_ok=True)

# Categorize images by class
class_images = defaultdict(list)

print("Analyzing dataset...")
for label_file in os.listdir(train_labels):
    if not label_file.endswith('.txt'):
        continue
    
    label_path = os.path.join(train_labels, label_file)
    
    with open(label_path, 'r') as f:
        lines = f.readlines()
        if len(lines) > 0:
            first_line = lines[0].strip().split()
            if len(first_line) > 0:
                cls = int(first_line[0])
                image_name = label_file.replace('.txt', '.jpg')
                class_images[cls].append((image_name, label_file))

print(f"\nCurrent distribution:")
print(f"  Class 0 (ambulance): {len(class_images[0])} images")
print(f"  Class 1 (police): {len(class_images[1])} images")

# Keep only 1500 ambulances (to balance with police)
target_per_class = 1500
moved = 0

print(f"\nBalancing to {target_per_class} images per class...")

for cls in [0, 1]:
    if len(class_images[cls]) > target_per_class:
        # Move excess to backup
        excess = class_images[cls][target_per_class:]
        for img_name, lbl_name in excess:
            # Move image
            img_src = os.path.join(train_images, img_name)
            img_dst = os.path.join(balanced_backup, 'images', img_name)
            if os.path.exists(img_src):
                shutil.move(img_src, img_dst)
            
            # Move label
            lbl_src = os.path.join(train_labels, lbl_name)
            lbl_dst = os.path.join(balanced_backup, 'labels', lbl_name)
            if os.path.exists(lbl_src):
                shutil.move(lbl_src, lbl_dst)
            
            moved += 1

print(f"\nBalanced dataset created!")
print(f"  Moved {moved} excess images to backup")
print(f"  New distribution: ~{target_per_class} ambulances, ~{target_per_class} police")
print(f"\nNow retrain with: python train_emergency_model.py")
