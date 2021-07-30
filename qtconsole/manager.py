""" Defines a KernelClient that provides signals and slots.
"""

from qtpy import QtCore

# Local imports
from traitlets import Bool, DottedObjectName

import jupyter_client
from jupyter_client import KernelManager
from jupyter_client.restarter import KernelRestarter

from .kernel_mixins import QtKernelManagerMixin, QtKernelRestarterMixin


class QtKernelRestarter(KernelRestarter, QtKernelRestarterMixin):

    def start(self):
        if self._timer is None:
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(self.poll)
        self._timer.start(round(self.time_to_dead * 1000))

    def stop(self):
        self._timer.stop()

    def poll(self):
        super().poll()


def _post_start_kernel():
    # KernelManager.post_start_kernel is async in jupyter_client>=7.0
    if int(jupyter_client.__version__.split(".")[0]) >= 7:
        async def post_start_kernel(self, **kw):
            """Kernel restarted."""
            await super(QtKernelManager, self).post_start_kernel(**kw)
            if self._is_restarting:
                self.kernel_restarted.emit()
                self._is_restarting = False
    else:
        def post_start_kernel(self, **kw):
            """Kernel restarted."""
            super(QtKernelManager, self).post_start_kernel(**kw)
            if self._is_restarting:
                self.kernel_restarted.emit()
                self._is_restarting = False
    return post_start_kernel


class QtKernelManager(KernelManager, QtKernelManagerMixin):
    """A KernelManager with Qt signals for restart"""

    client_class = DottedObjectName('qtconsole.client.QtKernelClient')
    autorestart = Bool(True, config=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_restarting = False

    def start_restarter(self):
        """Start restarter mechanism."""
        if self.autorestart and self.has_kernel:
            if self._restarter is None:
                self._restarter = QtKernelRestarter(
                    kernel_manager=self,
                    parent=self,
                    log=self.log,
                )
                self._restarter.add_callback(self._handle_kernel_restarting)
            self._restarter.start()

    def stop_restarter(self):
        """Stop restarter mechanism."""
        if self.autorestart:
            if self._restarter is not None:
                self._restarter.stop()

    post_start_kernel = _post_start_kernel()

    def _handle_kernel_restarting(self):
        """Kernel has died, and will be restarted."""
        self._is_restarting = True
