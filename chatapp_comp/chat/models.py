from django.db import models


# テーブルを作成
class Message(models.Model):
    contents = models.CharField(max_length=80)
    response = models.TextField()
    created_at = models.DateTimeField()

    # モデルを表すものとして、contents（書き込み内容）を使う
    def __str__(self):
        return self.contents


class Answer(models.Model):
    departure = models.CharField(max_length=80)
    destination = models.CharField(max_length=80)
    stay = models.CharField(max_length=80)
    created_at = models.DateTimeField()

    def __str__(self):
        return str(self.created_at)
