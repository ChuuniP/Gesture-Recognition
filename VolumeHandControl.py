import cv2
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap = cv2.VideoCapture(0)
w, h = 640, 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

hands, my_hands, my_drawing = htm.get_hands()

# Lấy loa mặc định
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Lấy range âm lượng
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

# Đặt âm lượng ban đầu (0 dB ~ max)
volume.SetMasterVolumeLevel(0, None)

while True:
    success, img = cap.read()
    if not success:
        print("Không mở được camera")
        break

    # Vẽ bàn tay
    img, all_hands = htm.draw_hands(img, hands, my_hands, my_drawing)

    # Lấy vị trí landmark
    positions = htm.get_hand_positions(img, hands)
    if positions:
        cx1, cy1 = positions[4]   # Ngón cái
        cx2, cy2 = positions[8]   # Ngón trỏ

        # Vẽ 2 điểm và đường nối
        cv2.circle(img, (cx1, cy1), 10, (0, 255, 255), -1)
        cv2.circle(img, (cx2, cy2), 10, (0, 255, 255), -1)
        cv2.line(img, (cx1, cy1), (cx2, cy2), (0, 200, 200), 3)

        # Tính khoảng cách
        distance = math.hypot(cx2 - cx1, cy2 - cy1)
        print("Khoảng cách giữa 2 điểm:", distance)

        # Map khoảng cách -> âm lượng
        vol = minVol + (distance / 200) * (maxVol - minVol)
        vol = max(minVol, min(vol, maxVol))
        volume.SetMasterVolumeLevel(vol, None)

    cv2.imshow("Img", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
