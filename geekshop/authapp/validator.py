# from django.core.exceptions import ValidationError
# from django.utils.translation import ngettext_lazy as _
#
# def validator_name(value):
#     if value.isdigit():
#         raise ValidationError(
#             _(f'Имя не может состоять только из циферок'),
#             params=('value': value),
#         )
#     if not value.isalpha():
#         raise ValidationError(
#             _(f'Имя не может содержать циферки'),
#             params=('value': value),
#         )
