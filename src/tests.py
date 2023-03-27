
from common import measure_time, pipe, random_stops, read_file
from cost_functions import cost_time, cost_time_switch, cost_time_switch_dist
from graph import analyze_path, print_path, shortest_path, spawn_graph

def main():
    data = read_file("./connection_graph.csv")
    graph = spawn_graph(data)
    ran = random_stops(graph, 5, 2, 1, 4)

    # pipe(["Grota-Roweckiego", "most Grunwaldzki"],
    #     lambda stops_to_visit: measure_time(lambda:
    #         shortest_path(graph, stops_to_visit, "12:26:00", cost_time_switch_dist)
    #     ),
    #     lambda path_time: analyze_path("12:26:00", path_time[0], path_time[1]),
    #     lambda path_time: print_path(path_time[0])
    # )
    # pipe(["GALERIA DOMINIKAŃSKA", "Dyrekcyjna"],
    #     lambda stops_to_visit: measure_time(lambda:
    #         shortest_path(graph, stops_to_visit, "07:51:00", cost_time)
    #     ),
    #     lambda path_time: analyze_path("07:51:00", path_time[0], path_time[1]),
    # )

    print("scenario_len,different_lines,travel_time_in_mins,search_time,avg_wait_time")
    for cost_function in [cost_time, cost_time_switch, cost_time_switch_dist]:
        for batch in ran:
            for scenario in batch:

                print(len(scenario), end=",")

                pipe(scenario,
                    lambda stops_to_visit:
                        measure_time(lambda:
                            shortest_path(graph, stops_to_visit, "14:00:00", cost_function)
                        ),
                    lambda path_time: analyze_path("14:00:00", path_time[0], path_time[1]),
                )
                print("")
        print("")


    # print(time)

if __name__ == '__main__':
    main()
