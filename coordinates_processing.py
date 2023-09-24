def buf_rect (buf_box_xy):
    point1_x = buf_box_xy[0]
    point2_x = buf_box_xy[2]
    track_width_cm = 152
    bufzone_width_cm = 100
    track_width_pix = abs(point1_x - point2_x)
    bufzone_width_pix = bufzone_width_cm / track_width_cm * track_width_pix
    #if point1_x < point2_x:
    point1_x -= bufzone_width_pix
    point2_x += bufzone_width_pix
    #else:
    #    point1_x += bufzone_width_pix
    #   point2_x -= bufzone_width_pix
    return [point1_x, buf_box_xy[1], point2_x, buf_box_xy[3]]

def warning (person_box_xy,buf_box_xy):
    person_xy1 = person_box_xy[:2]
    person_xy2 = person_box_xy[2:4]
    buf_box_xy1 = buf_box_xy[:2]
    buf_box_xy2 = buf_box_xy[2:4]
    s_target = 0.2
    s_person = (person_xy2[0]-person_xy1[0])*(person_xy2[1]-person_xy1[1])
    if (buf_box_xy1[0] < person_xy1[0] < buf_box_xy2[0]) or (buf_box_xy1[0] < person_xy2[0] < buf_box_xy2[0]):

        x_left = max(person_xy1[0], buf_box_xy1[0])
        y_left = min(person_xy1[1], buf_box_xy1[1])
        x_right = min(person_xy2[0], buf_box_xy2[0])
        y_right = max(person_xy2[1], buf_box_xy2[1])

        width = x_right - x_left
        height = y_right - y_left

        if (width < 0) or (height < 0): return False
        elif (width*height/s_person < s_target): return False
        else:
            return True



