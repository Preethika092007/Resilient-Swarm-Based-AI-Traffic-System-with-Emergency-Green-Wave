import os
from collections import Counter

dataset_root = r'D:\urban swarm\datasets\emergency_vehicle_dataset'

# Check all folders
folders_to_check = [
    os.path.join(dataset_root, 'train', 'labels'),
    os.path.join(dataset_root, 'valid', 'labels'),
    os.path.join(dataset_root, 'test', 'labels'),
    os.path.join(dataset_root, 'train_backup', 'labels')
]

for folder in folders_to_check:
    if not os.path.exists(folder):
        continue
    
    print(f"\n{'='*60}")
    print(f"Analyzing: {folder}")
    print('='*60)
    
    class_counts = Counter()
    total_files = 0
    
    for label_file in os.listdir(folder):
        if not label_file.endswith('.txt'):
            continue
        
        total_files += 1
        label_path = os.path.join(folder, label_file)
        
        with open(label_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split()
                if len(parts) > 0:
                    cls = parts[0]
                    class_counts[cls] += 1
    
    print(f"Total label files: {total_files}")
    print(f"\nClass distribution:")
    for cls in sorted(class_counts.keys()):
        count = class_counts[cls]
        class_name = {
            '0': 'ambulance',
            '1': 'police', 
            '2': 'fire_truck',
            '3': 'unknown/mislabeled'
        }.get(cls, f'unknown-{cls}')
        print(f"  Class {cls} ({class_name}): {count} instances")

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print("\nThe fire truck images are likely labeled as class 0 or 1 by mistake.")
print("You need to manually check and relabel them, or get a properly labeled dataset.")
