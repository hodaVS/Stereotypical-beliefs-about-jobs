#!/usr/bin/python
# -*- coding: utf-8 -*-
from psychopy import visual, core, event, gui, sound, monitors
import pandas as pd
import numpy as np
import random
from Params import *
from datetime import datetime
from pathlib import Path


    
def Run_Task():
    Trial_csv = []
    userAns_csv = []
    RTime_csv = []
    RJob_csv = []
    block_type_csv = []

    user_info = UserInfo()
    (win, square) = set_window(screen_size=[widthPix, heightPix],
                               color='white')
    mouse = event.Mouse(visible=True, win=win)
            
    Type_block = ['Training','Main']
    for blockT in Type_block:
        r_jobs = get_random_jobs(blockT)
        if blockT == 'Training':
            trial_c = len(r_jobs)
            path = '../Asset/Jobs/Training/'
        else:
            trial_c = len(r_jobs[:number_of_jobs])
            path = '../Asset/Jobs/'
        for i in range(0, trial_c):
            block_type_csv.append(blockT)
            Trial_csv.append(i)
            if r_jobs[i]['Color'] == 'b':
                Jcolor = 'Blue'
            elif r_jobs[i]['Color'] == 'g':
                Jcolor = 'Green'
            else:
                Jcolor = 'Pink'
                
            
            
            
            img_name = r_jobs[i]['Name'] + '_ ' + r_jobs[i]['Color']
            Arc = visual.ImageStim(win=win, image='../Asset/' + 'Arc'
                                   + '.PNG', pos=(0, 100))
            Click_img = visual.ImageStim(win=win, image='../Asset/'
                    + 'click' + '.PNG', pos=(0, 0))
            Job_img = visual.ImageStim(win=win, image= path
                                       + img_name + '.PNG', pos=(0, 55),size=(500,300))
            Slow_mov = visual.ImageStim(win=win, image='../Asset/'
                                        + 'Slow_move' + '.PNG')

            square.draw()
            Arc.draw()
            Click_img.autoDraw = True
            win.flip()

            check_in = True
            timer = core.Clock()
            timer_2 = core.Clock()
            timer_3 = core.Clock()

            while check_in:

                if mouse.isPressedIn(square, buttons=[0]):
                    Click_img.autoDraw = False
                    core.wait(display_jobox)
                    Job_img.autoDraw = True
                    s_2 = timer_2.getTime()
                    check_in = False
                else:
                    check_in = True

            event.clearEvents()
            mouse.setPos = mouse_pos

            isin = True

            while isin:
                (x, y) = mouse.getPos()
                if x > -25. and x < 25. and y < -126 and y > -176:
                    e_2 = timer_2.getTime()
                    if e_2 - s_2 > hurry:
                        Job_img.autoDraw = False
                        displayImg(
                            win,
                            'Hurry',
                            feedback_delay,
                            False,
                            None,
                            None,
                            )
                        Job_img.autoDraw = True
                        timer_2.reset()
                    timer.reset()
                    isin = True
                else:
                    s_3 = timer_3.getTime()
                    Job_img.autoDraw = False
                    isin = False

                square.draw()
                Arc.draw()
                win.flip()

            start = timer.getTime()
            is_pressed = False
            while not is_pressed:
                if mouse.getPressed() == [1, 0, 0]:
                    (pressed_posX, pressed_posY) = mouse.getPos()
                    is_pressed = True
                else:
                    e_3 = timer_3.getTime()
                    if e_3 - s_3 > slow_move:
                        square.draw()
                        Arc.draw()
                        Slow_mov.autoDraw = True
                        win.flip()
                        core.wait(feedback_delay)
                        square.draw()
                        Arc.draw()
                        Slow_mov.autoDraw = False
                        win.flip()
                        timer_3.reset()

                    is_pressed = False

            RT = timer.getTime() - start
            if RT <= Too_fast:
                displayImg(
                    win,
                    'Too_fast',
                    feedback_delay,
                    False,
                    None,
                    None,
                    )
            if RT >= Too_slow:
                displayImg(
                    win,
                    'Too_slow',
                    feedback_delay,
                    False,
                    None,
                    None,
                    )
            RJob_csv.append(r_jobs[i]['Name'] + '_ ' + Jcolor)
            RTime_csv.append(RT)
            userAns_csv.append(angle_between((pressed_posX, pressed_posY
                               + 72), (420, 0)))

    win.close()
    DialogGui = gui.Dlg(title='color prefer')
    DialogGui.addField(' What color do you prefer?  ', choices=['Gray',
                       'Blue', 'Pink'])  # 0
    DialogGui.show()
    SaveDate(
        user_info,
        Trial_csv,
        userAns_csv,
        RTime_csv,
        DialogGui.data[0],
        RJob_csv,
        block_type_csv
        )


