from config.account_config import get_account_usecase
from social_oauth.application.usecase.google_oauth2_usecase import GoogleOAuth2UseCase
from social_oauth.infrastructure.service.google_oauth2_service import GoogleOAuth2Service

# 전역 변수들
_service_instance = None
_usecase_instance = None

def get_google_oauth2_service() -> GoogleOAuth2Service:
    global _service_instance
    if _service_instance is None:
        _service_instance = GoogleOAuth2Service()
    return _service_instance

def get_google_oauth2_usecase() -> GoogleOAuth2UseCase:
    global _usecase_instance
    if _usecase_instance is None:
        _usecase_instance = GoogleOAuth2UseCase(
            get_google_oauth2_service(),
            get_account_usecase()
        )
    return _usecase_instance
