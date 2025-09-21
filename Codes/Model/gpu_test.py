import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Kullanılan Cihaz: {device}")

devNumber= torch.cuda.current_device()
print(f"Kullanılan cihazın numarası: {devNumber}")

devName = torch.cuda.get_device_name(devNumber)
print(f"GPU İsmi : {devName}")

#CPU da üretilen değeri GPU ile okumak için bir dizi testi
T1=torch.randn(4,4)
print("CPU :")
print(T1)


T2=T1.to(device)
print("GPU :")
print(T2)