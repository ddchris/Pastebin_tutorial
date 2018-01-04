from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXER = [item for item in get_all_lexers() if item[1]]

LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXER ])

STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    '''
    ForeignKey 表示此 model 依附在 auth.User model(指向其主鍵), 
    on_delete 表示當 User 物件刪除時其 Snippet 物件也要一併刪除
    '''
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE, default= '')
    highlighted = models.TextField(default= '')

    # 複寫 model.Model 內的 save()，使其在存檔前添加高亮語法
    def save(self, *args, **kwargs):
        '''
        使用 pygments 創建高亮的HTML文本
        '''
        lexer = get_lexer_by_name(self.language)
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                    full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)

        '''
        呼叫父類別內的 save() 存檔
        '''
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ('created',)








