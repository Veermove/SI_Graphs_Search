import math
import bisect

def read_file():
    with open("connection_graph.csv", "r") as file:
        lines = file.readlines()
        headers = lines[0].replace('\n', '').split(',')[1:]
        print(headers)
        data = []
        for l in lines[1:]:
            ld = {}
            for i, field in enumerate(l.replace('\n', '').split(',')[1:]):
                ld[headers[i]] = field
            data.append(ld)
        return data

class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.x = float(x)
        self.y = float(y)
        self.edges = {}

    def __str__(self) -> str:
        return str(self.name) + ", " + str(self.x) + ", " + str(self.y)

    def print_node(self):
        print(str(self.name) + ", " + str(self.x) + ", " + str(self.y))
        for (_, v) in self.edges.items():
            print(v[0])


def spawn_graph(data):
    nodes: dict[str, Node] = {}
    for ld in data:
        nodes[ld['start_stop']] = Node(ld['start_stop'], ld['start_stop_lat'], ld['start_stop_lon'])

        if ld['end_stop'] not in nodes:
            nodes[ld['end_stop']] = Node(ld['end_stop'], ld['end_stop_lat'], ld['end_stop_lon'])

    for ld in data:
        if ld['start_stop'] != ld['end_stop']:
            if not nodes[ld['start_stop']].edges[ld['end_stop']]:
                nodes[ld['start_stop']].edges[ld['end_stop']] = {}

            nodes[ld['start_stop']].edges[ld['end_stop']][ld['departure_time']] = ld['arrival_time']

    return nodes


def sp_dijkstra(start, end, data, start_time):
    if start not in data or end not in data:
        return None

    dist = {}
    prev = {}

    for k in data.keys():
        dist[k] = math.inf
        prev[k] = None

    queue = []
    visited: set[str] = set()

    queue.append((start, start_time, 0))
    dist[start] = 0

    while queue:
        (name, current_time, _) = queue.pop(0)

        # print("==================")
        # for k, v in prev.items():
        #     print(k.ljust(45), v)

        # print("==================")

        if name == end:
            break

        print(current_time,name.ljust(40))
        for (to, departures) in data[name].edges.items():
            for (dt, at) in departures.items():
                # print(to.ljust(40), dt, time_diff(current_time, dt))
                if to not in visited and time_diff(dt, current_time) < 0:
                    alt = dist[name] + time_diff(dt, at)
                    # print(alt, dist[name], name, to)
                    if alt < dist[to]:
                        prev[to] = name
                        dist[to] = alt
                        bisect.insort_left(queue, (to, at, time_diff(current_time, dt)), key= lambda x: x[2])
        # print(queue)
        visited.add(name)

    path = []
    u = end
    if prev[u] or u == start:
        while prev[u]:
            path.insert(0, u)
            u = prev[u]
        path.insert(0, u)

    print(path)







def time_diff(dep_time, arr_time):
    dt = dep_time.split(':')
    at = arr_time.split(':')

    return ((int(at[0]) * 60) + int(at[1])) - ((int(dt[0]) * 60) + int(dt[1]))






def main():
    data = read_file()
    graph = spawn_graph(data)
    sp_dijkstra("GALERIA DOMINIKAŃSKA", "pl. Legionów", graph, "09:31:00")




if __name__ == '__main__':
    main()
