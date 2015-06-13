from django.db import models


class Container(models.Model):
    """Represents a local or remote journal volume and issue."""
    volume = models.IntegerField()
    issue = models.IntegerField()
    date = models.DateField()
    url = models.URLField(blank=True)
    title = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        if self.title != '':
            return self.title

        if self.url != '':
            return self.url
        else:
            return str(self.volume) + '(' + str(self.issue) + ')'


class Article(models.Model):
    """Represents an article in an overlay journal."""
    title = models.CharField(max_length=500)

    # Local attributes: a date when the article was added and the volume/issue it should appear in.
    local_container = models.ForeignKey(Container, related_name='local_container')

    # Remote attributes: the remote journal, issue and volume.
    remote_container = models.OneToOneField(Container, related_name='remote_container')

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-id']

    def get_authors(self):
        authors = self.author_set.all()

        author_list = ''

        last = len(authors) - 1

        for i, author in enumerate(authors):
            if i == 0:
                author_list += author.family
            elif i == last:
                author_list += ' and {0}'.format(author.family)
            else:
                author_list += ', {0}'.format(author.family)

        return author_list


class Author(models.Model):
    """Represents an author of an article."""
    given = models.CharField(max_length=500)
    family = models.CharField(max_length=500)
    article = models.ForeignKey(Article)

    def __unicode__(self):
        return self.given + ' ' + self.family