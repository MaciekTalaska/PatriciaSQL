from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QSyntaxHighlighter

hldata = \
    [
        {
            'name': 'keywords',
            'color': '0x0087ff',
            'words': ['all', 'analyse', 'analyze', 'array', 'as', 'asc', 'authorization', 'both', 'case', 'cast',
                      'check', 'collate', 'column', 'concurrently', 'constraint', 'create', 'current_catalog',
                      'current_date', 'current_role', 'current_schema', 'current_time', 'current_timestamp',
                      'current_user', 'defaults', 'deferrable', 'desc', 'distinct', 'do', 'else', 'end', 'except',
                      'false', 'fetch', 'for', 'foreign', 'from', 'full', 'grant', 'group by', 'having', 'ilike',
                      'initially', 'intersect', 'into', 'lateral', 'limit', 'localtime', 'localtimestamp', 'null',
                      'offset', 'on', 'only', 'order by', 'placing', 'primary', 'references', 'returning', 'select',
                      'session_user', 'similar', 'some', 'symmetric', 'table', 'then', 'trailing', 'true', 'union',
                      'unique', 'user', 'variadic', 'version', 'when', 'window', 'with'],
            'regex': '',
        },
        {
            'name': 'operators',
            'color': '0xdc322f',
            'words': ['\+', '-', '\*', '/', '\%', '\&', '\|', '\^', '=', '>', '<', '>=', '<=', '<>', '\+=', '-=', '\*=',
                      '/=', '\%=', '\%=', '\^-=', '\|*=', ' all ', ' and ', ' any ', ' between ', ' exists ', ' in ',
                      ' like ', ' not ', ' or ', ' some ', ],
            'regex': ''
        },
        {
            'name': 'strings',
            'color': '0xd33682',
            'words': [],
            'regex': r'"[^"\\]*(\\.[^"\\]*)*"'
        },
        {
            'name': 'strings',
            'color': '0xd33682',
            'words': [],
            'regex': r'"[^"\\]*(\\.[^"\\]*)*"'
        },
        {
            'name': 'numbers',
            'color': '0x268bd',
            'words': [],
            'regex': r'[+-]?\b\d+\b'
        },
        {
            'name': 'comments',
            'color': '0x839496',
            'words': [],
            'regex': r'--.*$'
        },
    ]


class PgSQLHighlighter(QSyntaxHighlighter):

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        rules = self.process_data(hldata)

        self.rules = [(QRegExp(pattern), color)
                      for (pattern, color) in rules]

    def process_data(self, highlightdata):
        rules = []
        for g in highlightdata:
            # color
            text_color = g.get('color')
            color = QColor.fromRgb(int(text_color, 16))
            text_formatting = QTextCharFormat()
            text_formatting.setForeground(color)
            # group name
            group_name = g.get('name')
            # c[group_name] = text_formatting
            if group_name == 'keywords':
                ks = str.join(r"|", g['words'])
                rules += [(r'\b%s\b' % ks, text_formatting)]
                continue
            if group_name == 'operators':
                os = str.join(r"|", g['words'])
                rules += [(r'%s' % os, text_formatting)]
                continue
            rules += [(g['regex'], text_formatting)]
        return rules


    def highlightBlock(self, text):
        for regx, style in self.rules:
            match = regx.indexIn(text, 0)
            while match > -1:
                index = regx.pos(0)
                length = len(regx.cap(0))
                self.setFormat(index, length, style)
                # check if there are any other tokens to be highlighted
                match = regx.indexIn(text, length + index)
            continue
        self.setCurrentBlockState(0)
