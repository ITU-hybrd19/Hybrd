import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
cv2.namedWindow("Tracking green")
cv2.namedWindow("Tracking red")

cv2.createTrackbar("GLH", "Tracking green", 0, 255, nothing)
cv2.createTrackbar("GLS", "Tracking green", 0, 255, nothing)
cv2.createTrackbar("GLV", "Tracking green", 0, 255, nothing)
cv2.createTrackbar("GUH", "Tracking green", 255, 255, nothing)
cv2.createTrackbar("GUS", "Tracking green", 255, 255, nothing)
cv2.createTrackbar("GUV", "Tracking green", 255, 255, nothing)

cv2.createTrackbar("RLH", "Tracking red", 0, 255, nothing)
cv2.createTrackbar("RLS", "Tracking red", 0, 255, nothing)
cv2.createTrackbar("RLV", "Tracking red", 0, 255, nothing)
cv2.createTrackbar("RUH", "Tracking red", 255, 255, nothing)
cv2.createTrackbar("RUS", "Tracking red", 255, 255, nothing)
cv2.createTrackbar("RUV", "Tracking red", 255, 255, nothing)

while (1):
    _, img = cap.read()

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    g_l_h = cv2.getTrackbarPos("GLH", "Tracking green")
    g_l_s = cv2.getTrackbarPos("GLS", "Tracking green")
    g_l_v = cv2.getTrackbarPos("GLV", "Tracking green")
    g_u_h = cv2.getTrackbarPos("GUH", "Tracking green")
    g_u_s = cv2.getTrackbarPos("GUS", "Tracking green")
    g_u_v = cv2.getTrackbarPos("GUV", "Tracking green")

    r_l_h = cv2.getTrackbarPos("RLH", "Tracking red")
    r_l_s = cv2.getTrackbarPos("RLS", "Tracking red")
    r_l_v = cv2.getTrackbarPos("RLV", "Tracking red")
    r_u_h = cv2.getTrackbarPos("RUH", "Tracking red")
    r_u_s = cv2.getTrackbarPos("RUS", "Tracking red")
    r_u_v = cv2.getTrackbarPos("RUV", "Tracking red")



    # defining the range of green color
    green_lower = np.array([g_l_h , g_l_s, g_l_v], np.uint8)
    green_upper = np.array([g_u_h , g_u_s, g_u_v], np.uint8)
    # defining the range of red color
    red_lower = np.array([r_l_h, r_l_s, r_l_v])
    red_upper = np.array([r_u_h, r_u_s, r_u_v])

    # finding the range green and red colour in the image
    green = cv2.inRange(hsv, green_lower, green_upper)
    red = cv2.inRange(hsv, red_lower, red_upper)
    # Morphological transformation, Dilation
    kernal = np.ones((5, 5), "uint8")

    mask_green = cv2.dilate(green, kernal, iterations=3)
    mask_green = cv2.erode(mask_green, None, iterations=2)
    mask_green = cv2.GaussianBlur(mask_green, (5, 5), 0)
    mask_green = cv2.Canny(mask_green, 30, 200)

    mask_red = cv2.dilate(red, kernal, iterations=3)
    mask_red = cv2.erode(mask_red, None, iterations=2)
    mask_red = cv2.GaussianBlur(mask_red, (5, 5), 0)
    mask_red = cv2.Canny(mask_red, 30, 200)

    res_green = cv2.bitwise_and(img, img, mask=mask_green)
    res_red = cv2.bitwise_and(img, img, mask=mask_red)

    # Tracking Colour (green)
    ( contours_green, hierarchy) = cv2.findContours(mask_green.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ( contours_red, hierarchy) = cv2.findContours(mask_red.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour_green in enumerate(contours_green):
        area = cv2.contourArea(contour_green)
        if (area > 300):
            x, y, w, h = cv2.boundingRect(contour_green)
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(img, "green", (x, y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, 100)

    for pic, contour_red in enumerate(contours_red):
        area = cv2.contourArea(contour_red)
        if (area > 300):
            x, y, w, h = cv2.boundingRect(contour_red)
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)
            cv2.putText(img, "red", (x, y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, 100)

    cv2.imshow("Color Tracking", img)
    img = cv2.flip(img, 1)
    cv2.imshow("green", res_green)
    cv2.imshow("red", res_red)

    if cv2.waitKey(10) & 0xFF == 27:
        cap.release()
        cv2.destroyAllWindows()
        break