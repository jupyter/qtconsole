import sys

import pytest

from qtconsole.qtconsoleapp import JupyterQtConsoleApp


def test_shortcut_traitlets():
    """ Verify that the traitlets are initialized correctly.
    """
    # Simulate startup
    test_args = ["test", ""]
    app = JupyterQtConsoleApp()
    app.initialize(test_args)
    app.window.confirm_exit = False

    # Check if the shortcuts traitlet has the expected value
    assert app.shortcut_full_screen == ("Ctrl+Meta+F" if sys.platform == 'darwin' else "F11")
    assert app.shortcut_copy == "Ctrl+C"
    assert app.shortcut_paste == "Ctrl+V"
    assert app.shortcut_cut == "Ctrl+X"
    assert app.shortcut_clear == "Ctrl+L"
    assert app.shortcut_new_kernel_tab == "Ctrl+T"
    assert app.shortcut_slave_kernel_tab == "Ctrl+Shift+T"
    assert app.shortcut_existing_kernel_tab == "Alt+T"
    assert app.shortcut_save == "Ctrl+S"
    assert app.shortcut_print == "Ctrl+P"
    assert app.shortcut_undo == "Ctrl+Z"
    assert app.shortcut_redo == ("Ctrl+Y" if sys.platform.startswith('win') else "Ctrl+Shift+Z")
    assert app.shortcut_copy_raw == "Ctrl+Shift+C"
    assert app.shortcut_select_all == "Ctrl+A"
    assert app.shortcut_ctrl_shift_m == "Ctrl+Shift+M"
    assert app.shortcut_zoom_in == "Ctrl++"
    assert app.shortcut_zoom_out == "Ctrl+-"
    assert app.shortcut_reset_font_size == "Ctrl+0"
    assert app.shortcut_interrupt_kernel == ("Meta+C" if sys.platform == 'darwin' else "Ctrl+C")
    assert app.shortcut_restart_kernel == ("Meta+." if sys.platform == 'darwin' else "Ctrl+.")
    assert app.shortcut_minimize == "Ctrl+M"
    assert app.shortcut_prev_tab == ("Ctrl+Alt+Left" if sys.platform == 'darwin' else "Ctrl+PgUp")
    assert app.shortcut_next_tab == ("Ctrl+Alt+Right" if sys.platform == 'darwin' else "Ctrl+PgDown")
    assert app.shortcut_rename_window == "Alt+R"
    assert app.shortcut_rename_current_tab == "Ctrl+R"
    assert app.shortcut_close == ("Ctrl+F4" if sys.platform.startswith('win') else "Ctrl+W")
    app.window.close()


@pytest.mark.parametrize(
    "shortcut",
    ["undo", "redo", "copy", "cut", "paste", "print", "clear", "close"]
)
def test_custom_shortcut_manager(shortcut):
    """ Verify that the shortcuts traitlets are set with a custom value.
    """
    # Simulate startup with a command-line argument that changes shortcuts
    test_args = ["test", f"--JupyterQtConsoleApp.shortcut_{shortcut}=Ctrl+O"]

    # Initialize the application with the simulated arguments
    app = JupyterQtConsoleApp()
    app.initialize(test_args)
    window = app.window
    window.confirm_exit = False

    # Check if the shortcut traitlet has the expected value
    assert getattr(app, f"shortcut_{shortcut}") == "Ctrl+O"
    assert getattr(window, f"{shortcut}_action").shortcut().toString() == "Ctrl+O"
    window.close()
