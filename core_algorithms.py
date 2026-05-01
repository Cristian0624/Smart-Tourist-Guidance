import math

# Distance calculation using Haversine formula

def distance_haversine(p1, p2):
    R = 6371  # Earth radius in kilometers

    lat1, lon1 = math.radians(p1['latitude']), math.radians(p1['longitude'])
    lat2, lon2 = math.radians(p2['latitude']), math.radians(p2['longitude'])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Union-Find (Disjoint Set Union) implementation for Kruskal's algorithm

class union_find():
    def __init__(self, n):
        self.parent = list(range(n))
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False
        self.parent[root_y] = root_x
        return True

def mst_kruskal(points):
    edges = []
    n = len(points)

    # Create edges with distances
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance_haversine(points[i], points[j])
            edges.append((dist, i, j))

    # Sort edges by distance
    edges.sort()

    uf = union_find(n)
    mst_edges = [[] for _ in range(n)]

    for dist, u, v in edges:
        if uf.union(u, v):
            mst_edges[u].append(v)
            mst_edges[v].append(u)

    return mst_edges

# DFS traversal to get a route from the MST

def dfs(mst, start = 0):
    visited = [False] * len(mst)
    route = []

    def visit(node):
        visited[node] = True
        route.append(node)
        for neighbor in mst[node]:
            if not visited[neighbor]:
                visit(neighbor)

    visit(start)
    return route

# Calculate total distance of a given route

def calculate_distance(route, points):
    total = 0
    for i in range(len(route) - 1):
        total += distance_haversine(points[route[i]], points[route[i + 1]])
    return total

# -----------------------------
# 2-Opt optimization
# -----------------------------
def two_opt(route, points):
    best = route
    improved = True
    
    while improved:
        improved = False
        best_distance = calculate_distance(best, points)
        
        for i in range(1, len(best) - 2):
            for j in range(i + 1, len(best)):
                if j - i == 1:
                    continue
                
                new_route = best[:]
                new_route[i:j] = reversed(best[i:j])
                
                new_distance = calculate_distance(new_route, points)
                
                if new_distance < best_distance:
                    best = new_route
                    improved = True
                    break
            if improved:
                break
    
    return best

def solve_tsp(points):
    # Step 1: Construct MST using Kruskal's algorithm
    mst = mst_kruskal(points)
    # Step 2: Get an initial route using DFS traversal of the MST
    initial_route = dfs(mst)
    # Step 3: Optimize the route using 2-Opt algorithm
    optimized_route = two_opt(initial_route, points)
    # Step 4: Return ordered indices
    return optimized_route

if __name__ == "__main__":
    points = [
        {"name": "A", "latitude": 47.0105, "longitude": 28.8638},
        {"name": "B", "latitude": 47.0200, "longitude": 28.8500},
        {"name": "C", "latitude": 47.0300, "longitude": 28.8700},
        {"name": "D", "latitude": 47.0150, "longitude": 28.8800},
        {"name": "E", "latitude": 47.0250, "longitude": 28.8400},
    ]
    
    route = solve_tsp(points)
    
    print("Optimized Route:")
    for i in route:
        print(points[i]["name"])
    
    print(f"Total distance: {calculate_distance(route, points):.3f} km")