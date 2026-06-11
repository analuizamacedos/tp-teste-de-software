# Streak flexível (Opção B): se a conclusão mais recente foi ontem,
# o streak ainda conta — hoje ainda pode ser completado.
# O streak zera apenas se a data mais recente for anterior a ontem.

from datetime import date, timedelta


def calculate_current_streak(logs: list[date]) -> int:
    if not logs:
        return 0
    sorted_logs = sorted(set(logs), reverse=True)
    today = date.today()
    yesterday = today - timedelta(days=1)
    if sorted_logs[0] == today:
        expected = today
    elif sorted_logs[0] == yesterday:
        expected = yesterday
    else:
        return 0
    count = 0
    for d in sorted_logs:
        if d == expected:
            count += 1
            expected -= timedelta(days=1)
        elif d < expected:
            break
    return count


def calculate_max_streak(logs: list[date]) -> int:
    if not logs:
        return 0
    sorted_logs = sorted(set(logs))
    max_seen = 1
    current = 1
    for i in range(1, len(sorted_logs)):
        if sorted_logs[i] == sorted_logs[i - 1] + timedelta(days=1):
            current += 1
            max_seen = max(max_seen, current)
        else:
            current = 1
    return max_seen
