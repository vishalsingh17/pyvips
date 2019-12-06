from __future__ import division

import logging

import pyvips
from pyvips import vips_lib

logger = logging.getLogger(__name__)


class Streamou(pyvips.Streamo):
    """An output stream you can connect action signals to to implement
    behaviour.

    """

    def __init__(self):
        """Make a new stream from a file descriptor (a small integer).

        You can pass this stream to (for example) :meth:`write_to_stream`.

        """

        super(Streamou, self).__init__(vips_lib.vips_streamou_new())

    def on_write(self, handler):
        """Attach a write handler.

        The interface is exactly as io.write(). The handler is given a
        bytes-like object to write, and should return the number of bytes
        written.

        """

        def interface_handler(buf):
            bytes_written = handler(buf)
            # py2 will often return None for bytes_written ... replace with
            # the length of the string
            if bytes_written is None:
                bytes_written = len(buf)

            return bytes_written

        self.signal_connect("write", interface_handler)

    def on_finish(self, handler):
        """Attach a finish handler.

        This optional handler is called at the end of write. It should do any
        cleaning up necessary.

        """

        self.signal_connect("finish", handler)


__all__ = ['Streamou']
