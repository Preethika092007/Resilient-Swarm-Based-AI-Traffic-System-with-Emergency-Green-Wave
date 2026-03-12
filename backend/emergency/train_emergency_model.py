from ultralytics import YOLO

import os

# helper that fixes mis‑indexed labels in the dataset (class `3` → `1` police)
def fix_labels(dataset_root):
    """Walk each split and rewrite any label line whose first token is 3."""
    total = 0
    for split in ("train", "valid", "test"):
        label_dir = os.path.join(dataset_root, split, "labels")
        if not os.path.isdir(label_dir):
            continue
        for fn in os.listdir(label_dir):
            path = os.path.join(label_dir, fn)
            changed = False
            lines = []
            with open(path, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 0:
                        continue
                    cls = parts[0]
                    if cls == '3':
                        # remap to police (1)
                        parts[0] = '1'
                        changed = True
                        total += 1
                    lines.append(" ".join(parts) + "\n")
            if changed:
                with open(path, 'w') as f:
                    f.writelines(lines)
    return total

# Load pretrained YOLOv8 nano model
model = YOLO('yolov8n.pt')

if __name__ == '__main__':
    # correct labels before training
    dataset_dir = r'D:\urban swarm\datasets\emergency_vehicle_dataset'
    fixed = fix_labels(dataset_dir)
    if fixed:
        print(f"Fixed {fixed} label entries (class 3 -> 1) in dataset.")
        print("You should verify these changes by inspecting the modified .txt files.")
    else:
        print("No mislabeled entries found (class 3). Dataset is clean.")

    # Train the model on emergency vehicle dataset
    print("Starting training on emergency vehicle dataset...")
    print("Classes: ambulance, police, fire_truck")

    results = model.train(
        data=dataset_dir + r'\data.yaml',
        epochs=20,
        imgsz=640,
        batch=8,
        name='emergency_vehicle_train_final',
        patience=10,
        save=True,
        plots=True,
        cache=True,
        augment=True,
        workers=0
    )

    print("\nTraining completed!")
    print("Best model saved at: runs/detect/emergency_vehicle_train/weights/best.pt")
    print("Last model saved at: runs/detect/emergency_vehicle_train/weights/last.pt")
