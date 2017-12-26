" ============================================================================
" File:        color_config.vim
" Description: commands to call public functions in autoload/
" Author:      Near Huscarl <near.huscarl@gmail.com>
" Last Change: Wed Dec 27 01:51:00 +07 2017
" Licence:     BSD 3-Clause license
" Note:        nah
" ============================================================================

" {{{ init
if !executable('python3')
	finish
endif

let g:loaded_color_config = 1
" }}}
" {{{ commands
command! -nargs=0 ColorConfigGenerate        call color_config#generate()
command! -nargs=0 ColorConfigGenerateVerbose call color_config#generate_verbose()
command! -nargs=0 ColorConfigInfo            call color_config#print_info()
command! -nargs=0 ColorConfigResetDefault    call color_config#reset_default()
" }}}
