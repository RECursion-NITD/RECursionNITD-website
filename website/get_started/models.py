from django.db import models


class Level(models.Model):
    Number = models.PositiveIntegerField(primary_key=True)
    Level_title = models.CharField(max_length=200, default='')

    def __int__(self):
        return self.Number


class Topic(models.Model):
    Topic_title = models.CharField(max_length=200, default='')
    level = models.ForeignKey('Level', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.Topic_title


class Link(models.Model):
    sub_topic = models.CharField(max_length=200)
    url_topic = models.URLField()
    topic = models.ForeignKey('Topic', null=True, on_delete=models.CASCADE)
    level = models.ForeignKey('Level', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_topic


class Note(models.Model):
    Notes_topic = models.CharField(max_length=200, default='')
    Description = models.TextField()
    Image = models.ImageField()
    topic = models.ForeignKey('Topic', null=True, on_delete=models.CASCADE)
    level = models.ForeignKey('Level', null=True, on_delete=models.CASCADE)
    link = models.ForeignKey('link', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.Notes_topic


class File(models.Model):
    heading = models.CharField(max_length=200, default='')
    image = models.ImageField()
    upload = models.FileField()
    topic = models.ForeignKey('Topic', null=True, on_delete=models.CASCADE)
    level = models.ForeignKey('Level', null=True, on_delete=models.CASCADE)
    link = models.ForeignKey('link', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.heading
