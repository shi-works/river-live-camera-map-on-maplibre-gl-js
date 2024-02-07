import requests
import geojson
import csv
from pathlib import Path

def download_csv(url, path, encoding):
    response = requests.get(url)
    response.raise_for_status()  # エラー時に例外を発生
    path = Path(path)
    # ディレクトリが存在しない場合は作成
    path.parent.mkdir(parents=True, exist_ok=True)
    # レスポンスのバイトデータをファイルに書き込む
    with open(path, 'wb') as file:
        file.write(response.content)

def csv_to_geojson(csv_path, geojson_path, encoding='utf-8'):
    with open(csv_path, newline='', encoding=encoding) as csvfile:
        reader = csv.DictReader(csvfile)
        features = []
        for row in reader:
            # 緯度経度の値が空でないことを確認
            if row['経度'] and row['緯度']:
                try:
                    # 緯度経度のデータを取得し、GeoJSONのポイントに変換
                    point = geojson.Point((float(row['経度']), float(row['緯度'])))
                    features.append(geojson.Feature(geometry=point, properties=row))
                except ValueError as e:
                    # 緯度経度の変換に失敗した場合のエラーハンドリング
                    print(f"Error converting row to GeoJSON: {e}")
                    continue
            else:
                # 緯度または経度が空の場合はスキップ
                continue

        feature_collection = geojson.FeatureCollection(features)
        # GeoJSONをUTF-8で保存
        with open(geojson_path, 'w', encoding='utf-8') as f:
            geojson.dump(feature_collection, f, ensure_ascii=False)

def main():
    urls = [
        "https://opendata.pref.shizuoka.jp/dataset/fuji-156/resource/32450/%E6%B2%B3%E5%B7%9D%E3%82%AB%E3%83%A1%E3%83%A9%EF%BC%88202010401%EF%BC%89.csv",
        "https://www.opendata.metro.tokyo.lg.jp/kensetsu/R4/130001_river-monitoring-cameras.csv"
    ]
    csv_paths = ["data/shizuoka_river_cameras.csv", "data/tokyo_river_cameras.csv"]
    geojson_paths = ["data/shizuoka_river_cameras.geojson", "data/tokyo_river_cameras.geojson"]
    encodings = ["cp932", "utf-8"]  # シフトJISとUTF-8のエンコーディング

    for url, csv_path, geojson_path, encoding in zip(urls, csv_paths, geojson_paths, encodings):
        # CSVファイルをダウンロード
        download_csv(url, csv_path, encoding)
        # CSVからGeoJSONへの変換
        csv_to_geojson(csv_path, geojson_path, encoding)
        print(f"GeoJSON saved to {geojson_path}")

if __name__ == "__main__":
    main()
