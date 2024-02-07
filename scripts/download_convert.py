import requests
import geojson
import csv
from pathlib import Path

def download_csv(url, path):
    response = requests.get(url)
    response.raise_for_status()  # エラー時に例外を発生
    with open(path, 'w') as file:
        file.write(response.text)

def csv_to_geojson(csv_path, geojson_path):
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        features = []
        for row in reader:
            point = geojson.Point((float(row['経度']), float(row['緯度'])))
            features.append(geojson.Feature(geometry=point, properties=row))
        feature_collection = geojson.FeatureCollection(features)
        with open(geojson_path, 'w') as f:
            geojson.dump(feature_collection, f)

def main():
    urls = [
        "https://opendata.pref.shizuoka.jp/dataset/fuji-156/resource/32450/%E6%B2%B3%E5%B7%9D%E3%82%AB%E3%83%A1%E3%83%A9%EF%BC%88202010401%EF%BC%89.csv",
        "https://www.opendata.metro.tokyo.lg.jp/kensetsu/R4/130001_river_monitoring_cameras.csv"
    ]
    csv_paths = ["data/shizuoka_river_cameras.csv", "data/tokyo_river_cameras.csv"]
    geojson_paths = ["data/shizuoka_river_cameras.geojson", "data/tokyo_river_cameras.geojson"]

    for url, csv_path, geojson_path in zip(urls, csv_paths, geojson_paths):
        # CSVファイルをダウンロード
        download_csv(url, csv_path)
        # CSVからGeoJSONへの変換
        csv_to_geojson(csv_path, geojson_path)
        print(f"GeoJSON saved to {geojson_path}")

if __name__ == "__main__":
    main()


