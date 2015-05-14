from .base import *


STAGE = "development"


INSTALLED_APPS += (
    'django_extensions', 
    )


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s module=%(module)s, '
            'process_id=%(process)d, %(message)s'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'celery': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'lets_encrypt_demo': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
