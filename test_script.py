from django_gravatar.helpers import get_gravatar_url

from authentication.models import Account
from job.models import Job
from proxies.models import IP
from seed.models import Seed

for i in range(20):
    user = Account.objects.create_user(username='user_' + str(i),
                                       first_name='First' + str(i),
                                       last_name='Last' + str(i),
                                       email='address' + str(i) + '@gmail.com',
                                       profile_picture=get_gravatar_url('address' + str(i) + '@gmail.com'),
                                       password='user_' + str(i)
                                       )
    user.save()

for acc in Account.objects.all():
    # Create Seed Lists:

    for i in range(100):
        seed = Seed.objects.create(
            user=acc,
            list_name='seed_' + acc.username,
            proxyType='proxy'
        )

        seed.save()

    # Creat Jobs:

    j = 0

    for i in range(10):
        job = Job.objects.create(
            user=acc
        )
        seeds = Seed.objects.all()[j: j + 9]
        for seed in seeds:
            job.seed_list.add(seed)
        job.save()
        j += 10

    for i in range(1, 5):
        for j in range(1, 255):
            ip = IP.objects.create(
                ip_address='192.168.' + str(i) + '.' + str(j),
                ip_port=1000 + j,
                ip_login='login' + str(j),
                ip_password='pass' + str(j)
            )
            ip.save()
