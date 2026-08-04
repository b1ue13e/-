from __future__ import annotations

from pathlib import Path
from urllib.request import urlretrieve


FILES = {
    "covid.train.csv": "https://drive.google.com/uc?export=download&id=19CCyCgJrUxtvgZF53vnctJiOJ23T5mqF",
    "covid.test.csv": "https://drive.google.com/uc?export=download&id=1CE240jLm2npU-tdz81-oVKEF3T2yfT1O",
}


def main() -> None:
    data_dir = Path(__file__).resolve().parents[2] / "data" / "ml_hw01"
    data_dir.mkdir(parents=True, exist_ok=True)

    for filename, url in FILES.items():
        output_path = data_dir / filename
        print(f"Downloading {filename} -> {output_path}")
        urlretrieve(url, output_path)

    print("Done.")


if __name__ == "__main__":
    main()
