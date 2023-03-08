from django.db import models
from django.core import checks
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):


    description = "Ordering field on a unique field"

    def __init__(self, unique_for_field=None, *args, **kwargs):
        self.unique_for_field = unique_for_field
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_for_field_attribute(**kwargs),
        ]

    def _check_for_field_attribute(self, **kwargs):
        if self.unique_for_field is None:
            return [
                checks.Error("OrderField must define a 'unique_for_field' attribute")
            ]
        elif self.unique_for_field not in [f.name for f in self.model._meta.get_fields()]:
            # grab a list of all the fields in the table and check to see if unique_for_field is in field names
            return [
                checks.Error("OrderField entered does not match an existing model field")
            ]


        return []

    def pre_save(self, model_instance, add):
        # each one of the field in admin, is gets passed from here individually
        # print("HELLO")
        print(model_instance)

        if getattr(model_instance, self.attname) is None:
            # print(getattr(model_instance, self.attname))
            # print("NEED A VALUE")
            qs = self.model.objects.all()
            try:
                # building query string
                query = {self.unique_for_field : getattr(model_instance, self.unique_for_field)}
                # print(query)
                # filter our particular product lines based upon the unique_for_field
                qs = qs.filter(**query)
                last_item = qs.latest(self.attname)
                value = last_item.order + 1 # grab the last order object value and add 1 to it
                # print(self.attname)
                # print(qs)
            except ObjectDoesNotExist:
                value = 1

            return value
        else:
            return super().pre_save(model_instance, add)