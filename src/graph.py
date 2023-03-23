import math
import bisect

from common import pipe, time_diff

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

def shortest_path(data, stops_to_visit, start_time, cost_function):
    if len(stops_to_visit) <= 1:
        assert False, "Must provide at least start and end stop"

    path = []
    current_time = start_time
    for (starting, ending) in list(zip(stops_to_visit, stops_to_visit[1:] + stops_to_visit[:1]))[:-1]:
        sub_path = sp_dijkstra(starting, ending, data, current_time, cost_function)

        if not sub_path:
            # print("FAILED TO FIND PATH BETWEEN: ", starting, " AND ", ending)
            return

        assert sub_path[0][0] == starting, "Starting point incorrect"
        assert sub_path[-1][1] == ending, "Ending point incorrect"

        current_time = sub_path[-1][2]['arrival_time']
        path += sub_path

    return path


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

        # if current_stop in visited:
        #     continue

        for (next_stop, departures) in data[current_stop].edges.items():
            for (departure_time, connection_info) in departures.items():
                if next_stop not in visited and time_diff(current_time, departure_time) >= 0:
                    # if current_stop == 'Arkady (Capitol)' or current_stop == 'Renoma' or current_stop == "DWORZEC GŁÓWNY":
                    #     print(current_stop, next_stop, current_time, departure_time, time_diff(current_time, departure_time), connection_info['arrival_time'], connection_info['line'])

                    # calculate cost using provided cost function
                    alternative = dist[current_stop] + cost_function(
                            end,
                            current_stop,
                            next_stop,
                            current_time,
                            departure_time,
                            prev_line,
                            data
                        )

                    # add neighbour to (sorted) queue,
                    # compare using alternative cost
                    bisect.insort_right(
                        queue,
                        (next_stop, connection_info['arrival_time'], connection_info['line'], alternative),
                        key=lambda x: x[3]
                    )

                    # if current way is better than remembered
                    # remember this way
                    if alternative <= dist[next_stop]:
                        prev[next_stop] = (current_stop, next_stop, connection_info)
                        dist[next_stop] = alternative

        print("=============================", current_stop, current_time)
        for a in queue:
            print(a)

        visited.add(current_stop)


    path = []
    u = end

    if prev[u] or u == start:
        while prev[u]:
            (u, c, time) = prev[u]
            path.insert(0, (u, c, time))

    # list of (start_name, end_name, connection_data)
    return path

def analyze_path(start_time, path, time):
    if path:
        different_lines: set[str] = { travel_data[2]['line'] for travel_data in path }
        total_travel_minutes = time_diff(path[0][2]['departure_time'], path[-1][2]['arrival_time'])

        avg_wait_time = pipe(path,
            lambda k: ([start_time] + [s[2]['arrival_time'] for s in k][:-1],  [s[2]['departure_time'] for s in k]),
            lambda arr_dep: zip(arr_dep[1], arr_dep[0]),
            lambda dep_arr: map(lambda d_a: time_diff(d_a[1], d_a[0]), dep_arr),
            list,
            lambda wait_times:  print(wait_times)#sum(wait_times) / len(wait_times)
        )

        # if avg_wait_time < 0:
        print_path(path)

        print(len(different_lines), end=",")
        print(total_travel_minutes, end=",")
        print(time, end=",")
        print(avg_wait_time, end=",")
    else:
        print(",,,", end="")
    return path, time


def print_path(path):
    if not path:
        return path
    max_stop_name_len = pipe(
        { stop_data[0] for stop_data in path },
        lambda name_set: name_set.union({ stop_data[1] for stop_data in path }),
        lambda names: map(lambda x: len(x), names),
        max
    )

    for k, f, v in path:
        print(k.ljust(max_stop_name_len), f.ljust(max_stop_name_len), v['departure_time'], v['arrival_time'], v['line'])

    return path
