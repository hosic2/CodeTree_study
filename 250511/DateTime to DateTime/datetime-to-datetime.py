a, b, c = map(int, input().split())

# Please write your code here.
print((a * 60 * 24 + b * 60 + c) - (11 * 60 * 25 + 11) if a > 11 and b > 11 and c > 11 else -1) 