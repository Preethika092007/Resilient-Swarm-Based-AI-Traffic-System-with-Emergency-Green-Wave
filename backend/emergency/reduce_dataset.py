import os
import shutil
from collections import defaultdict

# Paths
dataset_root = r'D:\urban swarm\datasets\emergency_vehicle_dataset'
train_images = os.path.join(dataset_root, 'train', 'images')
train_labels = os.path.join(dataset_root, 'train', 'labels')

# Backup folder
backup_folder = os.path.join(dataset_root, 'train_backup')
os.makedirs(backup_folder, exist_ok=True)
os.makedirs(os.path.join(backup_folder, 'images'), exist_ok=True)
os.makedirs(os.path.join(backup_folder, 'labels'), exist_ok=True)

# Class names
class_names = {0: 'ambulance', 1: 'police', 2: 'fire_truck'}

# Count images per class
class_images = defaultdict(list)

print("Analyzing dataset...")

# Read all label files and categorize by class
for label_file in os.listdir(train_labels):
    if not label_file.endswith('.txt'):
        continue
    
    label_path = os.path.join(train_labels, label_file)
    
    with open(label_path, 'r') as f:
        lines = f.readlines()
        if len(lines) > 0:
            # Get the first class in the file
            first_line = lines[0].strip().split()
            if len(first_line) > 0:
                cls = int(first_line[0])
                image_name = label_file.replace('.txt', '.jpg')
                class_images[cls].append((image_name, label_file))

# Print current distribution
print("\nCurrent dataset distribution:")
for cls, images in class_images.items():
    print(f"  Class {cls} ({class_names.get(cls, 'unknown')}): {len(images)} images")

# Keep only first 300 images per class
images_per_class = 300
kept_images = set()
moved_count = 0

print(f"\nKeeping {images_per_class} images per class...")

for cls, images in class_images.items():
    # Keep first 100 images
    keep = images[:images_per_class]
    for img_name, lbl_name in keep:
        kept_images.add(img_name)
    
    # Move the rest to backup
    remove = images[images_per_class:]
    for img_name, lbl_name in remove:
        # Move image
        img_src = os.path.join(train_images, img_name)
        img_dst = os.path.join(backup_folder, 'images', img_name)
        if os.path.exists(img_src):
            shutil.move(img_src, img_dst)
        
        # Move label
        lbl_src = os.path.join(train_labels, lbl_name)
        lbl_dst = os.path.join(backup_folder, 'labels', lbl_name)
        if os.path.exists(lbl_src):
            shutil.move(lbl_src, lbl_dst)
        
        moved_count += 1

print(f"\n✅ Dataset reduced!")
print(f"   Kept: {len(kept_images)} images")
print(f"   Moved to backup: {moved_count} images")
print(f"   Backup location: {backup_folder}")

print("\nNew dataset distribution:")
for cls in class_images.keys():
    remaining = min(len(class_images[cls]), images_per_class)
    print(f"  Class {cls} ({class_names.get(cls, 'unknown')}): {remaining} images")

print("\n🚀 You can now train much faster!")
print("   Run: python train_emergency_model.py")
