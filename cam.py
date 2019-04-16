import sensor, image, time, pyb

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

led_indicator = pyb.LED(1)          # Create a LED object which will indicate when camera on/off
                                    # LED(1) turns on red
led_indicator.off()                 # Set initial state to off

s_pan = pyb.Servo(1)                #Pan Servo connected to Pin P7
s_pan.angle(0)                     #Set initial position to 0 degrees

s_tilt = pyb.Servo(2)               #Tilt Servo connected to Pin P8
s_tilt.angle(0)                    #Set intitial position to 0 degrees

pan_angle = 0
tilt_angle = 0

# Load Haar Cascade
# By default this will use all stages, lower satges is faster but less accurate.
face_cascade = image.HaarCascade("frontalface", stages=25)
print(face_cascade)

#calculating bounds for movement
bound = 0.3
leftBound = (int)(320 * bound)
rightBound = (int)(320 * (1 - bound))
upperBound = (int)(240 * bound)
lowerBound = (int)(240 * (1 - bound))
boundWidth = rightBound - leftBound
boundHeight = lowerBound - upperBound

# FPS clock
clock = time.clock()

while (True):
    clock.tick()

    # Capture snapshot
    img = sensor.snapshot()

    # Find objects.
    # Note: Lower scale factor scales-down the image more and detects smaller objects.
    # Higher threshold results in a higher detection rate, with more false positives.
    objects = img.find_features(face_cascade, threshold=0.75, scale_factor=1.25)
    img.draw_rectangle((leftBound, upperBound, boundWidth, boundHeight))
    # Draw objects
    if(objects):
        r = objects[0]
        img.draw_rectangle(r)
        print(r)
        centerX = r[0] + (r[2] * 0.5)
        centerY = r[1] + (r[3] * 0.5)
        if (centerX < leftBound):
            print("left")
            print(pan_angle)
            if(pan_angle < 85):
                pan_angle = pan_angle + 5
                s_pan.angle(pan_angle)
                #print(pan_angle)
        elif (centerX > rightBound):
            print("right")
            print(pan_angle)
            if(pan_angle > -85):
                pan_angle = pan_angle - 5
                s_pan.angle(pan_angle)
                #print(pan_angle)
        if (centerY < upperBound):
            print("up")
            print(tilt_angle)
            if(tilt_angle < 85):
                tilt_angle = tilt_angle + 5
                s_tilt.angle(tilt_angle)
                #print(tilt_angle)
        elif (centerY > lowerBound):
            print("down")
            print(tilt_angle)
            if(tilt_angle > -85):
                tilt_angle = tilt_angle - 5
                s_tilt.angle(tilt_angle)
                #print(tilt_angle)

    # Print FPS.
    # Note: Actual FPS is higher, streaming the FB makes it slower.
    #print(clock.fps())