def get_random_jobs(Type):
    Jobs = []
    color = []
    Job_list = []
    Job_dic = {}
    
    if Type == "Training":
        path = '../Asset/Jobs/Training'
        r = random.sample(range(0, 15), 15)
    elif Type == "Main":
        path = '../Asset/Jobs'
        r = random.sample(range(0, 600), 600)
    filenames = sorted(Path(path).glob('*.png'))
    for job in filenames:
        Jobs.append(job.name)
    Jobs = np.asarray(Jobs)
    for item in Jobs:
        Job_dic['Name'] = item.split('_')[0]
        Job_dic['Color'] = item[-5:][0]
        Job_list.append(Job_dic.copy())
    
    Jobs_list = np.asarray(Job_list)
    return Jobs_list[r]


def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi)) * (5 / 9)  # scale from 0-180 -> 0-100


def set_window(screen_size, color):

    if color == 'black' or color == 'Black':
        Cwin = [-1, -1, -1]
    elif color == 'white' or color == 'White':
        Cwin = [1, 1, 1]
    elif color == 'grey' or color == 'Grey':
        Cwin = [0, 0, 0]

    win = visual.Window(monitor=mon, size=screen_size, fullscr=True,
                        units='pix', color=Cwin)

    square = visual.Rect(
        win=win,
        units='pix',
        width=50,
        height=50,
        pos=mouse_pos,
        fillColor=[-1, -1, -1],
        lineColor=[-1, -1, -1],
        )

    return (win, square)


def print_mouse_pos(windows, img, square):
    mouse = event.Mouse(visible=True, newPos=None, win=windows)
    while not mouse.getPressed() == [1, 0, 0]:
        textstimlike = visual.TextBox(
            window=windows,
            text=str(mouse.getPos()),
            font_size=18,
            font_color=[-1, -1, 1],
            color_space='rgb',
            size=(1.8, .1),
            pos=(-.1, .8),
            units='norm',
            )
        textstimlike.draw()
        img.draw()
        square.draw()
        windows.flip()


#    windows.flip()

def displayImg(
    win,
    imgName,
    duration,
    instr,
    size,
    pos,
    win_flip=True,
    ):

    if size == None and pos == None:
        img = visual.ImageStim(win=win, image='../Asset/' + imgName
                               + '.PNG')
    else:
        img = visual.ImageStim(win=win, image='../Asset/' + imgName
                               + '.PNG', pos=(pos[0], pos[1]))
    if instr:
        img.draw()
        win.flip()
    elif not win_flip:
        imgClk = core.Clock()
        while True:
            if imgClk.getTime() >= duration:
                img.draw()
                win.flip()
                break
    else:

        imgClk = core.Clock()
        while imgClk.getTime() < duration:
            img.draw()
            win.flip()

        win.flip()


def Index_check(arr, maxim):
    for i in range(maxim - len(arr)):
        arr.append(' ')


def SaveDate(
    UsrInfo,
    Trial_csv,
    userAns_csv,
    RTime_csv,
    color_preferance,
    trial_job,
    block_type
    ):
    Id = []
