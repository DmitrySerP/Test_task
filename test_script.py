import pytest
import csv
from script import read_csv, filter_list, aggregate_data, print_result

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

def test_filter_numeric(sample_csv):
    data = read_csv(sample_csv)
    filtered = filter_list(data, "price", ">", "500")
    assert len(filtered) == 2
    assert filtered[0]["name"] == "iphone 15 pro"
    assert filtered[1]["name"] == "galaxy s23 ultra"

def test_filter_text(sample_csv):
    data = read_csv(sample_csv)
    filtered = filter_list(data, "brand", "=", "xiaomi")
    assert len(filtered) == 1
    assert filtered[0]["name"] == "redmi note 12"

def test_filter_less(sample_csv):
    data = read_csv(sample_csv)
    filtered = filter_list(data, "price", "<", "1000")
    assert len(filtered) == 2
    assert filtered[0]["name"] == "iphone 15 pro"
    assert filtered[1]["name"] == "redmi note 12"

def test_filter_empty(sample_csv):
    data = read_csv(sample_csv)
    filtered = filter_list(data, None, None, None)
    assert len(filtered) == 3

def test_aggregate_avg(sample_csv):
    data = read_csv(sample_csv)
    result = aggregate_data(data, "avg", "rating")
    assert abs(result - 4.76666666666667) < 0.0001

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
    assert "Avg rating: 4.76666666667" in captured.out







