from authentication.models import Account
from seed.models import Seed

account = Account.objects.latest('updated_at')

for i in range(20):
    Seed.objects.create(user=account, list_name='seed_test_0' + str(i), proxyType='proxy').save()

Seed.objects.all()