from django.core.management.base import BaseCommand
from workouts.models import CustomUser

class Command(BaseCommand):
    help = 'Удалить пользователей по условию'

    def add_arguments(self, parser):
        parser.add_argument('condition', type=str, help='Условие для выбора пользователей')

    def handle(self, *args, **kwargs):
        condition = kwargs['condition']
        users_to_delete = CustomUser.objects.filter(email__icontains=condition)
        for user in users_to_delete:
            user.delete()
            self.stdout.write(self.style.SUCCESS(f'Пользователь {user.email} удалён'))

# python manage.py delete_users "email__icontains:example"
