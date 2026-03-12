import os

dataset_root = r'D:\urban swarm\datasets\emergency_vehicle_dataset'

# Keywords that indicate fire truck in filename
fire_keywords = ['fire', 'firetruck', 'fire_truck', 'fire-truck', 'fireengine', 'fire_engine']

folders = [
    os.path.join(dataset_root, 'train', 'labels'),
    os.path.join(dataset_root, 'valid', 'labels'),
    os.path.join(dataset_root, 'test', 'labels')
]

total_relabeled = 0

for folder in folders:
    if not os.path.exists(folder):
        continue
    
    print(f"\nProcessing: {folder}")
    relabeled = 0
    
    for label_file in os.listdir(folder):
        if not label_file.endswith('.txt'):
            continue
        
        # Check if filename contains fire truck keywords
        filename_lower = label_file.lower()
        is_fire_truck = any(keyword in filename_lower for keyword in fire_keywords)
        
        if not is_fire_truck:
            continue
        
        label_path = os.path.join(folder, label_file)
        
        with open(label_path, 'r') as f:
            lines = f.readlines()
        
        # Change class 0 (ambulance) to class 2 (fire_truck)
        new_lines = []
        changed = False
        for line in lines:
            parts = line.strip().split()
            if len(parts) > 0 and parts[0] == '0':
                parts[0] = '2'
                changed = True
                relabeled += 1
            new_lines.append(' '.join(parts) + '\n')
        
        # Write back if changed
        if changed:
            with open(label_path, 'w') as f:
                f.writelines(new_lines)
            print(f"  Relabeled: {label_file}")
    
    print(f"  Total relabeled in this folder: {relabeled}")
    total_relabeled += relabeled

print(f"\n{'='*60}")
print(f"Total fire truck labels created: {total_relabeled}")
print(f"{'='*60}")

if total_relabeled > 0:
    print("\nNow update data.yaml to 3 classes and retrain!")
else:
    print("\nNo fire truck images found by filename.")
    print("Fire truck images don't have 'fire' in their filenames.")
    print("Manual relabeling would be required.")
