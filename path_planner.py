# path_planner.py
import heapq

def heuristic(a, b):
    """啟發函數：使用曼哈頓距離（Manhattan distance）"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal, obstacles, grid_size=20):
    """
    A* 路徑搜尋
    :param start: (x, y) 起點
    :param goal: (x, y) 終點
    :param obstacles: [(x,y), ...] 障礙物清單
    :param grid_size: 地圖邊界大小（可調）
    :return: 路徑 list[(x,y)] 或 None
    """
    # 用來避免路徑超出範圍
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
            # 回溯找路徑
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

    return None  # 找不到路徑

def get_next_step(current, target, obstacles):
    """
    使用 A* 算法取得下一步。
    若找不到路徑，則原地不動。
    """
    if current == target:
        return current

    path = a_star(current, target, obstacles)

    if path and len(path) > 0:
        # 回傳第一個步驟（下一格）
        return path[0]
    else:
        # 無法找到路徑就不動
        return current

# ✅ 測試範例
if __name__ == "__main__":
    start = (0, 0)
    goal = (5, 5)
    obstacles = [(1,0),(1,1),(1,2),(2,2),(3,2)]
    print("🚗 從", start, "到", goal)
    step = get_next_step(start, goal, obstacles)
    print("➡️ 下一步:", step)

