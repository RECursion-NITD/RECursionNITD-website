from django.db import models


class Level(models.Model):
    Number = models.PositiveIntegerField(primary_key=True, default='')
    Color = models.CharField(max_length=200, default='')
    Image = models.ImageField(blank=True)
    Level_title = models.CharField(max_length=200, default='')

    def __int__(self):
        return self.Number


class Topic(models.Model):
    Topic_title = models.CharField(max_length=200, default='', blank=True)
    level = models.ForeignKey('Level', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.Topic_title


class SubTopic(models.Model):
    sub_topic = models.CharField(max_length=200, blank=True)
    topic = models.ForeignKey('Topic', null=True, on_delete=models.CASCADE)
    level = models.ForeignKey('Level', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_topic


class Note(models.Model):
    Notes_topic = models.CharField(max_length=200, default='', blank=True)
    Description = models.TextField(blank=True)
    Code_snippet = models.TextField(blank=True)
    Image1 = models.ImageField(blank=True)
    Image2 = models.ImageField(blank=True)
    topic = models.ForeignKey('Topic', null=True, on_delete=models.CASCADE)
    level = models.ForeignKey('Level', null=True, on_delete=models.CASCADE)
    subtopic = models.ForeignKey('SubTopic', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.Notes_topic


class File(models.Model):
    heading = models.CharField(max_length=200, default='', blank=True)
    upload = models.FileField(blank=True)
    topic = models.ForeignKey('Topic', null=True, on_delete=models.CASCADE)
    level = models.ForeignKey('Level', null=True, on_delete=models.CASCADE)
    subtopic = models.ForeignKey('SubTopic', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.heading

class Link(models.Model):
    link1 = models.CharField(max_length=200, default='', blank=True)
    url_link1 = models.URLField(blank=True)
    link2 = models.CharField(max_length=200, default='', blank=True)
    url_link2 = models.URLField(blank=True)
    link3 = models.CharField(max_length=200, default='', blank=True)
    url_link3 = models.URLField(blank=True)
    link4 = models.CharField(max_length=200, default='', blank=True)
    url_link4 = models.URLField(blank=True)
    file = models.ForeignKey('File', null=True, on_delete=models.CASCADE)