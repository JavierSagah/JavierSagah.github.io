# import unittest
from django.test import TestCase
from Poker_app.CommandHandler import CommandHandler, menu
from Poker_app.models import Account


class PlayerTestCase(TestCase):

    r1 = "Command not recognized. Try username: command args(if needed)."

    def setUp(self):
        # self.admin = Account.objects.create(username="admin", role="admin")
        self.player = Account.objects.create(username="player1", role="player")
        self.app = CommandHandler()

    # def test_player_provides_username_success(self):
    #     self.assertEqual(self.app.command("", "player1"), "player1 is allowed to give a command. Please use the command line.")

    def test_player_provides_nonexistent_username(self):
        self.assertEqual(self.app.command("", "poker_star1"), "Username poker_star1 does not exist or is invalid. Try again.")

    def test_player_command_success(self):
        self.assertEqual(self.app.command("player1: quit", "player1"), "You have left the game, Bye.")

    # this is same as player provides valid username
    def test_player_no_command(self):
        self.assertEqual(self.app.command("", "player1"), menu("player1"))

    def test_player_bad_command(self):
        self.assertEqual(self.app.command("sdfsdf", "player1"), self.r1)
        self.assertEqual(self.app.command(" ", "player1"), self.r1)
        self.assertEqual(self.app.command("player1", "player1"), self.r1)
        self.assertEqual(self.app.command("player1:", "player1"), self.r1)
        self.assertEqual(self.app.command("player1 quit", "player1"), self.r1)
        self.assertEqual(self.app.command("player1quit", "player1"), self.r1)
        self.assertEqual(self.app.command("player1:quit", "player1"), self.r1)
        self.assertEqual(self.app.command("player1: quitgame", "player1"), self.r1)

    def test_player_pretend_admin(self):
        self.assertEqual(self.app.command("admin: quit", "admin"), "admin username not allowed for players.")
        self.assertEqual(self.app.command("admin: quit", "player1"), "You are not the admin.")




