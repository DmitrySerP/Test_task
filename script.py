import argparse
import csv
from tabulate import tabulate


def arg_cmdline():
    arg_cmd = argparse.ArgumentParser(description="Process CSV file")
    arg_cmd.add_argument("--file", help="Путь к CSV-файлу")
    arg_cmd.add_argument("--where", help="Условие фильтрации, например 'price<1000'")
    arg_cmd.add_argument("--aggregate", help="Агрегация, например 'avg=rating'")
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
    try:
        float(data[0][column])
        return True
    except (ValueError, KeyError):
        return False

def parse_where(where):
    if not where:
        return None, None, None
    for op in ["<", ">", "="]:
        if op in where:
            column, value = where.split(op)
            return column.strip(), op, value.strip()
    raise ValueError("Неверный формат where, используйте column<value, column>value или column=value")

def parse_aggregate(aggregate):
    if not aggregate:
        return None, None
    try:
        function, column = aggregate.split("=")
        if function not in ["avg", "min", "max"]:
            raise ValueError("Неверный формат агрегации, используйте avg, min или max")
        return function, column.strip()
    except ValueError:
        raise ValueError("Неверный формат агрегации, используйте function=column, например avg=rating")


def filter_data(data, column, operator, value):
    if not column or not operator or not value:
        return data
    filtered_data = []
    is_numeric = is_numeric_column(data, column)

    if is_numeric:
        filter_value = float(value)
    else:
        filter_value = value

    for row in data:
        try:
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
        except KeyError:
            continue
    return filtered_data

def aggregate_data(data, agg_function, agg_column):
    if not data or not agg_function or not agg_column:
        return None

    if not is_numeric_column(data, agg_column):
        return "Aggregation is only possible for numeric columns."

    values = []
    for row in data:
        try:
            value = float(row[agg_column])
            values.append(value)
        except KeyError:
            continue

    if not values:
        return None

    if agg_function == "avg":
        total = sum(values)
        return total / len(values)
    elif agg_function == "min":
        return min(values)
    elif agg_function == "max":
        return max(values)
    return None

def print_result(data, agg_result, agg_function, agg_column):
    if data:
        print(tabulate(data, headers="keys", tablefmt="pipe"))

    if agg_result is not None:
        if isinstance(agg_result, str):
            print(agg_result)
        else:
            print(f"{agg_function.capitalize()} {agg_column}: {agg_result:.6f}")
    return None

def main():
    args = arg_cmdline()
    try:
        data = read_csv(args.file)
        column, operator, value = parse_where(args.where)
        filtered_data = filter_data(data, column, operator, value)
        agg_function, agg_column = parse_aggregate(args.aggregate)
        agg_result = aggregate_data(filtered_data, agg_function, agg_column)
        print_result(filtered_data, agg_result, agg_function, agg_column)
    except(FileNotFoundError, ValueError) as e:
        print(f"Ошибка: {e}")
    return None

if __name__ == "__main__":
    main()


