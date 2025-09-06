# 내 풀이 복기
# 다익스트라로 접근

from collections import defaultdict
import heapq

def init(N, K, sBuilding, eBuilding, distance):
    global _N, graph, INF
    _N = N
    graph = defaultdict(list)
    INF = K * 1000
    
    for i in range(K):
        add(sBuilding[i], eBuilding[i], distance[i])
        
    
def add(sBuilding, eBuilding, distance):
    graph[sBuilding].append((eBuilding, distance))
    graph[eBuilding].append((sBuilding, distance))


def dijkstra(mShop, mSkip, R):
    """
    mShop을 출발지로 하는 거리 리스트 중 R 이하인 거리만 저장
    mSkip은 유망한 건물의 ID set
    """
    dist = [INF] * _N
    q = []
  
    for shop_id in mShop:
        dist[shop_id] = 0
        heapq.heappush(q, (0, shop_id))
        while q:
            curr_dist, curr_id = heapq.heappop(q)
            if curr_dist > dist[curr_id]:
                continue
            
            for next_id, next_dist in graph[curr_id]:
                if next_id not in mSkip:
                    continue
                if curr_dist + next_dist >= dist[next_id]:
                    continue
                dist[next_id] = curr_dist + next_dist
                heapq.heappush(q, (dist[next_id], next_id))
        
    limited_dist = defaultdict(int)
    for idx in mSkip:
        if 0 < dist[idx] <= R:
            limited_dist[idx] = dist[idx]
    
    return limited_dist 


def calculate(M, mCoffee, P, mBakery, R):
    mHouse = set(range(_N)) - set(mCoffee) - set(mBakery)
    cafe = dijkstra(mCoffee, mHouse, R)
    mHouse = set(cafe.keys())
    bakery = dijkstra(mBakery, mHouse, R)
    
    if not bakery:
        return -1
    
    min_dist = min(cafe[cId] + bakery[cId] for cId in bakery.keys())
    return min_dist
