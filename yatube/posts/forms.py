from django import forms  # Импортируем модуль forms, из него возьмём класс ModelForm

from .models import Post  # Импортируем модель, чтобы связать с ней форму

class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        # Здесь перечислим поля модели, которые должны отображаться в веб-форме;
        # при необходимости можно вывести в веб-форму только часть полей из модели.
        fields = ('text', 'group')

        def clean_text(self):
            data = self.cleaned_data['text']

            if self.cleaned_data['text'] == '':
                raise forms.ValidationError('Пост не может быть пустым!')

            return data 

