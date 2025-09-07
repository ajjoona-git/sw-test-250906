# 커피점과 제과점

### 유사문제
[boj 13911](https://www.acmicpc.net/problem/13911)

## 제한사항

파이썬 6초

## 문제 설명

N개의 건물 (ID: 0~N-1) (N≤10000)

M개의 커피점

P개의 제과점

나머지는 주택

K개의 양방향 도로 (K≤30000)

거리 정보가 주어진다. (1 ≤ dist ≤ 1000)

거리 제한 R (50 ≤ R ≤ 25000)

커피점과의 거리가 R이하이면서 제과점과의 거리가 R 이하인 주택 중 최소 거리 합을 출력해라. 조건을 만족하는 주택이 없다면 -1을 출력해라. 

## 함수

`def init(N, K, sBuilding[], eBuilding[], distance[])`

`def add(sBuilding, eBuilding, distance)`

`def calculate(M, mCoffee, P, mBakery, R)`

---

## 결과

테스트케이스 23/25 (시간 초과)

---

## 코드 분석 및 시간 초과 해결 방안

제출하신 코드의 로직은 거의 정확하지만, 다익스트라 알고리즘 구현 방식에 치명적인 비효율이 있어 시간 초과가 발생합니다. 핵심 원인과 해결 방안을 자세히 설명해 드리겠습니다.

### 시간 초과 핵심 원인: 잘못된 다익스트라 구현

가장 큰 문제는 dijkstra 함수 내의 반복문 구조입니다.

### 문제의 코드:

```python
def dijkstra(mShop, mSkip, R):
  # ...
  q = []
  for shop_id in mShop: # ① 외부 루프
    dist[shop_id] = 0
    heapq.heappush(q, (0, shop_id))
    while q: # ② 내부 루프
      # ... 다익스트라 로직 ...
```

현재 코드는 mShop에 포함된 모든 시작점(shop_id)에 대해 while q: 루프를 중첩해서 실행하고 있습니다. 이는 다음과 같은 문제를 일으킵니다.

- 반복 실행: mShop에 가게가 M개 있다면, 다익스트라 알고리즘 전체가 M번 반복 실행되는 것과 유사한 효과를 냅니다. 첫 번째 가게에 대한 탐색이 끝난 후에도 q가 비워지지 않고, 두 번째 가게 정보가 q에 추가된 상태로 다시 탐색을 시작합니다.

- 불필요한 연산: 이 구조는 의도하신 '여러 출발점에서 모든 노드까지의 최단 거리'를 한 번에 구하는 멀티 소스(multi-source) 다익스트라가 아닙니다. 이로 인해 시간 복잡도가 (M + P) * O(K log N)에 가깝게 증가하여 시간 초과를 유발합니다.

### 논리적 오류 가능성

`if next_id not in mSkip: continue` 부분에도 논리적 오류가 있습니다.

이 코드는 다음 탐색 대상을 mSkip(유망한 주택 후보군)으로 제한합니다. 하지만 커피점에서 주택까지 가는 최단 경로가 다른 커피점이나 제과점을 거쳐갈 수도 있습니다. 이 코드는 그러한 경로 탐색을 원천적으로 차단하므로, 실제 최단 거리를 구하지 못하고 틀린 답을 낼 가능성이 있습니다.

다행히 시간 초과가 발생한 것으로 보아, 이 논리적 오류를 검증하는 테스트 케이스 이전에 시간 제한에 걸린 것으로 보입니다.

## 해결 방안 및 추천 코드

문제를 해결하려면 정석적인 멀티 소스 다익스트라를 구현하고, 거리 조건 필터링은 다익스트라가 완전히 끝난 후에 수행해야 합니다.

- 올바른 다익스트라 함수: 시작점들을 먼저 모두 우선순위 큐에 넣고, 그 후에 while 루프를 한 번만 실행하여 모든 노드까지의 최단 거리를 계산합니다.
- 분리된 로직: calculate 함수에서 다익스트라를 두 번(커피점, 제과점) 호출하여 각 주택까지의 최단 거리 배열을 구합니다.
- 최종 필터링: 두 거리 배열을 이용해 R 조건을 만족하는 주택을 찾고, 거리 합의 최솟값을 계산합니다.
아래는 위 해결 방안을 적용한 추천 코드입니다.

### 수정된 dijkstra 함수

mSkip과 R 매개변수를 제거하여 순수하게 최단 거리를 계산하는 역할만 하도록 수정합니다.

```python
import heapq
from collections import defaultdict

# init, add 함수는 그대로 사용합니다.

def dijkstra(start_nodes):
    """
    여러 출발 노드(start_nodes)로부터 모든 건물까지의 최단 거리를 계산하는
    올바른 멀티 소스 다익스트라 함수
    """
    dist = [_N * 1000 + 1] * _N  # INF 값으로 초기화
    q = []

    # 1. 모든 시작점의 거리를 0으로 초기화하고 우선순위 큐에 추가
    for node in start_nodes:
        dist[node] = 0
        heapq.heappush(q, (0, node))

    # 2. 우선순위 큐를 이용한 다익스트라 로직을 한 번만 실행
    while q:
        curr_dist, curr_id = heapq.heappop(q)

        if curr_dist > dist[curr_id]:
            continue

        for next_id, next_dist in graph[curr_id]:
            new_dist = curr_dist + next_dist
            if new_dist < dist[next_id]:
                dist[next_id] = new_dist
                heapq.heappush(q, (new_dist, next_id))

    return dist

```

### 수정된 calculate 함수

수정된 dijkstra 함수를 호출하고, 모든 계산이 끝난 후 결과를 종합하여 답을 도출합니다.

```python
def calculate(M, mCoffee, P, mBakery, R):
    # 1. 커피점에서 모든 건물까지의 최단 거리 계산
    dist_from_coffee = dijkstra(mCoffee)
    
    # 2. 제과점에서 모든 건물까지의 최단 거리 계산
    dist_from_bakery = dijkstra(mBakery)

    min_total_dist = float('inf')
    found = False

    # 주택 ID 집합 생성
    shops = set(mCoffee) | set(mBakery)
    
    # 3. 모든 건물을 순회하며 조건을 만족하는 '주택'을 탐색
    for i in range(_N):
        if i in shops: # 현재 건물이 커피점이나 제과점이면 건너뜀
            continue

        # 현재 주택이 커피점과 제과점 양쪽에서 R 이하 거리에 있는지 확인
        if dist_from_coffee[i] <= R and dist_from_bakery[i] <= R:
            found = True
            total_dist = dist_from_coffee[i] + dist_from_bakery[i]
            min_total_dist = min(min_total_dist, total_dist)

    if not found:
        return -1
    else:
        return min_total_dist
```

## 요약

| 구분 | 기존 코드의 문제점 | 해결 방안 |
| --- | --- | --- |
| 성능 | for 루프 안에 while 루프가 중첩되어 다익스트라가 비효율적으로 반복 실행됨. | 시작점을 큐에 모두 넣고 while 루프를 한 번만 실행하는 올바른 멀티 소스 다익스트라로 수정. |
| 정확성 | 경로 탐색 시 주택이 아닌 노드를 건너뛰어 최단 경로를 놓칠 수 있음. | 다익스트라에서는 모든 노드를 방문하도록 허용하고, 거리 조건(R) 필터링은 나중에 수행. |

---

## 느낀점

최적화는 어렵다. 

직전에 공부한 다익스트라가 나와서 정답 근처에라도 갈 수 있었다. 

시간 줄이려고 거리합 연산 줄이는 데에만 신경썼는데 왜 for문을 없앨 생각을 못했을까… 자료형에 너무 집착한 듯. 결국 불필요한 반복을 없애는 것이 최적화의 핵심인 것 같다. 앞으로는 반복문부터 뜯어보자. 

아예 접근이라도 못했으면 미련없을텐데 뭔가 할수있었을것 같아서 더 아쉽다. 그래도 현장에서 할 수 있는 건 다 해봤으니됐다.