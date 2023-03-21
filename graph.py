import math
import bisect

def read_file():
    with open("connection_graph.csv", "r") as file:
        lines = file.readlines()
        headers = lines[0].replace('\n', '').split(',')[1:]
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

def spawn_graph(data):
    nodes: dict[str, Node] = {}
    for ld in data:
        nodes[ld['start_stop']] = Node(ld['start_stop'], ld['start_stop_lat'], ld['start_stop_lon'])

        if ld['end_stop'] not in nodes:
            nodes[ld['end_stop']] = Node(ld['end_stop'], ld['end_stop_lat'], ld['end_stop_lon'])

    for ld in data:
        if ld['start_stop'] != ld['end_stop']:
            if ld['end_stop'] not in nodes[ld['start_stop']].edges:
                nodes[ld['start_stop']].edges[ld['end_stop']] = {}

            nodes[ld['start_stop']].edges[ld['end_stop']][ld['departure_time']] = dict([
                ('arrival_time',   ld['arrival_time']),
                ('departure_time', ld['departure_time']),
                ('company',        ld['company']),
                ('line',           ld['line'])
            ])

    return nodes

                                                     # start_stop
                                                     #  |    end_stop
                                                     #  |     |   connection data
def sp_dijkstra(start, end, data, start_time, cost_function) -> list[(str, str, dict)]:
    # validate inputs
    if start not in data or end not in data:
        assert False, "Provided data is incorrect"

    # initialize dictionaries
    dist = { name: math.inf for (name) in data.keys() }
    prev = { name: None     for (name) in data.keys() }
    visited = set()

            # stop   time       line  cost
    queue = [(start, start_time, None, 0)]
    dist[start] = 0

    while queue:
        (current_stop, current_time, prev_line, _) = queue.pop(0)

        if current_stop == end:
            break

        for (next_stop, departures) in data[current_stop].edges.items():
            for (departure_time, connections) in departures.items():
                if next_stop not in visited and time_diff(current_time, departure_time) >= 0:

                    # calculate cost usinng provided cost function
                    alternative = cost_function(
                            end,
                            current_stop,
                            next_stop,
                            current_time,
                            departure_time,
                            prev_line,
                            dist[current_stop],
                            data
                        )

                    # add neighbour to (sorted) queue,
                    # compare using alternative cost
                    bisect.insort_right(
                        queue,
                        (next_stop, connections['arrival_time'], connections['line'], alternative),
                        key=lambda x: x[3]
                    )

                    # if current way is better than remembered
                    # remember this way
                    if alternative <= dist[next_stop]:
                        prev[next_stop] = (current_stop, next_stop, connections)
                        dist[next_stop] = alternative

        visited.add(current_stop)


    path = []
    u = end

    if prev[u] or u == start:
        while prev[u]:
            (u, c, time) = prev[u]
            path.insert(0, (u, c, time))

    # list of (start_name, end_name, connection_data)
    return path

def time_diff(dep_time, arr_time):
    dt = dep_time.split(':')
    at = arr_time.split(':')

    return ((int(at[0]) * 60) + int(at[1])) - ((int(dt[0]) * 60) + int(dt[1]))

def print_path(path):
    max_stop_name_len = pipe(
        { stop_data[0] for stop_data in path },
        lambda name_set: name_set.union({ stop_data[1] for stop_data in path }),
        lambda names: map(lambda x: len(x), names),
        max
    )

    for k, f, v in path:
        print(k.ljust(max_stop_name_len), f.ljust(max_stop_name_len), v['departure_time'], v['arrival_time'], v['line'])

def dijkstra_cost_function(_, current_stop, next_stop, current_time, departure_time, prev_line, current_best_distance, all_nodes):

    current_line = all_nodes[current_stop].edges[next_stop][departure_time]['line']

    # prioritize not changing lines
    # changing lines is equal to waiting 10 minutes
    line_changed_cost = 10 if current_line != prev_line else 0

    return current_best_distance + time_diff(current_time, departure_time) + line_changed_cost

def astar_cost_function(end_stop, current_stop, next_stop, current_time, departure_time, prev_line, current_best_distance, all_nodes):
    basic_cost = dijkstra_cost_function(
        end_stop, current_stop, next_stop,
        current_time, departure_time,
        prev_line,
        current_best_distance,
        all_nodes
    )

    manhatan_cost = abs(all_nodes[next_stop].x - all_nodes[end_stop].x) \
                    + abs(all_nodes[next_stop].y - all_nodes[end_stop].y)

    return manhatan_cost + basic_cost


def main():
    data = read_file()
    graph = spawn_graph(data)
    path = sp_dijkstra("GALERIA DOMINIKAŃSKA", "pl. Legionów", graph, "09:31:00", dijkstra_cost_function)
    # path = sp_dijkstra('Mokronos Dolny - Parkowa/Stawowa', 'Psie Pole', graph, '08:46:00', dijkstra_cost_function)
    # path = sp_dijkstra('Mokronos Dolny - Parkowa/Stawowa', 'Mirków - Sportowa', graph, '19:46:00', astar_cost_function)
    print_path(path)


def pipe(start_value, *args):
    if not args:
        return start_value

    v = start_value
    for func in args:
        v = func(v)
    return v


if __name__ == '__main__':
    main()
