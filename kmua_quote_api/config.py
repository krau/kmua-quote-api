from pathlib import Path

from dynaconf import Dynaconf

_BASE_DIR = Path(__file__).resolve().parent.parent

settings = Dynaconf(
    envvar_prefix="KMUA_QUOTE_API",
    settings_files=["config.toml"],
    base_dir=_BASE_DIR,
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
