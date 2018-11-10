"""Test QtConsoleApp"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import os
import shutil
import sys
import tempfile
from subprocess import check_output

from traitlets.tests.utils import check_help_all_output
import pytest

from . import no_display


@pytest.mark.skipif(no_display, reason="Doesn't work without a display")
def test_help_output():
    """jupyter qtconsole --help-all works"""
    check_help_all_output('qtconsole')


@pytest.mark.skipif(no_display, reason="Doesn't work without a display")
@pytest.mark.skipif(os.environ.get('CI', None) is None,
                    reason="Doesn't work outside of our CIs")
def test_generate_config():
    """jupyter qtconsole --generate-config"""
    td = tempfile.mkdtemp()
    try:
        check_output([sys.executable, '-m', 'qtconsole', '--generate-config'],
            env={'JUPYTER_CONFIG_DIR': td},
        )
        assert os.path.isfile(os.path.join(td, 'jupyter_qtconsole_config.py'))
    finally:
        shutil.rmtree(td)
