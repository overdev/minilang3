# -*- encoding: utf8 -*-

# region EXPORTS

__all__ = [
    'TK_WHITESPACE',
    'TK_WORD',
    'TK_KEYWORD',
    'TK_NUMBER',
    'TK_DELIMITER',
    'TK_OPERATOR',
    'TK_STRING',
    'TK_COMMENT',
    'TK_DOCUMENTATION',
    'TK_EOF',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'COMMA',
    'DOT',
    'ASSIGN',
    'LSHIFT',
    'SEMICOLON',
    'COLON',
    'POINTER',
    'INCR',
    'DECR',
    'ADD',
    'SUB',
    'MUL',
    'DIV',
    'MOD',
    'SK_SINGLEQUOTE',
    'SK_DOUBLEQUOTE',
    'SK_TEMPLATE',
    'SK_RESERVED',
    'KW_IMPORT',
    'KW_GET',
    'KW_SET',
    'KW_IF',
    'KW_ELIF',
    'KW_ELSE',
    'KW_WHILE',
    'KW_DO',
    'KW_SWITCH',
    'KW_RETURN',
    'KW_BREAK',
    'KW_BREAKPOINT',
    'KW_CONTINUE',
    'KW_REPEAT',
    'KW_PRINT',
    'KW_ASSERT',
    'SK_ACCESS',
    'KW_PUBLIC',
    'KW_PROTECTED',
    'KW_PRIVATE',
    'SK_KEYVALUE',
    'KW_NULL',
    'KW_TRUE',
    'KW_FALSE',
    'KW_THIS',
    'KW_SUPER',
    'KW_BASE',
    'KW_VALUE',
    'SK_QUALIFIER',
    'KW_STATIC',
    'KW_UNBOUND',
    'KW_FINAL',
    'KW_ABSTRACT',
    'KW_CONST',
    'KW_READONLY',
    'KW_OVERRIDE',
    'KW_OVERLOAD',
    'SK_PRIMITIVE',
    'KW_I8',
    'KW_I16',
    'KW_I32',
    'KW_I64',
    'KW_U8',
    'KW_U16',
    'KW_U32',
    'KW_U64',
    'KW_F32',
    'KW_F64',
    'KW_BOOLEAN',
    'KW_STRING',
    'SK_IDENTIFIER',
    'SK_INTEGER',
    'SK_FLOAT',
]

# endregion (exports)

# region CONSTANTS


TK_WHITESPACE = 'WS'
TK_WORD = 'WORD'
TK_KEYWORD = 'KEYWORD'
TK_NUMBER = 'NUMBER'
TK_DELIMITER = 'DELIMITER'
TK_OPERATOR = 'OPERATOR'
TK_STRING = 'STRING'
TK_COMMENT = 'COMMENT'
TK_DOCUMENTATION = 'DOCUMENTATION'
TK_EOF = 'EOF'
LPAREN = '('
RPAREN = ')'
LBRACE = '{'
RBRACE = '}'
LBRACKET = '['
RBRACKET = ']'
COMMA = ','
DOT = '.'
ASSIGN = '='
LSHIFT = '<<'
SEMICOLON = ';'
COLON = ':'
POINTER = '->'
INCR = '++'
DECR = '--'
ADD = '+'
SUB = '-'
MUL = '*'
DIV = '/'
MOD = '%'
SK_SINGLEQUOTE = 'SINGLEQUOTE'
SK_DOUBLEQUOTE = 'DOUBLEQUOTE'
SK_TEMPLATE = 'TEMPLATE'
SK_RESERVED = 'RESERVED'
KW_IMPORT = 'import'
KW_GET = 'get'
KW_SET = 'set'
KW_IF = 'if'
KW_ELIF = 'elif'
KW_ELSE = 'else'
KW_WHILE = 'while'
KW_DO = 'do'
KW_SWITCH = 'switch'
KW_RETURN = 'return'
KW_BREAK = 'break'
KW_BREAKPOINT = 'breakpoint'
KW_CONTINUE = 'continue'
KW_REPEAT = 'repeat'
KW_PRINT = 'print'
KW_ASSERT = 'assert'
SK_ACCESS = 'ACCESS'
KW_PUBLIC = 'public'
KW_PROTECTED = 'protected'
KW_PRIVATE = 'private'
SK_KEYVALUE = 'KEYVALUE'
KW_NULL = 'null'
KW_TRUE = 'true'
KW_FALSE = 'false'
KW_THIS = 'this'
KW_SUPER = 'super'
KW_BASE = 'base'
KW_VALUE = 'value'
SK_QUALIFIER = 'QUALIFIER'
KW_STATIC = 'static'
KW_UNBOUND = 'unbound'
KW_FINAL = 'final'
KW_ABSTRACT = 'abstract'
KW_CONST = 'const'
KW_READONLY = 'readonly'
KW_OVERRIDE = 'override'
KW_OVERLOAD = 'overload'
SK_PRIMITIVE = 'PRIMITIVE'
KW_I8 = 'i8'
KW_I16 = 'i16'
KW_I32 = 'i32'
KW_I64 = 'i64'
KW_U8 = 'u8'
KW_U16 = 'u16'
KW_U32 = 'u32'
KW_U64 = 'u64'
KW_F32 = 'f32'
KW_F64 = 'f64'
KW_BOOLEAN = 'boolean'
KW_STRING = 'string'
SK_IDENTIFIER = 'IDENTIFIER'
SK_INTEGER = 'INTEGER'
SK_FLOAT = 'FLOAT'

# endregion (constants)
