

from authentication.models import User


def create_superuser(username):
    user = User.objects.get(username=username)
    user.is_staff = True
    user.save()
    return user

def create_superuser_and_add_level(self):
        response= self.client.post(path=self.register_url,data=self.user_data[1],format='json')
        username = response.data['user']['username']
        user = create_superuser(username)
        
        self.client.login(username='rengo',password='ararar6029676')
        self.client.post(path=self.levels_url,data=self.levels_data[0],format='json')
        #self.client.logout()
