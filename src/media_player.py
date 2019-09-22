import cv2

test_file = "data/8cfdc752-dde5-4cc9-9a90-5c87ba658728/test.avi"

if __name__ == "__main__":
    video_file = cv2.VideoCapture(test_file)
    print("AffMEM Media Player player")

    fps = video_file.get(cv2.CAP_PROP_FPS)
    video_file.set(cv2.CAP_PROP_FPS, fps)
    while video_file.isOpened():
        _, img = video_file.read() 
    
        cv2.imshow("Out", img)
        key = cv2.waitKey(1) & 0xff

    video_file.release()
