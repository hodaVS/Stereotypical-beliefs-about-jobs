from psychopy import visual , core , event , gui , sound , monitors

number_of_jobs = 5

#delays
display_jobox = 0.25
Too_fast = 0.15
hurry = 2.5
Too_slow = 4
slow_move = 1
feedback_delay = 0.5


# Display parameters
widthPix = 1600 # screen width in px
heightPix = 900 # screen height in px
monitorwidth = 40 # monitor width in cm
viewdist = 60. # viewing distance in cm
monitorname = 'SonyG500'
scrn = 0 # 0 to use main screen, 1 to use external screen
mon = monitors.Monitor(monitorname, width=monitorwidth, distance=viewdist)
mon.setSizePix((widthPix, heightPix))
mon.saveMon()

mouse_pos = (0,-150)
focal_point = (0,-30)