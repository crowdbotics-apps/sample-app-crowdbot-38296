class FieldRequestViewsetMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.excluded_fields = list()

    def add_excluded_field(self, field_name):
        if field_name in self.excluded_fields:
            return
        self.excluded_fields.append(field_name)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        fields = self.request.GET.get('fields', []) if self.request else []
        if fields:
            cleaned_fields = [f for f in set(fields.split(',')) if f not in self.excluded_fields]
            context.update({'fields': cleaned_fields})

        if self.excluded_fields:
            context.update({'excluded_fields': self.excluded_fields})

        return context
