
import cv2
import numpy as np

def read_barcode_qrcode(image):
    detector = cv2.QRCodeDetector()
    value, pts, _ = detector.detectAndDecode(image)
    
    if value:
        print(f"Detected Barcode/QR code: {value}")
        
        if pts is not None:
            pts = pts[0]
            if len(pts) == 4:
                pts = np.int32(pts)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(image, [pts], True, (0, 255, 0), 3)
            else:
                rect = cv2.boundingRect(np.array(pts))
                cv2.rectangle(image, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3)
        
        cv2.putText(image, value, (pts[0][0][0], pts[0][0][1] - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    return image

def process_image(image_path):
    image = cv2.imread(r'C:\Users\ADITYA MARATHI\Desktop\adi\barcodeImage.png')
    
    if image is None:
        print("Error: Could not open or find the image. Please check the image path.")
        return
    
    image = read_barcode_qrcode(image)
    cv2.imshow("Barcode/QR Code Reader (Image)", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def process_webcam():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not access the webcam.")
        return
    
    print("Starting webcam scan... Press 'q' to exit.")
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Could not read frame.")
            break
        
        frame = read_barcode_qrcode(frame)
        cv2.imshow("Live Barcode/QR Code Scanner", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def main():
    choice = input("Choose mode:\n1. Scan from image file\n2. Scan using webcam\nEnter choice (1 or 2): ")
    
    if choice == '1':
        image_path = input("Enter the path to the image file: ")
        process_image(image_path)
    elif choice == '2':
        process_webcam()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()