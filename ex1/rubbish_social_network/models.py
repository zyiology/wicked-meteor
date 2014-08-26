from django.db import models
from django.contrib.auth.models import User
  
# Create your models here.
class UserLink(models.Model):
  class Meta:
    unique_together = ("from_user", "to_user")
  from_user = models.ForeignKey(User, related_name = "from_user")
  to_user = models.ForeignKey(User, related_name = "to_user")
  date_added = models.DateField()
  
  def save(self, *args, **kwargs):
    if self.from_user == self.to_user:
      return
    else:
      super(UserLink, self).save(*args,**kwargs)
  
  def __unicode__(self):
    return self.from_user.username + " is following " + self.to_user.username

