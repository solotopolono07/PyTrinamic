from pytrinamic.connections.tmcl_interface import TmclInterface


class DummyTmclInterface(TmclInterface):

    def __init__(self, port, datarate=115200, host_id=2, module_id=1, debug=True):
        """
        Opens a dummy TMCL connection
        """
        if not isinstance(port, str):
            raise TypeError

        TmclInterface.__init__(self, host_id, module_id, debug)

        if self._debug:
            print("Opened dummy TMCL interface on port '" + port + "'")
            print("\tData rate:  " + str(datarate))
            print("\tHost ID:    " + str(host_id))
            print("\tModule ID:  " + str(module_id))

    def __enter__(self):
        return self

    def __exit__(self, exit_type, value, traceback):
        """
        Close the connection at the end of a with-statement block.
        """
        del exit_type, value, traceback
        self.close()

    def close(self):
        """
        Closes the dummy TMCL connection
        """
        if self._debug:
            print("Closed dummy TMCL interface")

    def _send(self, host_id, module_id, data):
        """
            Send the bytearray parameter [data].

            This is a required override function for using the tmcl_interface
            class.
        """
        del host_id, module_id, data
        pass

    def _recv(self, host_id, module_id):
        """
            Read 9 bytes and return them as a bytearray.

            This is a required override function for using the tmcl_interface
            class.
        """
        del host_id, module_id

        return bytearray(9)

    @staticmethod
    def supports_tmcl():
        return True

    def print_info(self):
        print("Connection: type=dummy_tmcl_interface")

    @staticmethod
    def list():
        """
            Return a list of available connection ports as a list of strings.

            This function is required for using this interface with the
            connection manager.
        """
        return ["dummy"]


if __name__ == "__main__":
    interface = DummyTmclInterface("dummy")

    interface.get_version_string()
    interface.send_boot()
    interface.close()
