from ultralytics import YOLO

# Model seçimi: yolov8n.pt (önceden eğitilmiş model, transfer learning)
model = YOLO('yolov8n.pt')

# Eğitimi başlat
def main():
    model = YOLO('yolov8n.pt')  
    model.train(
    data='D:/Graduation_Project/dataset/data.yaml',
    epochs=15,
    imgsz=320,
    batch=2,           # bir seferde öğreneceği resim sayısı
    name='plaka_model',
    project='D:\Graduation_Project\YOLO_Results',
    device=0           # GPU cihazının id si
)

if __name__ == '__main__':
    from multiprocessing import freeze_support
    freeze_support()
    main()
