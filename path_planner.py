# path_planner.py
def get_next_step(current, target, obstacles):
    """
    根據當前位置(current) 和 目標(target) 回傳下一步座標。
    若前方有障礙，就換方向。
    """
    x, y = current
    tx, ty = target

    # 嘗試往目標方向移動
    if x < tx and (x + 1, y) not in obstacles:
        return (x + 1, y)
    elif x > tx and (x - 1, y) not in obstacles:
        return (x - 1, y)
    elif y < ty and (x, y + 1) not in obstacles:
        return (x, y + 1)
    elif y > ty and (x, y - 1) not in obstacles:
        return (x, y - 1)
    else:
        # 若四面都被擋住，原地不動
        return (x, y)
