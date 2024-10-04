import unittest
from unittest.mock import patch
from uart_communicate import UARTCommunication


class TestUARTCommunication(unittest.TestCase):

    @patch('serial.Serial')
    def test_open_port_success(self, mock_serial):
        uart = UARTCommunication()
        mock_serial.return_value.is_open = True
        status = uart.open_port("COM3")
        self.assertEqual(status, "Connected to COM3")
        self.assertIsNotNone(uart.ser)

    @patch('serial.Serial')
    def test_open_port_fail(self, mock_serial):
        uart = UARTCommunication()
        mock_serial.side_effect = Exception("Cannot open port")
        status = uart.open_port("COM3")
        self.assertEqual(status, "Error: Cannot open port")
        self.assertIsNone(uart.ser)

    @patch('serial.Serial')
    def test_send_message_success(self, mock_serial):
        uart = UARTCommunication()
        mock_serial.return_value.is_open = True
        uart.ser = mock_serial()
        status = uart.send_message("Hello")
        self.assertEqual(status, "Sent: Hello")
        uart.ser.write.assert_called_with(b"Hello\n")

    @patch('serial.Serial')
    def test_send_message_fail(self, mock_serial):
        uart = UARTCommunication()
        uart.ser = None
        status = uart.send_message("Hello")
        self.assertEqual(status, "Port not opened")

    @patch('serial.Serial')
    def test_receive_message_success(self, mock_serial):
        uart = UARTCommunication()
        mock_serial.return_value.is_open = True
        uart.ser = mock_serial()
        uart.ser.readline.return_value = b"Received data\n"
        response = uart.receive_message()
        self.assertEqual(response, "Received data")

    @patch('serial.Serial')
    def test_receive_message_fail(self, mock_serial):
        uart = UARTCommunication()
        uart.ser = None
        response = uart.receive_message()
        self.assertEqual(response, "Port not opened")


if __name__ == '__main__':
    unittest.main()
