from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, MultiWidgetField

SORT = (
    ('activity', 'activity'),
    ('votes', 'votes'),
    ('creation', 'creation'),
    ('relevance', 'relevance')
)
ORDER = (
    ('desc', 'desc'),
    ('asc', 'asc')
)

TRUE_OR_FALSE = (
    ('', '---'),
    ('True', 'True'),
    ('False', 'False')
)


class SearchForm(forms.Form):
    d = forms.DateTimeField(widget=forms.DateTimeInput(attrs={
        'class': 'form-control datetimepicker-input',
        'data-target': '#datetimepicker1'
    }), required=False)
    page = forms.IntegerField(widget=forms.NumberInput(), required=False, min_value=1)
    pagesize = forms.IntegerField(widget=forms.NumberInput(), required=False, min_value=1)
    # from_date = forms.DateField(widget=forms.SelectDateWidget(), required=False)
    # to_date = forms.DateField(widget=forms.SelectDateWidget(), required=False)
    from_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    to_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    order = forms.ChoiceField(choices=ORDER)
    min = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    max = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    sort = forms.ChoiceField(choices=SORT)
    q = forms.CharField(widget=forms.TextInput(), label='Query', required=False)
    accepted = forms.ChoiceField(choices=TRUE_OR_FALSE, required=False)
    answers = forms.IntegerField(widget=forms.NumberInput(), required=False, min_value=1)
    body = forms.DateField(widget=forms.TextInput(), required=False)
    closed = forms.ChoiceField(choices=TRUE_OR_FALSE, required=False)
    migrated = forms.ChoiceField(choices=TRUE_OR_FALSE, required=False)
    notice = forms.ChoiceField(choices=TRUE_OR_FALSE, required=False)
    nottagged = forms.CharField(widget=forms.TextInput(), required=False)
    tagged = forms.CharField(widget=forms.TextInput(), required=False)
    title = forms.CharField(widget=forms.TextInput(), required=False)
    user = forms.CharField(widget=forms.NumberInput(), required=False)
    url = forms.CharField(widget=forms.TextInput(), required=False)
    views = forms.IntegerField(widget=forms.NumberInput(), required=False, min_value=0)
    wiki = forms.ChoiceField(choices=TRUE_OR_FALSE, required=False)

