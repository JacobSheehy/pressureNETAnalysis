import hashlib

from django import forms

from customers.models import Customer


class CustomerForm(forms.ModelForm):
    api_key = forms.CharField(required=False)

    class Meta:
        model = Customer
        fields = (
            'customer_type',
            'customer_plan',
            'company_name',
            'contact_name',
            'contact_mail',
            'contact_phone',
            'contact_address',
            'comments',
            'api_key',
        )

    def clean(self):
        cleaned_data = super(CustomerForm, self).clean()

        # Generate API Key
        company_name = cleaned_data.get('company_name')
        contact_name = cleaned_data.get('contact_name')
        contact_email = cleaned_data.get('contact_mail')

        customer_info = '%s;%s;%s' % (company_name, contact_name, contact_email)
        message = hashlib.md5(customer_info)
        api_key = message.hexdigest()

        cleaned_data['api_key'] = api_key

        return cleaned_data
