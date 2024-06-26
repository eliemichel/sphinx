import os
import sys
from pathlib import Path

import docutils
import pytest

import sphinx
import sphinx.locale
import sphinx.pycode
from sphinx.testing.util import _clean_up_global_state


def _init_console(locale_dir=sphinx.locale._LOCALE_DIR, catalog='sphinx'):
    """Monkeypatch ``init_console`` to skip its action.

    Some tests rely on warning messages in English. We don't want
    CLI tests to bleed over those tests and make their warnings
    translated.
    """
    return sphinx.locale.NullTranslations(), False


sphinx.locale.init_console = _init_console

pytest_plugins = 'sphinx.testing.fixtures'

# Exclude 'roots' dirs for pytest test collector
collect_ignore = ['roots']

os.environ['SPHINX_AUTODOC_RELOAD_MODULES'] = '1'


@pytest.fixture(scope='session')
def rootdir():
    return Path(__file__).parent.resolve() / 'roots'


def pytest_report_header(config):
    header = f"libraries: Sphinx-{sphinx.__display_version__}, docutils-{docutils.__version__}"
    if hasattr(config, '_tmp_path_factory'):
        header += f"\nbase tmp_path: {config._tmp_path_factory.getbasetemp()}"
    return header


@pytest.fixture(autouse=True)
def _cleanup_docutils():
    saved_path = sys.path
    yield  # run the test
    sys.path[:] = saved_path

    _clean_up_global_state()
