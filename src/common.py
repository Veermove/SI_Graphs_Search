from timeit import default_timer as timer
import random

def time_diff(dep_time, arr_time):
    dt = dep_time.split(':')
    at = arr_time.split(':')

    return ((int(at[0]) * 60) + int(at[1])) - ((int(dt[0]) * 60) + int(dt[1]))

def pipe(start_value, *args):
    if not args:
        return start_value

    v = start_value
    for func in args:
        v = func(v)
    return v

def read_file(path_to_file):
    with open(path_to_file, "r") as file:
        lines = file.readlines()
        headers = lines[0].replace('\n', '').split(',')[1:]
        data = []
        for l in lines[1:]:
            ld = {}
            for i, field in enumerate(l.replace('\n', '').split(',')[1:]):
                ld[headers[i]] = field
            data.append(ld)
        return data


def measure_time(callback):
    start = timer()
    result = callback()
    end = timer()
    return(result, (end - start))

def random_stops(data, batch_size, stops_in_first_batch, increment_per_batch, batch_number):
    batches = []
    current_number_of_stops_to_draw = stops_in_first_batch
    for i in range(0, batch_number):
        batch = []
        for j in range(0, batch_size):
            batch.append(random.sample(list(data.keys()), current_number_of_stops_to_draw))
        batches.append(batch)
        current_number_of_stops_to_draw += increment_per_batch
    return batches