#    Name = []
#    LastName = []
    Gender = []
    Age = []
    Job = []
    Parrent_job = []
    Colorblind = []
    Color_choose = []

    (
        usrNum,
#        usrName,
#        usrLastName,
        usrAge,
        usrGender,
        usrJob,
        parrentJob,
        clorBlind,
        ) = UsrInfo
    maxim = max(len(Trial_csv), len(block_type),len(RTime_csv), len(userAns_csv),
                len(trial_job))
    for i in range(maxim):
        Id.append('-')
#        Name.append('-')
#        LastName.append('-')
        Age.append('-')
        Gender.append('-')
        Job.append('-')
        Parrent_job.append('-')
        Colorblind.append('-')
        Color_choose.append('-')

    Id[0] = usrNum
#    Name[0] = usrName
#    LastName[0] = usrLastName
    Age[0] = usrAge
    Gender[0] = usrGender
    Job[0] = usrJob
    Parrent_job[0] = parrentJob
    Colorblind[0] = clorBlind
    Color_choose[0] = color_preferance
    if (len(Trial_csv), len(userAns_csv), len(RTime_csv),
        len(trial_job) , len(block_type) / 5) != maxim:
        l = [Trial_csv, userAns_csv, RTime_csv, trial_job , block_type]
        for ind_l in l:
            Index_check(ind_l, maxim)
    data_dict = {
        'Subject.num': Id,
#        'Subject.name': Name,
#        'Subject.surName': LastName,
        'Age': Age,
        'Gender': Gender,
        'user Job': Job,
        'Parrent_job': Parrent_job,
        'Colorblind': Colorblind,
        'Color Chosen': Color_choose,
        'Correct.answer': userAns_csv,
        'Random_Job': trial_job,
        'R_time': RTime_csv,
        'Trial': Trial_csv,
        'Block Type' : block_type,
        }

    UserInfoDF = pd.DataFrame(data_dict, columns=[
        'Subject.num',
#        'Subject.name',
#        'Subject.surName',
        'Age',
        'Gender',
        'user Job',
        'Parrent_job',
        'Colorblind',
        'Block Type',
        'Trial',
        'Random_Job',
        'Correct.answer',
        'R_time',
        'Color Chosen',
        ])
    dir_csv = '../Output_File/'
    UserInfoDF.to_csv(dir_csv
                      + str(datetime.now().strftime('%d_%m_%Y_%H_%M_%S'
                      )) + '__' + str(usrNum) 
                      + '.csv', index=False, header=True,
                      line_terminator='\r\n')


def getUserInfo():
    again = False
    DialogGui = gui.Dlg(title='User information')
#    DialogGui.addField(' Subject Name: ')  # 0
#    DialogGui.addField(' Subject Surname: ')  # 1
    DialogGui.addField(' Subject Id: ')  # 2 0
    DialogGui.addField(' Age: ')  # 3 1
    DialogGui.addField('Gender', choices=['Male', 'Female'])  # 4 2
    DialogGui.addField('Job ')  # 5 3
    DialogGui.addField('Parent Job ')  # 6 4
    DialogGui.addField('Color Blind :', choices=['Yes', 'No'])  # 7 5
    DialogGui.show()

    if not DialogGui.data[0].isdigit() \
        or not DialogGui.data[1].isdigit():
        again = True
        (DialogGui.data[0], DialogGui.data[1]) = (99999999, 99999999)

#    if DialogGui.data[0].isdigit() or DialogGui.data[1].isdigit():
#        again = True

    if not DialogGui.OK:
        core.quit()
    listInfo = [
        int(DialogGui.data[0]),
#        DialogGui.data[0],
#        DialogGui.data[1],
        int(DialogGui.data[1]),
        DialogGui.data[2],
        DialogGui.data[3],
        DialogGui.data[4],
        DialogGui.data[5],
        ]
    if '' or 99999999 in listInfo:
        again = True
    else:
        again = False

    return [listInfo, again]


def UserInfo():
    (usrInfo, again) = getUserInfo()
    while again:
        (usrInfo, again) = getUserInfo()
    return usrInfo
