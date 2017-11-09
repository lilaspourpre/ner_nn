# -*- coding: utf-8 -*-
# import codecs
# import numpy as np
# import pymorphy2

# morph = pymorphy2.MorphAnalyzer()
#
#
#     def length(self):
#         return [len(self.token_text)]
#
#     def pos(self):
#         parsed_word = morph.parse(self.token_text)[0]
#         pos = str(parsed_word.tag.POS)
#         if 'NOUN' in pos:
#             return [0, 0, 0]
#         elif 'VERB' in pos:
#             return [0, 0, 1]
#         elif 'ADJ' in pos:
#             return [0, 1, 0]
#         elif 'PREP' in pos:
#             return [0, 1, 1]
#         elif 'PNCT' in pos:
#             return [1, 0, 0]
#         elif 'CONJ' in pos:
#             return [1, 0, 1]
#         else:
#             return [1, 1, 0]
#
#     def flection(self):
#         return [0, 1]
#
#     def case(self):
#         if self.token_text.isupper():
#             return [0, 0]
#         elif self.token_text.islower():
#             return [0, 1]
#         elif self.token_text.istitle():
#             return [1, 0]
#         else:
#             return [1, 1]
