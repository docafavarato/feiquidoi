from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(blank=True, upload_to='users/%Y/%m/%d')
    
    def __str__(self):
        return f'Perfil de {self.user.username}'
    
class Contact(models.Model):
    user_from = models.ForeignKey('auth.User',
                                  related_name ='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User',
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)
    
    class Meta:
        ordering = ('-created',)
        
    def __str__(self):
        return f'{self.user_from} segue {self.user_to}'


# Add following field to User dynamically
user_model = get_user_model()
user_model.add_to_class('following',
                        models.ManyToManyField('self',
                                                through=Contact,
                                                related_name='followers',
                                                symmetrical=False))