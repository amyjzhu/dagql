echom "About to load DAGQL syntax highlighting"
"if exists("b:current_syntax")
"    finish
"endif

echom "Loaded DAGQL syntax highlighting"
let b:current_syntax = "dagql"

syntax keyword dagqlKeyword SELECT FROM AS
syntax keyword dagqlKeyword TRAVERSE BY 
syntax keyword dagqlConstant TRUE FALSE DEPTH BREADTH EDGES NODES

syntax keyword dagqlFunction SEARCH WHERE LIMIT


syntax match dagqlString "\v'[^']*'"
syntax match dagqlNumber "\v[0-9]+(\.[0-9]+)?"
syntax match dagqlNumber "\v0x[0-9a-fA-F]+"
syntax match dagqlNumber "\v0b[01]+"
syntax match dagqlNumber "\v0o[0-7]+"

syntax match dagqlOperator "\v\*\*\=?"
syntax match dagqlOperator "\v\+\=?"
syntax match dagqlOperator "\v\-\=?"
syntax match dagqlOperator "\v!\=?\=?"
syntax match dagqlOperator "\v\^\=?"
syntax match dagqlOperator "\v\*\=?"
syntax match dagqlOperator "\v/\=?"
syntax match dagqlOperator "\v//\=?"
syntax match dagqlOperator "\v\%\=?"
syntax match dagqlOperator "\v\>\>\=?"
syntax match dagqlOperator "\v\<\<\=?"
syntax match dagqlOperator "\v\&\&?\=?"
syntax match dagqlOperator "\v\~\=?"
syntax match dagqlOperator "\v\<\=?"
syntax match dagqlOperator "\v\>\=?"
syntax match dagqlOperator "\v\?\?\=?"
syntax match dagqlOperator "\v\=\=?\=?"

"syntax region dagqlComment start="/\*" end="\*/"
"syntax match dagqlComment "\v\".*$"

highlight link dagqlOperator Operator
highlight link dagqlKeyword Keyword
highlight link dagqlConstant Constant
highlight link dagqlFunction Function
"highlight link dagqlComment Comment
highlight link dagqlString String
highlight link dagqlNumber Number
