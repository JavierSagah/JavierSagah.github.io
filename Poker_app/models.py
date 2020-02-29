from django.db import models


# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=10)
    role = models.CharField(max_length=6)
    in_game = models.BooleanField(default=False)
    total_balance = models.IntegerField(default=0)
    in_game_chips = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    # One table game can have many players, but a player can only be in one table at a time
    # the field is one to the model and the model is many to the field
    table = models.ForeignKey('Game', on_delete=models.CASCADE, blank=True, null=True)
    # to access the reversed relationship we use:
    # all_players_in_table = Account.objects.filter(table=thetable)
    # or
    # all_players_in_table = thetable.account_set
    # both will return a query set of all the players in thetable

    def __str__(self):
        status = "in a game" if self.in_game else "in the lobby"
        table = str(self.table.table_id) if self.table else "-"
        return "Username: " + self.username + " Role: " + self.role + " Status: " + status + " Balance: "\
               + str(self.total_balance) + " Highest score: " + str(self.score) + " Table: " + table


class Game(models.Model):
    table_id = models.IntegerField(default=0)
    game_on = models.BooleanField(default=False)
    num_players = models.IntegerField(default=0)

    def __str__(self):
        return "Table: " + str(self.table_id) + " ---------- players waiting: " + str(self.num_players)