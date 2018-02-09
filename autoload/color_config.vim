" ============================================================================
" File:        color_config.vim
" Description: util functions and settings to wrap into a plugin
" Author:      Near Huscarl <near.huscarl@gmail.com>
" Last Change: Thu Dec 28 03:13:25 +07 2017
" Licence:     BSD 3-Clause license
" Note:        nah
" ============================================================================

" {{{ global
let s:plugin_path = expand('<sfile>:p:h')
let s:executable_path = simplify(s:plugin_path . '/../src/color_config.py')
let s:has_python3 = executable('python3') ? 'True' : 'False'

call system("python -c 'import yaml'")
let s:has_pyyaml = v:shell_error ? 'False' : 'True'
let s:default_output = 'cwd'
let s:default_options = ['indent']
let s:default_debug_option = 0
" }}}
" {{{ options
if !exists('g:color_config_output_path')
	let g:color_config_output_path = s:default_output
endif
if !exists('g:color_config_options')
	let g:color_config_options = s:default_options
endif
if !exists('g:color_config_debug')
	let g:color_config_debug = s:default_debug_option
endif
" }}}
function! s:get_options() " {{{
	let options = ''
	for option in g:color_config_options
		let options .= '--' . option . ' '
	endfor
	return options
endfunction
" }}}
function! s:echo_hl(msg, hl_group) " {{{
	execute 'echohl ' . a:hl_group
	echomsg a:msg
	echohl None
endfunction
" }}}
function! s:print(content) " {{{
	call append('$', a:content)
endfunction
" }}}
function! s:print_command(command) " {{{
	call setline(1, 'Command:  ' . a:command)
endfunction
" }}}
function! s:print_variables() " {{{
	call s:print('Dependencies:')
	call s:print('s:has_python3: ' . s:has_python3)
	call s:print('s:has_pyyaml: ' . s:has_pyyaml)
	call s:print('')
	call s:print('Options:')
	call s:print('s:plugin_path: ' . shellescape(s:plugin_path))
	call s:print('s:executable_path: ' . shellescape(s:executable_path))
	call s:print('g:color_config_output_path: ' . shellescape(g:color_config_output_path))
	call s:print('g:color_config_options: ' . string(g:color_config_options))
	call s:print('g:color_config_debug: ' . g:color_config_debug)
	call s:print('')
endfunction
" }}})
function! s:print_debug_info() " {{{
	call s:print('')
	call s:print('Source: ' . s:cmd)
	call s:print('Input: ' . s:input)
	call s:print('Dest: ' . s:dest)
	call s:print('Parameters: ' . substitute(s:options, '\s$', '', ''))
	call s:print('')
	call s:print_variables()
endfunction
" }}}
function! s:open_status_win(title) " {{{
	" reuse window if already exists
	let winnr = bufwinnr('^' . a:title . '$')
	let split_win = 'silent botright new ' . a:title
	execute winnr < 0 ? split_win : winnr . 'wincmd w | q | ' . split_win
	setlocal buftype=nofile bufhidden=wipe nobuflisted noswapfile filetype=yaml
	nnoremap <silent> <buffer> q :q<CR>
endfunction
" }}}
function! s:reset_win_height(max_height) " {{{
	let height = line('$') <= a:max_height ? line('$') : a:max_height
	execute 'resize ' . height
endfunction
" }}}
function! s:execute_and_print_output(cmd) " {{{
	call s:print('')
	call s:print('Command Output:')
	silent execute '$read !'. a:cmd
endfunction
" }}}
function! s:run_shell_cmd(command) " {{{
	" execute shell command, if fails, show error in new window
   let b:win_info = winsaveview()
	call s:open_status_win('Error')
	call s:print_command(a:command)
	call s:execute_and_print_output(a:command)

	if v:shell_error != 0 || g:color_config_debug
		call s:print_debug_info()
		setlocal nomodifiable
		normal! gg
		call s:reset_win_height(20)
	else
		quit
		call winrestview(b:win_info)
	endif
endfunction
" }}}
function! s:get_dest() " {{{
	if g:color_config_output_path ==? 'cwd'
		return shellescape(expand('%:p:h'), 1)
	endif
	return shellescape(expand(g:color_config_output_path), 1)
endfunction
" }}}
function! color_config#generate() " {{{
	let s:cmd = shellescape(s:executable_path, 1)
	let s:input = shellescape(expand('%:p'), 1)
	let s:dest = s:get_dest()
	let s:options = s:get_options()
	call s:run_shell_cmd(s:cmd . ' -d ' . s:dest . ' ' . s:options . s:input)
endfunction
" }}}
function! color_config#generate_verbose() " {{{
	let old_debug_option = g:color_config_debug
	let g:color_config_debug = 1
	call color_config#generate()
	let g:color_config_debug = old_debug_option
endfunction
" }}}
function! color_config#print_info() " {{{
	call s:open_status_win('Info')
	call s:print_variables()
	setlocal nomodifiable
	call s:reset_win_height(20)
endfunction
" }}}
function! color_config#reset_default() " {{{
	let g:color_config_output_path = s:default_output
	let g:color_config_options = s:default_options
	let g:color_config_debug = s:default_debug_option
	call s:echo_hl('Options have been reset to default.', 'String')
endfunction
" }}}
