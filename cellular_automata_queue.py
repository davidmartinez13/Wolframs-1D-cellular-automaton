import numpy as np
import sys
import time
import cv2
import matplotlib as mpl
np.set_printoptions(threshold=sys.maxsize)
def circular(lst):
    while True:
        for element in lst:
            yield element
            
def compute_next_line(prev_line,ruleset):
    new_line = np.ones(prev_line.shape[0])

    line = prev_line.tolist()
    first = line[0]
    last = line[-1]
    line.append(first)
    line.insert(0, last)
    
    segment = np.zeros(3).tolist()
    
    for j in range(prev_line.shape[0]):
        segment = line[j:j+3]
        if segment == [1,1,1]:
            new_line[j] = ruleset[0]
        if segment == [1,1,0]:
            new_line[j] = ruleset[1]
        if segment == [1,0,1]:
            new_line[j] = ruleset[2]
        if segment == [1,0,0]:
            new_line[j] = ruleset[3]
        if segment == [0,1,1]:
            new_line[j] = ruleset[4]
        if segment == [0,1,0]:
            new_line[j] = ruleset[5]
        if segment == [0,0,1]:
            new_line[j] = ruleset[6]
        if segment == [0,0,0]:
            new_line[j] = ruleset[7]
    return new_line
def compute_next_line_np(prev_line,ruleset):
    row_size = prev_line.shape[0]
    new_line = np.ones(row_size)
    
    line = prev_line.tolist()

    first = line[0]
    last = line[-1]
    line.append(first)
    line.insert(0, last)
    line = np.array(line)

    left = line[:row_size]*2
    me = line[1:row_size+1] *4
    right = line[2:]*8
    
    l_m_r_sum = left + me + right
    new_line = np.zeros((8,row_size))

    new_line[0,:] = np.where(l_m_r_sum == 14,ruleset[0] ,0)
    new_line[1,:] = np.where(l_m_r_sum == 6, ruleset[1] ,0)    
    new_line[2,:] = np.where(l_m_r_sum == 10,ruleset[2] ,0)    
    new_line[3,:] = np.where(l_m_r_sum == 2, ruleset[3] ,0)
    new_line[4,:] = np.where(l_m_r_sum == 12,ruleset[4] ,0)
    new_line[5,:] = np.where(l_m_r_sum == 4, ruleset[5] ,0)    
    new_line[6,:] = np.where(l_m_r_sum == 8, ruleset[6] ,0)
    new_line[7,:] = np.where(l_m_r_sum == 0, ruleset[7] ,0)
    return new_line.sum(axis=0)
    


height = 90
width = 90

main_grid = np.ones((height,width)).tolist()
prev_line = np.ones(width)
prev_line[int(width/2)] = 0
#choose different rulesets

rulesets ={'a':[0,1,0,1,1,0,1,0],'b':[1,0,0,0,0,1,1,1],'c':[1,0,0,0,1,0,0,1],'d':[0,1,1,1,0,1,1,0],'e':[1,0,0,0,1,0,0,1]}
ruleset = rulesets['b']


while True:
    start = time.time()

    main_grid.append(prev_line )
    main_grid.pop(0)
    next_line = compute_next_line_np(prev_line, ruleset)
    prev_line = next_line
    char_grid = np.array(next_line)
    #printing with different squares on terminal

    bw_squares = {'big':["⬜","⬛"],'medium':["⬚","◼"],'small':["□","■"]}

    show = np.where(char_grid ==1,bw_squares['medium'][0],bw_squares['medium'][1])

    st = ""
    print(st.join(show.tolist()))
    _main_grid = np.repeat(np.array(main_grid),10, axis=0)
    _main_grid = np.repeat(_main_grid,10, axis=1)
    cv2.imshow('grid', cv2.resize(np.array(_main_grid.copy()), (600,600)))
    
    end = time.time()
    # print(end - start)

    time.sleep(0.05)
    k = cv2.waitKey(1)

    if k == 27:
        cv2.destroyAllWindows()
        break
