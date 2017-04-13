from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class SelectionGroup(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        ordering = ['name']

class Selector(models.Model):
    account = models.OneToOneField(User)
    selection_groups = models.ManyToManyField(SelectionGroup)

    def suggestions(self):
        return '%s' % (self.suggestion_set.count())

    def suggestions_yes(self):
        return '%s' % (self.suggestion_set.filter(suggestion_type=Suggestion.YES).count())

    def suggestions_maybe(self):
        return '%s' % (self.suggestion_set.filter(suggestion_type=Suggestion.MAYBE).count())

    def suggestions_no(self):
        return '%s' % (self.suggestion_set.filter(suggestion_type=Suggestion.NO).count())

    def __str__(self):
        return '%s' % (self.account.first_name + ' ' + self.account.last_name)

    class Meta:
        ordering = ['account']

class Suggestion(models.Model):
    YES = '0'    
    MAYBE = '1'
    NO = '2'
    SUGGESTION_TYPE_CHOICES = (
        (YES, 'Yes'),        
        (MAYBE, 'Maybe'),
        (NO, 'No'),
    )
    
    name = models.CharField(max_length=50, blank=False)
    suggestion_type = models.CharField(
        max_length=1,
        choices=SUGGESTION_TYPE_CHOICES,
        default=YES,
        blank=False,
    )
    created = models.DateTimeField(auto_now_add=True)
    last_checked = models.DateTimeField(auto_now=True)
    selector = models.ForeignKey(Selector, blank=False)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        ordering = ['name']
