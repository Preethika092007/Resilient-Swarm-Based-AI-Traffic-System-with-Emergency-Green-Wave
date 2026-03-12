import os
from collections import Counter

# Paths
dataset_root = r'D:\urban swarm\datasets\emergency_vehicle_dataset'
train_labels = os.path.join(dataset_root, 'train', 'labels')

# Count all class IDs
all_classes = []

print("Analyzing all label files...")

for label_file in os.listdir(train_labels):
    if not label_file.endswith('.txt'):
        continue
    
    label_path = os.path.join(train_labels, label_file)
    
    with open(label_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split()
            if len(parts) > 0:
                cls = parts[0]
                all_classes.append(cls)

# Count occurrences
class_counts = Counter(all_classes)

print("\n📊 All class IDs found in dataset:")
for cls, count in sorted(class_counts.items()):
    print(f"   Class {cls}: {count} instances")

print("\n💡 Expected mapping:")
print("   0 → ambulance")
print("   1 → police")
print("   2 → fire_truck")

if '3' in class_counts:
    print("\n⚠️ WARNING: Class ID '3' found in dataset!")
    print("   This might be mislabeled fire trucks.")
    print("   The training script should fix this automatically.")
