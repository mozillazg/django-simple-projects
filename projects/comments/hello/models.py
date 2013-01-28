from django.db import models


class Topic(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    @models.permalink
    def get_absolute_url(self):
        return ('display_topic', (), {'topic_id': self.id})

    def __unicode__(self):
        return self.title
