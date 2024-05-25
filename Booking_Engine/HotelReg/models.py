from django.db import models

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    bin = models.CharField(max_length=100, unique=True)
    owner_name = models.CharField(max_length=255)
    owner_email = models.EmailField(null=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.bin:
            self.bin = self.generate_bin()
        super().save(*args, **kwargs)

    def generate_bin(self):
        import uuid
        return str(uuid.uuid4())

