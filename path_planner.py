# path_planner.py
import heapq

def heuristic(a, b):
    """啟發函數：使用曼哈頓距離"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal, obstacles, grid_size=20):
    """
    A* 路徑搜尋
    :param start: (x, y) 起點
    :param goal: (x, y) 終點
    :param obstacles: [(x,y), ...] 障礙物清單
    :param grid_size: 地圖邊界大小
    :return: 路徑 list[(x,y)] 或 None
    """
    def in_bounds(x, y):
        return 0 <= x < grid_size and 0 <= y < grid_size

    obstacle_set = set(obstacles)
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        x, y = current
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            neighbor = (x+dx, y+dy)
            if not in_bounds(neighbor[0], neighbor[1]):
                continue
            if neighbor in obstacle_set:
                continue

            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))

    return None

def predict_neighbor_positions(obstacles):
    """
    預測其他車輛下一步可能位置（四方向 + 原地）。
    用來避免互相卡住或對撞。
    """
    predicted = set()
    for ox, oy in obstacles:
        for dx, dy in [(0,0),(1,0),(-1,0),(0,1),(0,-1)]:
            predicted.add((ox+dx, oy+dy))
    return predicted

def get_next_step(current, target, obstacles):
    """
    使用 A*，同時考慮其他車輛未來位置。
    若所有路徑都被擋，原地不動。
    """
    if current == target:
        return current

    # 預測其他車的下一步
    future_obstacles = predict_neighbor_positions(obstacles)
    all_blocked = set(obstacles) | future_obstacles

    # 嘗試找到避開所有預測障礙的最短路徑
    path = a_star(current, target, all_blocked)

    if path and len(path) > 0:
        next_pos = path[0]
        # 確保下一格不被任何車佔用
        if next_pos not in all_blocked:
            return next_pos
    return current

# ✅ 測試範例
if __name__ == "__main__":
    # 模擬多車避讓情境
    start = (0, 0)
    goal = (5, 5)
    other_vehicles = [(1,0), (2,1)]  # 其他車輛座標
    print("🚗 自車從", start, "到", goal, "避開：", other_vehicles)
    step = get_next_step(start, goal, other_vehicles)
    print("➡️ 下一步:", step)
