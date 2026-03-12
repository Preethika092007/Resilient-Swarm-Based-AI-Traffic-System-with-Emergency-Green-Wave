import os

dataset_root = r'D:\urban swarm\datasets\emergency_vehicle_dataset'

folders = [
    os.path.join(dataset_root, 'train', 'labels'),
    os.path.join(dataset_root, 'valid', 'labels'),
    os.path.join(dataset_root, 'test', 'labels')
]

total_removed = 0

for folder in folders:
    if not os.path.exists(folder):
        continue
    
    print(f"\nProcessing: {folder}")
    removed = 0
    
    for label_file in os.listdir(folder):
        if not label_file.endswith('.txt'):
            continue
        
        label_path = os.path.join(folder, label_file)
        
        with open(label_path, 'r') as f:
            lines = f.readlines()
        
        # Filter out class 2 (fire_truck)
        new_lines = []
        changed = False
        for line in lines:
            parts = line.strip().split()
            if len(parts) > 0 and parts[0] == '2':
                changed = True
                removed += 1
            else:
                new_lines.append(line)
        
        # Write back if changed
        if changed:
            with open(label_path, 'w') as f:
                f.writelines(new_lines)
    
    print(f"  Removed {removed} class 2 labels")
    total_removed += removed

print(f"\n✅ Total removed: {total_removed} fire_truck labels")
print("Dataset is now ready for 2-class training (ambulance + police)")
