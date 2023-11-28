from abc import ABC, abstractmethod
import shutil
import sqlite3
import zipfile
from collections import namedtuple
from http import HTTPStatus
from http.client import responses
from pathlib import Path

import pandas
import requests

DATABASE_ROOT = Path("pythonapi/db")
DATABASE_FILE = DATABASE_ROOT / Path("philadelphia.db")
DATABASE_CACHE = DATABASE_ROOT / Path("cache")


class Cmd(ABC):
    """A class to represent a command. The command is run with `exec`."""
    @abstractmethod
    def exec() -> None:
        pass


class GenerateDatabaseCmd(Cmd):
    """
    Create and populate a local SQL database with crash data fetched from
    PennDOT's website.
    """
    def exec(self):
        self._init_folders()
        self._cache_files()
        self._unzip_data()
        self._load_data_into_db()
        self._print_table_names()

    def _init_folders(self):
        DATABASE_ROOT.mkdir(exist_ok=True)
        DATABASE_FILE.unlink(missing_ok=True)
        DATABASE_CACHE.mkdir(exist_ok=True)

    def _cache_files(self) -> None:
        for year in range(2003, 2023):
            filename = f"Philadelphia_{year}.zip"
            self._cache_file(filename)

    def _cache_file(self, filename: str):
        # If we have the file already, do nothing.
        cached_file = DATABASE_CACHE / filename
        if cached_file.exists():
            print(f"Already cached: {cached_file.name}")
            return
        
        # Otherwise, download the file to the cache.
        url = f"https://gis.penndot.gov/gishub/crashZip/County/Philadelphia/{filename}"
        print(f"Attempting download from {url=} to {cached_file=} ... ", end='')
        r = requests.get(url)
        print(f"{r.status_code} {responses[r.status_code]}")
        assert r.status_code == HTTPStatus.OK, f"{r.status_code=}"
        open(cached_file, 'wb').write(r.content)

    def _unzip_data(self):
        for path in DATABASE_CACHE.iterdir():
            if path.suffix != ".zip":
                continue
            with zipfile.ZipFile(path) as zip:
                zip.extractall(path=DATABASE_ROOT)

    def _load_data_into_db(self):
        with sqlite3.connect(DATABASE_FILE) as conn:
            for csvfile in DATABASE_ROOT.iterdir():
                if csvfile.suffix != ".csv":
                    continue
                print(f"Loading {csvfile} into db...")
                table, _ = self._parse_info_from_csv_name(csvfile)
                df = pandas.read_csv(csvfile)
                df.to_sql(table, conn, if_exists='append', index=False)
                csvfile.unlink()

    def _parse_info_from_csv_name(self, csvfile: Path):
        """Expected format: '<TABLE>_<COUNTY>_<YEAR>.csv'."""
        tokens = csvfile.stem.split("_")
        assert len(tokens) == 3, f"{tokens=}"
        table, year = tokens[0], int(tokens[2])
        return table, year

    def _print_table_names(self):
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            print(cursor.fetchall())


GenerateDatabaseCmd().exec()
