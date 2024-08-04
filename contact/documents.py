from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Contact
from phonenumber_field.serializerfields import PhoneNumberField


class PhoneNumberField(fields.TextField):
    def get_value_from_instance(self, instance, field_value_to_ignore=None):
        value = super().get_value_from_instance(instance, field_value_to_ignore)
        print(value)
        return str(value)


# class UserField(fields.ObjectField):
#     def get_value_from_instance(self, instance, field_value_to_ignore=None):
#         value = super().get_value_from_instance(instance, field_value_to_ignore)
#         return {
#             "first_name": value.first_name,
#             "last_name": value.last_name,
#             "email": value.email,
#         }


@registry.register_document
class ContactDocument(Document):
    phone = PhoneNumberField(attr="phone", fields={
                             'raw': fields.KeywordField()})

    first_name = fields.TextField(
        fields={
            'keyword': fields.KeywordField(),
        }
    )
    last_name = fields.TextField(
        fields={
            'keyword': fields.KeywordField(),
        }
    )

    class Index:
        name = 'contacts'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    user = fields.ObjectField(properties={
        "first_name": fields.TextField(),
        "last_name": fields.TextField(),
        "number": PhoneNumberField(),
        "email": fields.TextField(),
    })

    class Django:
        model = Contact  # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            "email",
            "spam",
        ]
