Function
  intro
  with attr
  with para
  define color
Command
  fields
  pattern
  short args
  with shell
Customization
  intro
  environment variable
  find favorite colors
  
====================

They are designed for temporary using.
It is not recommended that using them in production,
instead, just hard code the string with color control code
such as `\033[32m{}\033[m`.



====================

不同的 terminal 顯示顏色可能不太一樣, 因此需要 customization

====================

colorex

https://bitbucket.org/linibou/colorex/wiki/Home

====================


.. 1. define color name
     1.1 (X) 考慮量多, 還是用單一檔案
     1.2 不考慮 COLORPRINT_XXX, 我定義的不是常數名稱, 所以不適合
     1.3 (X) 雖然考慮了 GREP_COLORS 的語法設計, 但量一多還是很難寫好看
     1.4 format 一切從簡; parser 會把 [,:;|\s]+ 全部換成空白, parsing 失敗會噴行號和 warning
     1.5 單一設定就會以 GREP_COLORS 的設計為主
     1.6 如果檔案和環境變數都有設定, 檔案優先, 噴 warning 說建議二選一
     1.7 容錯噴 warning; 除了環境變數一行設定以冒號分隔以外, 其他的都取代成空白
         print/pprint 也要在第一次 import 時提醒這個問題
     1.8 要有參數給出所有的 color name 和 customized color name

.. 2. default color
     2.1 no need to consider default color
         just set color explicit
     2.2 function cpf { colorprint --fields "$@" default_color ; }
     2.3 function cpp { colorprint --pattern "$@" default_color ; }
         stream | cpp patt | cpp patt

.. 3. 不考慮 `--mode` 因為
      這只是 light-weight tool, line by line, 僅能當作臨時上色用
      長期, 例如 date, 可以直接上色; git log 有上下文關係, 較不好上色
      所以就不考慮更偉大的使用方式
      但會提供 alias 和 function 的使用範例

.. 4. 追加 print/pprint 有參數 colors
      It is for explicit, so just use 'colors' as argument name

.. 5. 追加 兩種定義法的轉換, 它必須是互動式的功能
      參數 --conf2var, --var2conf: 幫助處理衝突, 轉換, 寫檔
      參數 --show-names: show custom names 

.. 6. Let methods as `print_` and `pprint_`

.. 7. Add attributes feature to support `update` ...etc

.. 8. Is there a way to get
