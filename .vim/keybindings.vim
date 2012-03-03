" map <up> <nop>
" map <down> <nop>
" map <left> <nop>
" map <right> <nop>

let mapleader = ","

noremap <silent> <Space> :silent noh<Bar>echo<CR>

cmap w!! w !sudo tee % >/dev/null

set pastetoggle=<F2>

" " Omnicomplete
" inoremap <expr> <CR> pumvisible() ? "\<C-y>" : "\<C-g>u\<CR>"
" inoremap <expr> <C-n> pumvisible() ? '<C-n>' :
"   \ '<C-n><C-r>=pumvisible() ? "\<lt>Down>" : ""<CR>'
" inoremap <expr> <M-,> pumvisible() ? '<C-n>' :
"   \ '<C-x><C-o><C-n><C-p><C-r>=pumvisible() ? "\<lt>Down>" : ""<CR>'

nnoremap <leader>r :RainbowParenthesesToggle<cr>

