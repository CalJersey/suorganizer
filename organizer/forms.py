from django import forms
from django.forms.widgets import HiddenInput
from django.core.exceptions import ValidationError
from .models import Tag, NewsLink, Startup

class SlugCleanMixin:
    def clean_slug(self):
        new_slug = (
            self.cleaned_data['slug'].lower()
        )
        if new_slug == 'create':
            raise ValidationError(
                'Slug may not be "create".'
            )
        return new_slug

class NameCleanMixin:
    def clean_name(self):
        return self.cleaned_data['name'].lower()

class TagForm(NameCleanMixin, SlugCleanMixin, forms.ModelForm):

    class Meta:
        model = Tag
        fields = '__all__'


class NewsLinkForm(NameCleanMixin, SlugCleanMixin, forms.ModelForm):

    class Meta:
        model = NewsLink
        fields = '__all__'
        widgets = {'startup':HiddenInput()}

    def clean(self):
        cleaned_data = super().clean()
        slug = cleaned_data.get('slug')
        startup_obj = self.data.get('startup')
        exists = (
            NewsLink.objects.filter(
                slug__iexact=slug,
                startup=startup_obj,
            ).exists()
        )
        if exists:
            raise ValidationError(
                "News article with this Slug and Startup already exists."
            )
        else:
            return cleaned_data

    def save(self, **kwargs):

        instance = super().save(commit=False)
        instance.startup = (self.data.get('startup'))
        instance.save()
        self.save_m2m()

        return instance


class StartupForm(NameCleanMixin, SlugCleanMixin, forms.ModelForm):

    class Meta:
        model = Startup
        fields = '__all__'