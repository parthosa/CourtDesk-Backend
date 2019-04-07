"""
Definition of models.
"""

from django.db import models

# Create your models here.

class Permission(models.Model):
    name = models.CharField(max_length=20,primary_key=True)
    view_peshi = models.BooleanField(default=False)
    edit_peshi = models.BooleanField(default=False)
    edit_casefile = models.BooleanField(default=False)

    def __str__(self):
        return self.name




class LR(models.Model):
    name = models.CharField(max_length=20)
    permissions = models.ForeignKey(Permission,on_delete=models.CASCADE,default="LR")
    def __str__(self):
        return self.name


class CourtStaff(models.Model):
    name = models.CharField(max_length=20)
    permissions = models.ForeignKey(Permission,on_delete=models.CASCADE,default="CS")
    def __str__(self):
        return self.name

class Judge(models.Model):
    name = models.CharField(max_length=20)
    permissions = models.ForeignKey(Permission,on_delete=models.CASCADE,default="JUDGE")
    lr = models.ManyToManyField(LR)
    court_staff = models.ManyToManyField(CourtStaff)

    def __str__(self):
        return self.name

class Court(models.Model):
    name = models.CharField(max_length=15,primary_key=True)

    def __str__(self):
        return self.name


class CourtRoom(models.Model):
    number = models.IntegerField(default=0)
    court = models.ForeignKey(Court,on_delete=models.CASCADE)
    def __str__(self):
        return self.court.name + "-" + str(self.number)

class CaseFile(models.Model):
    case_number = models.CharField(max_length=20)
    next_date_of_hearing = models.DateField()
    judges = models.ManyToManyField(Judge)
    court_room = models.ForeignKey(CourtRoom,on_delete = models.CASCADE)
    case_file = models.FileField(upload_to='files/casefiles/',null = True)
    peshi = models.FileField(upload_to='files/peshi/',null = True)

    matter = models.CharField(max_length=30,default="N.A.")
    petitioner_advocate = models.CharField(max_length=30,default="N.A.")
    respondant_advocate = models.CharField(max_length=30,default="N.A.")

    CASETYPE_CHOICES = (
    ("SUPPLEMENTARY", "Supplementary"),
    ("ADVANCE", "Advance")
    )
    
    case_type = models.CharField(max_length=15,choices=CASETYPE_CHOICES,default="SUPPLEMENTARY")
    def __str__(self):
        return self.case_number

class CaseLaw(models.Model):
    name = models.CharField(max_length=20)
    case_file = models.ForeignKey(CaseFile,on_delete = models.CASCADE)
    file = models.FileField(upload_to='files/caselaws/',null = True)

    def __str__(self):
        return self.name + "-" + self.case_file.name

class Legislature(models.Model):  
    name = models.CharField(max_length=20)
    case_file = models.ForeignKey(CaseFile,on_delete = models.CASCADE)
    file = models.FileField(upload_to='files/legislatures/',null = True)
    def __str__(self):
        return self.name + "-" + self.case_file.name
    