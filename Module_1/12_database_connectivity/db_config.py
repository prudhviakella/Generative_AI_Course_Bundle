# db_config.py
from dataclasses import dataclass
import configparser
from typing import Dict

@dataclass
class DBConfig:
    host: str
    port: int
    dbname: str
    user: str
    password: str
    schema: str = "public"

def load_db_config(config_path: str = "config.ini", section: str = "postgres", app_section: str = "app") -> DBConfig:
    """
    Load DB config from config.ini. Raises KeyError if required keys missing.
    """
    cp = configparser.ConfigParser()
    read = cp.read(config_path)
    if not read:
        raise FileNotFoundError(f"Config file '{config_path}' not found.")

    if section not in cp:
        raise KeyError(f"Section '{section}' not found in config file.")

    pg = cp[section]
    app_cfg = cp[app_section] if app_section in cp else {}

    host = pg.get("host", "localhost")
    port = int(pg.get("port", 5432))
    dbname = pg.get("dbname", "")
    user = pg.get("user", "")
    password = pg.get("password", "")

    schema = app_cfg.get("schema", "public")

    return DBConfig(host=host, port=port, dbname=dbname, user=user, password=password, schema=schema)