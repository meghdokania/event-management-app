from import_export import resources
from users.models import CustomUser

class CustomUserResource(resources.ModelResource):
    class Meta:
        model = CustomUser