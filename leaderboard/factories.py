import factory
from faker import Faker
from .models import User

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    name = factory.LazyAttribute(lambda _: fake.name())
    age = factory.LazyAttribute(lambda _: fake.random_int(min=18, max=70))
    points = factory.LazyAttribute(lambda _: fake.random_int(min=2, max=67))
    address = factory.LazyAttribute(lambda _: fake.address())
    # photo = factory.LazyAttribute(lambda _: fake.image_url())
