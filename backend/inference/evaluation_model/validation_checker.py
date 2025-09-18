import os
import torch
import torch.nn as nn
import pandas as pd
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import torch.nn.functional as F
from sklearn.model_selection import train_test_split

# --- Dataset Class ---
class ValidationDataset(Dataset):
    def __init__(self, image_dir, transform=None, csv_data=None):
        self.image_dir = image_dir
        self.transform = transform
        # Build full image paths from filenames in CSV
        self.image_paths = [os.path.join(image_dir, fname) for fname in csv_data['filename']]
        self.labels = csv_data['label'].tolist()

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        label = self.labels[idx]
        image = Image.open(image_path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image, label

# --- Model ---
class ValidationChecker(nn.Module):
    def __init__(self):
        super(ValidationChecker, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(0.25)

        # Adjust fully-connected layer to match 224x224 -> (224/4)x(224/4) = 56x56
        self.fc1 = nn.Linear(64 * 56 * 56, 128)
        self.fc2 = nn.Linear(128, 2)  # Binary (Valid=0, Invalid=1)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))  # -> [32, 112, 112]
        x = self.pool(F.relu(self.conv2(x)))  # -> [64, 56, 56]
        x = x.view(x.size(0), -1)             # flatten
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

# --- Transforms ---
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# --- Label Cleaning ---
def clean_labels(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df.rename(columns={"name": "filename", "label": "label"}, inplace=True)
    return df

# --- Main ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if __name__ == "__main__":
    print("Using device:", device)
    image_dir = "./dataset/validation_checker"  # All images are inside this folder
    csv_path = "./dataset/validation_label.csv"

    df = pd.read_csv(csv_path)
    df = clean_labels(df)

    # --- Auto Train/Test Split (80-20) ---
    train_df, test_df = train_test_split(
        df,
        test_size=0.2,
        stratify=df['label'],
        random_state=42
    )

    # Create datasets directly from the split dataframes
    train_dataset = ValidationDataset(image_dir, transform, train_df)
    test_dataset = ValidationDataset(image_dir, transform, test_df)

    # DataLoaders
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4, pin_memory=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=4, pin_memory=True)

    # Model, Loss, Optimizer
    model = ValidationChecker().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    epochs = 20
    best_acc = 0.0

    for epoch in range(epochs):
        # --- Train ---
        model.train()
        running_loss, correct, total = 0.0, 0, 0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        train_loss = running_loss / len(train_loader)
        train_acc = 100 * correct / total

        # --- Validate ---
        model.eval()
        test_loss, correct, total = 0.0, 0, 0
        with torch.inference_mode():
            for images, labels in test_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                test_loss += loss.item()
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        test_loss /= len(test_loader)
        test_acc = 100 * correct / total

        print(f"Epoch {epoch+1}/{epochs}")
        print(f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}% | "
              f"Test Loss: {test_loss:.4f}, Test Acc: {test_acc:.2f}%")

        # Save best model
        if test_acc > best_acc:
            best_acc = test_acc
            torch.save(model.state_dict(), "./saved_models/best_validation_checker.pth")
            print(f"✅ Saved new best model with acc {best_acc:.2f}%")

    print("✅ Training finished")
