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
    page = forms.IntegerField(widget=forms.NumberInput(), required=False, min_value=1)
    pagesize = forms.IntegerField(widget=forms.NumberInput(), required=False, min_value=1)
    from_date = forms.DateField(widget=forms.SelectDateWidget(), required=False)
    to_date = forms.DateField(widget=forms.SelectDateWidget(), required=False)
    order = forms.ChoiceField(choices=ORDER)
    min = forms.DateField(widget=forms.SelectDateWidget(), required=False)
    max = forms.DateField(widget=forms.SelectDateWidget(), required=False)
    sort = forms.ChoiceField(choices=SORT)
    q = forms.CharField(widget=forms.TextInput(), label='Query', required=False)
    accepted = forms.ChoiceField(choices=TRUE_OR_FALSE, required=False)
    answers = forms.IntegerField(widget=forms.NumberInput(), required=False, min_value=1)
    body = forms.CharField(widget=forms.TextInput(), required=False)
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('page', css_class='form-group col-md-1 mb-0'),
                Column('pagesize', css_class='form-group col-md-1 mb-0'),
                Column(MultiWidgetField('from_date', attrs=({'style': 'width: 33%; display: inline-block;'}))
                       , css_class='form-group col-md-2 mb-0'),
                Column(MultiWidgetField('to_date', attrs=({'style': 'width: 33%; display: inline-block;'}))
                       , css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('order', css_class='form-group col-md-2 mb-0'),
                Column(MultiWidgetField('min', attrs=({'style': 'width: 33%; display: inline-block;'}))
                       , css_class='form-group col-md-2 mb-0'),
                Column(MultiWidgetField('max', attrs=({'style': 'width: 33%; display: inline-block;'}))
                       , css_class='form-group col-md-2 mb-0'),
                Column('sort', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('q', css_class='form-group col-md-2 mb-0'),
                Column('accepted', css_class='form-group col-md-2 mb-0'),
                Column('answers', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('body', css_class='form-group col-md-2 mb-0'),
                Column('closed', css_class='form-group col-md-2 mb-0'),
                Column('migrated', css_class='form-group col-md-2 mb-0'),
                Column('notice', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('nottagged', css_class='form-group col-md-2 mb-0'),
                Column('tagged', css_class='form-group col-md-2 mb-0'),
                Column('title', css_class='form-group col-md-2 mb-0'),
                Column('user', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('url', css_class='form-group col-md-2 mb-0'),
                Column('views', css_class='form-group col-md-2 mb-0'),
                Column('wiki', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Search Questions')
        )


