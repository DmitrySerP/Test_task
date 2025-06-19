import pytest
import csv
import subprocess
from script import read_csv, filter_data, aggregate_data, print_result, parse_where, parse_aggregate

@pytest.fixture
def sample_csv(tmp_path):
    file_path = tmp_path / 'test.csv'
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["name", "brand", "price", "rating"])
        writer.writerow(["iphone 15 pro", "apple", "999", "4.9"])
        writer.writerow(["galaxy s23 ultra", "samsung", "1199", "4.8"])
        writer.writerow(["redmi note 12", "xiaomi", "199", "4.6"])
    return str(file_path)

@pytest.fixture
def empty_csv(tmp_path):
    file_path = tmp_path / "empty.csv"
    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "brand", "price", "rating"])
    return str(file_path)

def test_read_csv(sample_csv):
    data = read_csv(sample_csv)
    assert len(data) == 3
    assert data[0]["name"] == "iphone 15 pro"
    assert data[2]["price"] == "199"

def test_parse_where(sample_csv):
    assert parse_where("price>500") == ("price", ">", "500")
    assert parse_where("brand=xiaomi") == ("brand", "=", "xiaomi")
    assert parse_where(None) == (None, None, None)

def test_parse_aggregate(sample_csv):
    assert parse_aggregate("avg=rating") == ("avg", "rating")
    assert parse_aggregate("max=price") == ("max", "price")
    assert parse_aggregate(None) == (None, None)


def test_filter_numeric(sample_csv):
    data = read_csv(sample_csv)
    filtered = filter_data(data, "price", ">", "500")
    assert len(filtered) == 2
    assert filtered[0]["name"] == "iphone 15 pro"
    assert filtered[1]["name"] == "galaxy s23 ultra"

def test_filter_text(sample_csv):
    data = read_csv(sample_csv)
    filtered = filter_data(data, "brand", "=", "xiaomi")
    assert len(filtered) == 1
    assert filtered[0]["name"] == "redmi note 12"

def test_filter_less(sample_csv):
    data = read_csv(sample_csv)
    filtered = filter_data(data, "price", "<", "1000")
    assert len(filtered) == 2
    assert filtered[0]["name"] == "iphone 15 pro"
    assert filtered[1]["name"] == "redmi note 12"

def test_filter_empty(sample_csv):
    data = read_csv(sample_csv)
    filtered = filter_data(data, None, None, None)
    assert len(filtered) == 3

def test_aggregate_avg(sample_csv):
    data = read_csv(sample_csv)
    result = aggregate_data(data, "avg", "rating")
    assert abs(result - 4.766667) < 0.0001

def test_aggregate_min(sample_csv):
    data = read_csv(sample_csv)
    result = aggregate_data(data, "min", "price")
    assert result == 199

def test_aggregate_max(sample_csv):
    data = read_csv(sample_csv)
    result = aggregate_data(data, "max", "price")
    assert result == 1199.0

def test_aggregate_error(sample_csv):
    data = read_csv(sample_csv)
    result = aggregate_data(data, "avg", "brand")
    assert result == "Aggregation is only possible for numeric columns."

def test_print_result(capsys, sample_csv):
    data = read_csv(sample_csv)
    print_result(data, 4.766666666666667, "avg", "rating")
    captured = capsys.readouterr()
    assert "iphone 15 pro" in captured.out
    assert "Avg rating: 4.766667" in captured.out

def test_main(sample_csv):
    result = subprocess.run(
        [r".venv\Scripts\python.exe", "script.py", "--file", sample_csv, "--where", "price>500", "--aggregate", "avg=rating"],
        capture_output=True, text=True
    )
    print(result.stderr)
    assert "iphone 15 pro" in result.stdout
