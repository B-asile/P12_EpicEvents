from django.contrib.auth.models import Group

management_group, created = Group.objects.get_or_create(name='management')
sales_group, created = Group.objects.get_or_create(name='sales')
support_group, created = Group.objects.get_or_create(name='support')