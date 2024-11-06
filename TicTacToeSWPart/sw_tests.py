import unittest
from unittest.mock import MagicMock, patch
from tkinter import Tk
from io import StringIO
from main import UARTCommunication, update_game_board, send_move, set_mode, reset_game, auto_receive
import tkinter as tk


class TestUARTCommunication(unittest.TestCase):
    def setUp(self):
        self.uart = UARTCommunication()

    @patch('serial.tools.list_ports.comports')
    def test_list_ports(self, mock_comports):
        mock_comports.return_value = [MagicMock(device="COM3"), MagicMock(device="COM4")]
        ports = self.uart.list_ports()
        self.assertEqual(ports, ["COM3", "COM4"])

    @patch('serial.Serial')
    def test_open_port_success(self, mock_serial):
        mock_serial.return_value = MagicMock(is_open=True)
        status = self.uart.open_port("COM3")
        self.assertEqual(status, "Connected to COM3")
        self.assertTrue(self.uart.ser.is_open)

    @patch('serial.Serial')
    def test_open_port_failure(self, mock_serial):
        mock_serial.side_effect = Exception("Port error")
        status = self.uart.open_port("COM5")
        self.assertEqual(status, "Error: Port error")
        self.assertIsNone(self.uart.ser)

    @patch('serial.Serial')
    def test_send_message_success(self, mock_serial):
        mock_serial.return_value = MagicMock(is_open=True)
        self.uart.ser = mock_serial()
        result = self.uart.send_message({"command": "MOVE", "row": 0, "col": 1})
        self.assertIn("Sent:", result)

    @patch('serial.Serial')
    def test_send_message_failure(self, mock_serial):
        mock_serial.return_value = MagicMock(is_open=False)
        self.uart.ser = mock_serial()
        result = self.uart.send_message({"command": "MOVE", "row": 0, "col": 1})
        self.assertEqual(result, "Port not opened")

    @patch('serial.Serial')
    def test_receive_message_success(self, mock_serial):
        mock_serial.return_value = MagicMock(is_open=True, in_waiting=1)
        mock_serial().readline.return_value = b'{"command": "MOVE", "row": 0, "col": 1}\n'
        self.uart.ser = mock_serial()
        message = self.uart.receive_message()
        self.assertEqual(message, {"command": "MOVE", "row": 0, "col": 1})

    @patch('serial.Serial')
    def test_receive_message_invalid_json(self, mock_serial):
        mock_serial.return_value = MagicMock(is_open=True, in_waiting=1)
        mock_serial().readline.return_value = b'{"command": "MOVE", "row": 0, "col": }\n'
        self.uart.ser = mock_serial()
        message = self.uart.receive_message()
        self.assertEqual(message, "Error: Invalid JSON received")

    @patch('serial.Serial')
    def test_receive_message_no_data(self, mock_serial):
        mock_serial.return_value = MagicMock(is_open=True, in_waiting=0)
        self.uart.ser = mock_serial()
        message = self.uart.receive_message()
        self.assertEqual(message, "Port not opened")


class TestGameFunctions(unittest.TestCase):
    def test_update_game_board(self):
        root = Tk()
        buttons = [[tk.Button(root, text=" ") for _ in range(3)] for _ in range(3)]
        board = [["X", "O", "X"], ["O", "X", "O"], ["X", "O", "X"]]
        update_game_board(board, buttons)
        for i in range(3):
            for j in range(3):
                self.assertEqual(buttons[i][j]["text"], board[i][j])
        root.destroy()

    @patch.object(UARTCommunication, 'send_message')
    def test_send_move(self, mock_send_message):
        uart = UARTCommunication()
        send_move(uart, 1, 1)
        mock_send_message.assert_called_with({"command": "MOVE", "row": 1, "col": 1})

    @patch.object(UARTCommunication, 'send_message')
    def test_set_mode(self, mock_send_message):
        uart = UARTCommunication()
        set_mode(uart, 1)
        mock_send_message.assert_called_with({"command": "MODE", "mode": 1})

    @patch.object(UARTCommunication, 'send_message')
    def test_reset_game(self, mock_send_message):
        uart = UARTCommunication()
        reset_game(uart)
        mock_send_message.assert_called_with({"command": "RESET"})


if __name__ == '__main__':
    unittest.main()
