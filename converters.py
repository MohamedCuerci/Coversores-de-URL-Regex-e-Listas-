from werkzeug.routing import BaseConverter


#items = (a.*) por exemplo, caso fosse passado mais argumentos ele seriam detectados como "lista" items[1], items[2] etc
class RegexConverter(BaseConverter):
    def __init__(self, url_map, items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


#permite retorna varias informaçoes diferentes concatenadas pelo + , como no reddit
class ListConvert(BaseConverter):
    '''nome+nome2+nome3+etc'''

    #converte o q foi passado na url para ser usado no python
    def to_python(self, value):
        return value.split('+')

    #converte do python para url
    def to_url(self, values):
        return '+'.join(
            BaseConverter.to_url(self, item)
            for item in values
        )