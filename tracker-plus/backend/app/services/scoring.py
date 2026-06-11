def calculate_points(streak: int, base_points: int = 10) -> int:
    points = base_points
    if streak >= 7:
        points += 50
    if streak >= 30:
        points += 100
    return points
