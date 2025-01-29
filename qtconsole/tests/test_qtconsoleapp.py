import sys

import pytest

from qtconsole.qtconsoleapp import JupyterQtConsoleApp


@pytest.fixture
def qtconsole_with_argv(qtbot):
    """Qtconsole fixture with argv support."""
    console = JupyterQtConsoleApp()

    def _qtconsole(argv=[]):
        # Create a console
        console.initialize(argv=argv)
        console.window.confirm_exit = False

        return console

    yield _qtconsole

    console.window.close()


def test_shortcut_traitlets(qtconsole_with_argv):
    """ Verify that the traitlets are initialized correctly.
    """
    # Simulate startup
    test_args = ["test", ""]
    console = qtconsole_with_argv(test_args)

    # Check if the shortcuts traitlet has the expected value
    assert console.shortcut_full_screen == ("Ctrl+Meta+F" if sys.platform == 'darwin' else "F11")
    assert console.shortcut_copy == "Ctrl+C"
    assert console.shortcut_paste == "Ctrl+V"
    assert console.shortcut_cut == "Ctrl+X"
    assert console.shortcut_clear == "Ctrl+L"
    assert console.shortcut_new_kernel_tab == "Ctrl+T"
    assert console.shortcut_slave_kernel_tab == "Ctrl+Shift+T"
    assert console.shortcut_existing_kernel_tab == "Alt+T"
    assert console.shortcut_save == "Ctrl+S"
    assert console.shortcut_print == "Ctrl+P"
    assert console.shortcut_undo == "Ctrl+Z"
    assert console.shortcut_redo == ("Ctrl+Y" if sys.platform.startswith('win') else "Ctrl+Shift+Z")
    assert console.shortcut_copy_raw == "Ctrl+Shift+C"
    assert console.shortcut_select_all == "Ctrl+A"
    assert console.shortcut_ctrl_shift_m == "Ctrl+Shift+M"
    assert console.shortcut_zoom_in == "Ctrl++"
    assert console.shortcut_zoom_out == "Ctrl+-"
    assert console.shortcut_reset_font_size == "Ctrl+0"
    assert console.shortcut_interrupt_kernel == ("Meta+C" if sys.platform == 'darwin' else "Ctrl+C")
    assert console.shortcut_restart_kernel == ("Meta+." if sys.platform == 'darwin' else "Ctrl+.")
    assert console.shortcut_minimize == "Ctrl+M"
    assert console.shortcut_prev_tab == ("Ctrl+Alt+Left" if sys.platform == 'darwin' else "Ctrl+PgUp")
    assert console.shortcut_next_tab == ("Ctrl+Alt+Right" if sys.platform == 'darwin' else "Ctrl+PgDown")
    assert console.shortcut_rename_window == "Alt+R"
    assert console.shortcut_rename_current_tab == "Ctrl+R"
    assert console.shortcut_close == ("Ctrl+F4" if sys.platform.startswith('win') else "Ctrl+W")


@pytest.mark.parametrize(
    "shortcut",
    ["undo", "redo", "copy", "cut", "paste", "print", "clear", "close"]
)
def test_custom_shortcut_manager(qtconsole_with_argv, shortcut):
    """ Verify that the shortcuts traitlets are set with a custom value.
    """
    # Simulate startup with a command-line argument that changes shortcuts
    test_args = ["test", f"--JupyterQtConsoleApp.shortcut_{shortcut}=Ctrl+O"]

    # Initialize the application with the simulated arguments
    console = qtconsole_with_argv(test_args)
    window = console.window

    # Check if the shortcut traitlet has the expected value
    assert getattr(console, f"shortcut_{shortcut}") == "Ctrl+O"
    assert getattr(window, f"{shortcut}_action").shortcut().toString() == "Ctrl+O"
