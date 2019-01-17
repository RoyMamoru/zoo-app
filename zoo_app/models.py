from django.db import models

class ZooCollection(models.Model):
    # ログインUserの情報を保存するDB
    user_id = models.IntegerField(default=0)
    animal_id = models.IntegerField(default=0)

    def __str__(self):
        return '%d, %d' % (self.user_id, self.animal_id)

class AnimalInfo(models.Model):
    # 動物の情報を保存するDB
    id = models.AutoField(primary_key=True)
    animal_id = models.IntegerField(default=0)
    animal_name = models.CharField(max_length=50, default='')
    animal_title = models.CharField(max_length=300, default='')
    animal_disc = models.TextField(default='')

    def __str__(self):
        return '%d, %s, %s, %s' % (self.animal_id, self.animal_name, self.animal_title, self.animal_disc)
