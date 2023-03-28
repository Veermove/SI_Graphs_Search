from common import time_diff


def cost_time(_, _current_stop, _next_stop, current_time, departure_time, _prev_line, _all_nodes):
    return time_diff(current_time, departure_time)

def cost_time_switch(_, current_stop, next_stop, current_time, departure_time, prev_line, all_nodes):

    current_line = all_nodes[current_stop].edges[next_stop][departure_time]['line']
    line_changed_cost = 10 if current_line != prev_line else 0

    return line_changed_cost + 0.3 * cost_time(_, current_stop, next_stop, current_time, departure_time, prev_line, all_nodes)

def cost_time_dist(end_stop, current_stop, next_stop, current_time, departure_time, prev_line, all_nodes):
    manhatan_cost = abs(all_nodes[next_stop].x - all_nodes[end_stop].x) \
                    + abs(all_nodes[next_stop].y - all_nodes[end_stop].y)

    return manhatan_cost + 0.5 * cost_time(end_stop, current_stop, next_stop, current_time, departure_time, prev_line, all_nodes)


def cost_time_switch_dist(end_stop, current_stop, next_stop, current_time, departure_time, prev_line, all_nodes):
    basic_cost = cost_time_switch(
        end_stop, current_stop, next_stop,
        current_time, departure_time,
        prev_line,
        all_nodes
    )

    manhatan_cost = abs(all_nodes[next_stop].x - all_nodes[end_stop].x) \
                    + abs(all_nodes[next_stop].y - all_nodes[end_stop].y)

    return manhatan_cost + 0.5 * basic_cost
