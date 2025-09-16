import heapq

def init(N, K, sBuilding, eBuilding, mDistance):
	global graph, gN
	graph = [[] for _ in range(N+1)]
	gN = N
	for i in range(K) :
		graph[sBuilding[i]].append((eBuilding[i], mDistance[i]))
		graph[eBuilding[i]].append((sBuilding[i], mDistance[i]))
	return


def add(sBuilding, eBuilding, mDistance):
	global graph
	graph[sBuilding].append((eBuilding, mDistance))
	graph[eBuilding].append((sBuilding, mDistance))
	return


def calculate(M, mCoffee, P, mBakery, R):
	global graph, gN
	ans = 987654321
	hq = []
	visit = [[-1] * (gN+1) for _ in range(2) ]
	for i in range(M):
		heapq.heappush(hq, (0, mCoffee[i], 0))
	for i in range(P):
		heapq.heappush(hq, (0, mBakery[i], 1))

	while hq :
		dist, tId, CB = heapq.heappop(hq)
		if visit[CB][tId] != -1:
			continue
		visit[CB][tId] = dist

		if visit[0][tId] > 0 and visit[1][tId] > 0 :
			if ans > visit[0][tId] + visit[1][tId]:
				ans = visit[0][tId] + visit[1][tId]
			else :
				continue

		for nxt in graph[tId] :
			if dist + nxt[1] > R or dist + nxt[1] > ans or visit[CB][nxt[0]] != -1: 
				continue
			heapq.heappush(hq, (dist + nxt[1], nxt[0], CB))

	if ans == 987654321 : return -1
	return ans