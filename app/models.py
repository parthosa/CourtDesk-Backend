"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Permission(models.Model):
    name = models.CharField(max_length=20,primary_key=True)
    view_peshi = models.BooleanField(default=False)
    edit_peshi = models.BooleanField(default=False)
    edit_casefile = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    name = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class LR(UserProfile):
    permissions = models.ForeignKey(Permission,on_delete=models.CASCADE,default="LR")

class Restorer(UserProfile):
    permissions = models.ForeignKey(Permission,on_delete=models.CASCADE,default="LR")

class Steno(UserProfile):
    permissions = models.ForeignKey(Permission,on_delete=models.CASCADE,default="LR")

class CourtStaff(UserProfile):
    permissions = models.ForeignKey(Permission,on_delete=models.CASCADE,default="CS")

class Judge(UserProfile):
    permissions = models.ForeignKey(Permission,on_delete=models.CASCADE,default="JUDGE")
    lr = models.ManyToManyField(LR)
    court_staff = models.ManyToManyField(CourtStaff)
    restorer = models.ManyToManyField(Restorer)
    steno = models.ManyToManyField(Steno)

class Court(models.Model):
    name = models.CharField(max_length=15,primary_key=True)

    def __str__(self):
        return self.name


class CourtRoom(models.Model):
    number = models.IntegerField(default=0)
    court = models.ForeignKey(Court,on_delete=models.CASCADE)
    roster = models.CharField(max_length=20, null = True)
    judges = models.ManyToManyField(Judge)

    def __str__(self):
        return self.court.name + "-" + str(self.number)

class CaseLaw(models.Model):
    name = models.CharField(max_length=20)
    file = models.FileField(upload_to='files/caselaws/',null = True)

    def __str__(self):
        return self.name

class Legislature(models.Model):  
    name = models.CharField(max_length=20)
    file = models.FileField(upload_to='files/legislatures/',null = True)

    def __str__(self):
        return self.name
   

class CaseFile(models.Model):
    case_number = models.CharField(max_length=20)
    court_room = models.ForeignKey(CourtRoom,on_delete = models.CASCADE)
    next_date_of_hearing = models.DateField()
    last_date_of_hearing = models.DateField()

    file = models.FileField(upload_to='files/casefiles/',null = True)

    case_laws = models.ManyToManyField(CaseLaw)
    legislatures = models.ManyToManyField(Legislature)

    peshi = models.FileField(upload_to='files/peshi/',null = True)
    peshi_char = models.CharField(max_length=2000)
    order = models.FileField(upload_to='files/order/',null = True)
    order_char = models.CharField(max_length=2000)

    ORDERSTATUS_CHOICES = (
    ("DRAFT", "DRAFT"),
    ("REVIEW", "REVIEW"),
    ("FINAL", "FINAL")
    )
    
    status = models.CharField(max_length=20)
    order_status = models.CharField(max_length=15,choices=ORDERSTATUS_CHOICES,default="DRAFT")
    order_pass_date = models.DateField()
    is_urgent = models.BooleanField(default=False)

    matter = models.CharField(max_length=30,default="N.A.")

    petitioner_advocate = models.CharField(max_length=30,default="N.A.")
    respondant_advocate = models.CharField(max_length=30,default="N.A.")
    party = models.CharField(max_length=30,default="N.A.")

    notes = models.CharField(max_length=2000,default="N.A.")

    CASETYPE_CHOICES = (
    ("SUPPLEMENTARY", "Supplementary"),
    ("ADVANCE", "Advance")
    )
    
    case_type = models.CharField(max_length=15,choices=CASETYPE_CHOICES,default="SUPPLEMENTARY")
    def __str__(self):
        return self.case_number

