import argparse
import csv
from tabulate import tabulate


def arg_cmdline():
    arg_cmd = argparse.ArgumentParser(description="Process CSV file")
    arg_cmd.add_argument("file")
    arg_cmd.add_argument("--filter-col")
    arg_cmd.add_argument("--op", choices=["<", ">", "="])
    arg_cmd.add_argument("--val")
    arg_cmd.add_argument("--agg", choices=["avg", "min", "max"])
    arg_cmd.add_argument("--agg-col")
    return arg_cmd.parse_args()

def read_csv(file_path):
    data = []
    with open(file_path, newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
        return data

def is_numeric_column(data, column):
    if not data:
        return False
    value = data[0][column]
    try:
        float(value)
        return True
    except ValueError:
        return False

def filter_list(data, column, operator, value):
    if not column or not operator or not value:
        return data
    filtered_data = []
    is_numeric = is_numeric_column(data, column)

    if is_numeric:
        filter_value = float(value)
    else:
        filter_value = value

    for row in data:
        cell_value = row[column]
        if is_numeric:
            cell_value = float(cell_value)

        if operator == ">":
            if cell_value >filter_value:
                filtered_data.append(row)
        if operator == "<":
            if cell_value < filter_value:
                filtered_data.append(row)
        if operator == "=":
            if cell_value == filter_value:
                filtered_data.append(row)
    return filtered_data


def aggregate_data(data, agg_type, agg_column):
    if not data or not agg_type or not agg_column:
        return None

    if not is_numeric_column(data, agg_column):
        return "Aggregation is only possible for numeric columns."

    values = []
    for row in data:
        value = float(row[agg_column])
        values.append(value)

    if agg_type == "avg":
        total = 0
        for value in values:
            total += value
        return total / len(values)
    elif agg_type == "min":
        smallest = values[0]
        for value in values:
            if value < smallest:
                smallest = value
        return smallest
    elif agg_type == "max":
        largest = values[0]
        for value in values:
            if value > largest:
                largest = value
        return largest
    return None

def print_result(data, agg_result, agg_type, agg_column):
    if data:
        print(tabulate(data, headers="keys", tablefmt="pipe"))

    if agg_result is not None:
        if isinstance(agg_result, str):
            print(agg_result)
        else:
            print(f"{agg_type.capitalize()} {agg_column}: {agg_result:.11f}")
    return None

def main():
    args = arg_cmdline()
    data = read_csv(args.file)
    filtered_data = filter_list(data, args.filter_col, args.op, args.val)
    agg_result = aggregate_data(filtered_data, args.agg, args.agg_col)
    print_result(filtered_data, agg_result, args.agg, args.agg_col)
    return None
if __name__ == "__main__":
    main()


