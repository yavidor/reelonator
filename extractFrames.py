from sys import argv
import cv2
vidcap = cv2.VideoCapture(argv[1])
output_dir = argv[2]
print(output_dir)
success, image = vidcap.read()
count = 1
success = True
while success:
    cv2.imwrite(f"{output_dir}/frames/{count:06d}.jpg",
                image)     # save frame as JPEG file
    success, image = vidcap.read()
    if cv2.waitKey(10) == 27:                     # exit if Escape is hit
        break
    count += 1
