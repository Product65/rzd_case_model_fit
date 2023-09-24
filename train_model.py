from ultralytics import YOLO
import torch
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

if __name__ == '__main__':
    model = YOLO('yolov8s.pt')
    model.to(device)
    results = model.train(data='data.yaml',
   imgsz=640,
   epochs=25,
   batch=8,
   name='yolov8s_custom_rzd_25_epoches_combined_datasets')