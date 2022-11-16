import pupilcore as pupil

postprocessing = pupil.pupil_postprocessing(
    path                ='/home/antonio/WORKSPACE/test_data/ant_001_2022-11-11_17h36.59.762/000',
    start_time          =24,   #time to exclude before experiment begins
    ang                 = 1.5, #allowed eye-jitter in dva
    screen_width        = 38,
    viewing_distance    = 57,
    resolution          = [1024,768]
    )

# check that the files where exported with pupil-player
postprocessing.print_file_struc()

# get gaze data
gaze_data = postprocessing.get_gaze_pos()

# remove low confidence samples < 0.95
new_data = postprocessing.remove_low_conf(gaze_data)

# plot data again
postprocessing.plt_gaze_pos(new_data)
postprocessing.plt_gaze_scatter(new_data)