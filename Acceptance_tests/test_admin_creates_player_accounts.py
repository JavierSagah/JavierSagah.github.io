# import unittest
from django.test import TestCase
from Poker_app.CommandHandler import CommandHandler, menu
from Poker_app.models import Account


class AdminCreatesPlayerAccount(TestCase):

    def setUp(self):
        # the command handler receives 2 arguments: the command from the command input textbox
        # and the username form the username input textbox
        self.admin = Account.objects.create(username="admin", role="admin")
        self.player = Account.objects.create(username="player2", role="player")
        self.app = CommandHandler()

    def test_admin_creates_player_acc_success(self):
        self.assertEqual(self.app.command("admin: create account player1", "admin"), "Player account player1 successfully created.")
        self.assertEqual("player1", Account.objects.get(username="player1").username)

    def test_admin_creates_player_acc_duplicate(self):
        self.assertEqual(self.app.command("admin: create account player2", "admin"), "Player account player2 already exists.")

    def test_valid_admin_username_no_command(self):
        self.assertEqual(self.app.command("", "admin"), menu("admin"))

    def test_valid_admin_username_bad_command(self):
        self.assertEqual(self.app.command("asdsd", "admin"), "Command not recognized. Try <username>: <supported command>.")