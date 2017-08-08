from django.contrib.admin.sites import site
from django.contrib.auth.models import Group
from django.contrib.sessions.models import Session
from django.utils import translation
from django_admin_caching.caching import CacheKey
import pytest
from testapp.test_helpers import translation_being


@pytest.mark.parametrize(
    'admin_cls,result,expected_key', [
        (Session, Group(pk=3),
         'django.contrib.sessions.models.Session-auth.Group-3'),
        (Group, Group(pk=5),
         'django.contrib.auth.models.Group-auth.Group-5'),
    ]
)
def test_cache_key_is_derived_from_admin_and_obj_by_default(
        admin_cls, result, expected_key):
    ck = CacheKey(model_admin=admin_cls(), result=result)
    assert ck.result_key() == '{}'.format(result.pk)
    assert ck.key == expected_key


def test_can_provide_custom_override_to_cache_key_through_model_admin():
    class AdminWithCustomCacheKey(object):
        def admin_caching_key(self, obj):
            return 'Foo:Bar:9'

    ck = CacheKey(model_admin=AdminWithCustomCacheKey(), result=Group(pk=55))
    assert ck.result_key() == 'Foo:Bar:9'
    assert ck.key == \
        '{}.AdminWithCustomCacheKey-auth.Group-Foo:Bar:9'.format(
            AdminWithCustomCacheKey.__module__)


def test_when_model_admin_is_not_provided_it_is_derived_from_admin_registry():
    session_obj = Session()
    ck_explicit_admin = CacheKey(result=Group(), model_admin=session_obj)
    assert ck_explicit_admin.model_admin == session_obj

    ck_derived_admin = CacheKey(result=Group())
    assert ck_derived_admin.model_admin == site._registry[Group]

    orig_admin = site._registry[Group]
    try:
        admin_obj = object()
        site._registry[Group] = admin_obj
        ck_derived_admin = CacheKey(result=Group())
        assert ck_derived_admin.model_admin == site._registry[Group]
    finally:
        site._registry[Group] = orig_admin


@pytest.mark.parametrize(
    'language,i18n,l10n,expected_key_prefix', [
        ('en', True, True, 'en.en'),
        ('de-ch', True, True, 'de-ch.de_CH'),
        ('en-us', True, True, 'en-us.en_US'),
        ('en-us', True, False, 'en-us'),
        # L10N doesn't work w/out I18N
        # ('en-us', False, False, 'en_US'),
        ('en-us', False, False, ''),
    ]
)
def test_key_is_i18n_l10n_aware_if_settings_enabled(settings, language, i18n,
                                                    l10n, expected_key_prefix):
    settings.USE_I18N = i18n
    settings.USE_L10N = l10n
    with translation_being(language):
        ck = CacheKey(result=Group(pk=1))
        assert ck.i18n_l10n_prefix == expected_key_prefix
        assert ck.key.startswith(expected_key_prefix)
        if expected_key_prefix:
            assert ck.key.startswith('{}.'.format(expected_key_prefix))


def test_when_all_language_is_deactivated(settings):
    settings.USE_I18N = True
    settings.USE_L10N = True
    with translation_being('en'):
        translation.deactivate_all()
        ck = CacheKey(result=Group(pk=1))
        _ = ck.i18n_l10n_prefix
