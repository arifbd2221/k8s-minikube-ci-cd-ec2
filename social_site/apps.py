from django.apps import AppConfig


class SocialSiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'social_site'
    
    def ready(self):
        import social_site.signals  # Import the signals module
