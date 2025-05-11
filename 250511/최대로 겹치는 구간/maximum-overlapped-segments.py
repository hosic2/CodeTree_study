n = int(input())
segments = [tuple(map(int, input().split())) for _ in range(n)]

max_overlap = 0

# 모든 선분쌍을 기준으로 겹치는 지점 탐색
for i in range(n):
    for j in range(i + 1, n):
        # 두 선분의 교차 구간이 존재할 때 중간 지점을 계산
        l = max(segments[i][0], segments[j][0])
        r = min(segments[i][1], segments[j][1])

        if l < r:
            # 중간에 실수 지점을 선택 (정수는 제외)
            mid = (l + r) / 2

            count = 0
            for x1, x2 in segments:
                if x1 < mid < x2:  # 끝점 제외
                    count += 1

            max_overlap = max(max_overlap, count)

print(max_overlap)
