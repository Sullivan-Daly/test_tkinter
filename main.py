# coding: utf-8
# -*- coding: utf-8 -*-

from own_table import MenuDemo

if __name__ == '__main__':
    xM = MenuDemo()



# POST /twitter_test/tweet/AVnSyHjpBcM_BKrrmRNg/_update
# {
#    "script" : "ctx._source.new_field = 'value_of_new_field'"
# }



# POST twitter_test/_update_by_query
# {
#      "query" : {
#         "match_all" : {}
#     },
#     "script" : {
#       "inline": "ctx._source. = 'foo'"
#     }
# }