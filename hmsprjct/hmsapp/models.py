# models.py
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
   

    def __str__(self):
        return self.name
from django.db import models

class mortuary_table(models.Model):
    fullname = models.CharField(max_length=250)
    dod = models.DateField()  # Date of Death
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),  # Additional option for non-binary or other gender identities
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
    )
    cause_of_death = models.TextField()
    death_cert_num = models.CharField(max_length=20, unique=True)
    mortuary_fee = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'mortuary_table'

    def __str__(self):
        return (
            f"{self.dod} - {self.get_gender_display()} - "
            f"{self.cause_of_death} - {self.death_cert_num} - {self.mortuary_fee}"
        )
