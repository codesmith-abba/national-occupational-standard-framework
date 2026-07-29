from pathlib import Path
import json


class JSONLoader:

    def load(self, path: Path | str):
        """
        Load one JSON file or all JSON files under a directory.

        Returns:
            list[tuple[Path, dict]]
        """
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path)

        if path.is_file():
            return [(path, self._load_file(path))]

        files = sorted(path.rglob("*.json"))

        return [
            (file, self._load_file(file))
            for file in files
        ]

    def _load_file(self, file: Path) -> dict:
        with file.open("r", encoding="utf-8") as f:
            return json.load(f)