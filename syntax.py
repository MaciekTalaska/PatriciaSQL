from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QSyntaxHighlighter


class PgSQLHighlighter(QSyntaxHighlighter):

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        raw_data = open('colors.txt', 'rb').read()
        highlight_data = eval(raw_data)
        rules = self.process_data(highlight_data)

        self.rules = [(QRegExp(pattern), color)
                      for (pattern, color) in rules]

    def process_data(self, highlight_defs):
        rules = []
        for g in highlight_defs:
            # color
            text_color = g.get('color')
            color = QColor.fromRgb(int(text_color, 16))
            text_formatting = QTextCharFormat()
            text_formatting.setForeground(color)
            # group name
            group_name = g.get('name')
            if group_name == 'keywords':
                ks = "(\b" + str.join(r"\b)|(\b", g['words']) + "\b)"
                rules += [(r'%s' % ks, text_formatting)]
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
