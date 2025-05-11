a, b, c = map(int, input().split())

base = (11 * 24 * 60) + (11 * 60) + 11
now = (a * 24 * 60) + (b * 60) + c

print(now - base if now >= base else -1)