from django.db import models
from django.utils.timezone import now
# Create your models here.

class Job_fairs(models.Model):
    job_fair_id = models.AutoField(primary_key=True)
    district = models.CharField(max_length=100)
    date_of_job_fair = models.DateField()
    date_of_creation = models.DateTimeField(default=now)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    class Meta:
        db_table = 'job_fairs'  

    def __str__(self):
        return f"{self.district} - {self.date_of_job_fair}"

