echom "Loaded DAGQL syntax highlighting"
let b:current_syntax = "dagql"

syntax keyword dagqlKeyword SELECT FROM AS WHERE LIMIT SEARCH
syntax keyword dagqlKeyword TRAVERSE BY DEPTH BREADTH
syntax keyword dagqlConstant TRUE FALSE EDGES NODES

syntax match dagqlString "\v'[^']*'"
syntax match dagqlNumber "\v[0-9]+(\.[0-9]+)?"
syntax match dagqlNumber "\v\.[0-9]+"

syntax match dagqlOperator "\v\*"
syntax match dagqlOperator "\v\+"
syntax match dagqlOperator "\v\-"
syntax match dagqlOperator "\v/"
syntax match dagqlOperator "\v\|\|"
syntax match dagqlOperator "\v\<\=?"
syntax match dagqlOperator "\v\>\=?"
syntax match dagqlOperator "\v\="
syntax keyword dagqlOperator AND OR NOT

syntax match dagqlComment "\v--.*$"

highlight link dagqlOperator Operator
highlight link dagqlKeyword Keyword
highlight link dagqlConstant Constant
"highlight link dagqlComment Comment
highlight link dagqlString String
highlight link dagqlNumber Number
