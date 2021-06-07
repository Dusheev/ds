from django.forms import forms


class PostForm(forms.ModelForm):

    class Meta:
        model = my_models.Post
        fields = ('comment',)
        widgets = {
          'post': forms.Textarea(attrs={'rows':5, 'cols':40}),
        }