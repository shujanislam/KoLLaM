# model_stage2.py
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models

device = "cuda" if torch.cuda.is_available() else "cpu"

# Reuse same transforms
train_tfms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])
val_tfms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

def train_model(model, criterion, optimizer, train_loader, val_loader, num_epochs=10):
    model.to(device)
    for epoch in range(num_epochs):
        model.train()
        correct, total = 0, 0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

        print(f"Epoch {epoch+1}/{num_epochs} - Train Acc: {correct/total:.4f}")

    return model

def train_stage2(data_dir="Dataset/Stage2", save_path="saved_models/model_stage2.pth"):
    train_set = datasets.ImageFolder(f"{data_dir}/train", transform=train_tfms)
    val_set = datasets.ImageFolder(f"{data_dir}/val", transform=val_tfms)

    train_loader = DataLoader(train_set, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=32, shuffle=False)

    model = models.resnet18(pretrained=True)
    model.fc = nn.Linear(model.fc.in_features, 2)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    model = train_model(model, criterion, optimizer, train_loader, val_loader, num_epochs=10)
    torch.save(model.state_dict(), save_path)
    print(f"Stage 2 model saved at {save_path}")
