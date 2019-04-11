import sensor, image, time, pyb

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

led_indicator = pyb.LED(1)          # Create a LED object which will indicate when camera on/off
                                    # LED(1) turns on red
led_indicator.off()                 # Set initial state to off

# Load Haar Cascade
# By default this will use all stages, lower satges is faster but less accurate.
face_cascade = image.HaarCascade("frontalface", stages=25)
print(face_cascade)

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

    # Draw objects
    for r in objects:
        img.draw_rectangle(r)

    # Print FPS.
    # Note: Actual FPS is higher, streaming the FB makes it slower.
    print(clock.fps())
