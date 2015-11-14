"""
An example of opening up an RichJupyterWidget in a PyQT Application, this can
execute either stand-alone or by importing this file and calling
inprocess_qtconsole.show().

Based on the earlier example in the IPython repository, this has
been updated to use qtconsole.
"""


from qtconsole.qt import QtGui
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.inprocess import QtInProcessKernelManager


def show():
    global ipython_widget  # Prevent from being garbage collected

    # Create an in-process kernel
    kernel_manager = QtInProcessKernelManager()
    kernel_manager.start_kernel(show_banner=False)
    kernel = kernel_manager.kernel
    kernel.gui = 'qt4'

    kernel_client = kernel_manager.client()
    kernel_client.start_channels()

    ipython_widget = RichJupyterWidget()
    ipython_widget.kernel_manager = kernel_manager
    ipython_widget.kernel_client = kernel_client
    ipython_widget.show()


if __name__ == "__main__":
    app = QtGui.QApplication([])
    show()
    app.exec_()
