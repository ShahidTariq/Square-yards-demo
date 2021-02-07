from django import forms


# creating a Demo form
class DemoForm(forms.Form):
    address_file = forms.FileField(help_text="Upload address XL file", widget=forms.ClearableFileInput(
        attrs={"accept": ".xlsx, .xls,"}
    ))

    def __init__(self, *args, **kwargs):
        super(DemoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def validate(self, value):
        # First run the parent class' validation routine
        super().validate(value)        # Run our own file extension check
        file_extension = os.path.splitext(value.name)[1]
        if file_extension != '.csv':
            raise ValidationError(
                 ('Invalid file extension'),
                 code='invalid'
            )
