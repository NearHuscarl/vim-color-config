# Colorscheme config

Generate vim colorscheme file from simple yaml config

#### Input
``` yaml
name: example
author:
   name: Near Huscarl
   email: near.huscarl@gmail.com
license: BSD 3-Clauses
note: sample color config for demonstartion purpse only
option:
   transparent: true
   background: dark
palette:
   # color name         gui         cterm    optional
   dark:             ['#1F2D3A',      0,     'black'    ]
   yellow:           ['#F39C12',      3,     'yellow'   ]
   blue:             ['#2980B9',      4,     'blue'     ]
   gray:             ['#84888B',      7,     'lightgray']
   red:              ['#E74C3C',      9,     'lightred' ]
   white:            ['#ECF0F1',      15,    'white'    ]
group:
   #              fg          bg         attr
   Normal:        white       dark       _
   LineNr:        gray        dark       _
   Error:         red         _          reverse
   Identifier:    blue        _          _
   Ignore:        _           _          _
   Statement:     yellow      _          _
link:
   - Conditional              ->     Statement
   - PreProc                  ->     Error
```

#### Output
``` vim
" ==============================================================
" File:        example.vim
" Description: example colorscheme
" Author:      Near Huscarl <near.huscarl@gmail.com>
" Last Change: Wed Dec 27 02:00:11 +07 2017
" Licence:     BSD 3-Clauses
" Note:        sample color config for demonstartion purpse only
" ==============================================================

" Name    Hex      Rgb                 Xterm
" ==========================================
" dark    #1F2D3A  rgb(31, 45, 58)     0
" yellow  #F39C12  rgb(243, 156, 18)   3
" blue    #2980B9  rgb(41, 128, 185)   4
" gray    #84888B  rgb(132, 136, 139)  7
" red     #E74C3C  rgb(231, 76, 60)    9
" white   #ECF0F1  rgb(236, 240, 241)  15

hi clear

if exists('syntax_on')
	syntax reset
endif

let colors_name = 'example'
set background=dark

if ($TERM =~ '256' || &t_Co >= 256) || has('gui_running')
	hi Normal     ctermfg=15   ctermbg=NONE guifg=#ECF0F1 guibg=#1F2D3A cterm=NONE      gui=NONE
	hi LineNr     ctermfg=7    ctermbg=NONE guifg=#84888B guibg=#1F2D3A cterm=NONE      gui=NONE
	hi Error      ctermfg=9    ctermbg=NONE guifg=#E74C3C guibg=NONE    cterm=reverse   gui=reverse
	hi Identifier ctermfg=4    ctermbg=NONE guifg=#2980B9 guibg=NONE    cterm=NONE      gui=NONE
	hi Ignore     ctermfg=NONE ctermbg=NONE guifg=NONE    guibg=NONE    cterm=NONE      gui=NONE
	hi Statement  ctermfg=3    ctermbg=NONE guifg=#F39C12 guibg=NONE    cterm=NONE      gui=NONE
endif

hi link Conditional Statement
hi link PreProc     Error
```

## Dependency
* python3
* pyyaml (python package)
``` bash
$ pip install pyyaml
```

## Installation
todo

## Options
generate colorscheme file from simple yaml color config

| option                       | default      |
| :--------------------------- | :-------     |
| `g:color_config_debug`       | `0`          |
| `g:color_config_output_path` | `'cwd'`      |
| `g:color_config_options`     | `['indent']` |

**Note**: `g:color_config_output_path` is absolute path or relative path to `getcwd()`

#### Example
``` vim
let g:color_config_debug = 1
let g:color_config_output_path = '$HOME/.vim/colors/'
let g:color_config_options = ['callgraph', 'no-overwrite']
```

## Commandline Usage
```bash
$ cd path/to/this/plugin
$ python plugin/color_config.py -h
usage: color_config.py [-h] [-d [DEST]] [-cg] [-i] [-now] filename

Generate vim colorscheme file from simplilfied yaml config file

positional arguments:
  filename              yaml file path to parse

optional arguments:
  -h, --help            show this help message and exit
  -d [DEST], --dest [DEST]
                        destination path for generated colorscheme file,
                        default is current directory
  -cg, --callgraph      generate functions callgraph
  -i, --indent          indent colorscheme file using vim editor
  -now, --no-overwrite  throw error if target file has already existed
```

**Note**: Your vim dont have to be compiled with python (+python) because
the source file `source/color_config.py` can act as a standalone command

## Related Works
* [colortemplate](https://github.com/lifepillar/vim-colortemplate) by [lifepillar](https://github.com/lifepillar)
* [rnb](https://gist.github.com/romainl/5cd2f4ec222805f49eca) by [romainl](https://github.com/romainl)
