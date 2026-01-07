import sys
import time

# Check dependencies first
try:
    import cv2
    import requests
except ImportError as e:
    print("=" * 60)
    print("ERROR: Missing required package!")
    print("=" * 60)
    print(f"Details: {e}")
    print("\nPlease install the missing packages:")
    print("  pip install opencv-python requests")
    print("=" * 60)
    input("Press Enter to exit...")
    sys.exit(1)

# Flask API endpoint
API_URL = "http://localhost:5000/api/attendance/scan"
# Scanner secret must match SCANNER_SECRET in server (default 'dev-scanner')
SCANNER_SECRET = "dev-scanner"

def scan_qr_webcam(camera_index=0):
    try:
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            print("ERROR: Could not open camera!")
            print("Please check:")
            print("1. Camera is connected")
            print("2. Camera permissions are granted")
            print("3. No other application is using the camera")
            input("Press Enter to exit...")
            return
        
        detector = cv2.QRCodeDetector()

        # Get resolution
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        print("=" * 60)
        print("QR SCANNER STARTED")
        print("=" * 60)
        print("Press 'Q' key to quit")
        print("Scanning QR codes to update attendance...")
        print("Make sure Flask server is running on http://localhost:5000")
        print("=" * 60)
        
        prev_time = time.time()
        last_scanned_qr = None
        last_scan_time = 0
        scan_cooldown = 3  # seconds between scans of the same QR

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to read frame from camera.")
                break

            # Detect and decode QR code
            data, points, _ = detector.detectAndDecode(frame)

            if points is not None:
                pts = points[0].astype(int)
                for i in range(len(pts)):
                    cv2.line(frame, tuple(pts[i]), tuple(pts[(i+1) % len(pts)]), (0, 255, 0), 2)

            # Process QR code if detected
            if data:
                current_time = time.time()
                # Prevent duplicate scans
                if data != last_scanned_qr or (current_time - last_scan_time) > scan_cooldown:
                    last_scanned_qr = data
                    last_scan_time = current_time
                    
                    # Send to database
                    try:
                        response = requests.post(
                            API_URL,
                            json={'qr_data': data},
                            headers={
                                'Content-Type': 'application/json',
                                'X-Scanner-Secret': SCANNER_SECRET
                            },
                            timeout=5
                        )
                        result = response.json()
                        
                        if result.get('success'):
                            print(f"✓ {result.get('message')}")
                            cv2.putText(frame, "SUCCESS: " + result.get('message', ''), (10, 60),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        else:
                            print(f"✗ Error: {result.get('error')}")
                            cv2.putText(frame, "ERROR: " + result.get('error', ''), (10, 60),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    except requests.exceptions.ConnectionError:
                        print("✗ Connection error: Cannot connect to Flask server")
                        print("   Make sure the server is running on http://localhost:5000")
                        cv2.putText(frame, "Connection Error - Check Server", (10, 60),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    except requests.exceptions.Timeout:
                        print("✗ Request timeout")
                        cv2.putText(frame, "Request Timeout", (10, 60),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    except Exception as e:
                        print(f"✗ Error: {e}")
                
                cv2.putText(frame, f"QR: {data}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 0, 0), 2)

            # Calculate FPS
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time)
            prev_time = curr_time

            # Overlay resolution and FPS
            cv2.putText(frame, f"Resolution: {width}x{height}", (10, height - 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(frame, f"FPS: {int(fps)}", (10, height - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            cv2.imshow("QR Scanner - Press Q to Stop", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("=" * 60)
                print("Scanner stopped by user")
                print("=" * 60)
                break

        cap.release()
        cv2.destroyAllWindows()
        
    except Exception as e:
        print("=" * 60)
        print(f"FATAL ERROR: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        scan_qr_webcam()
    except KeyboardInterrupt:
        print("\nScanner interrupted by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")