" Enable filetype specific rules
filetype plugin indent on

" Pay attention to modelines in files.
set modeline

" Create backup files.
set backup
" Create the backup dir if it doesn't exist
if has("unix")
    if !isdirectory(expand("~/.tmp/vimbak/."))
        !mkdir -p ~/.tmp/vimbak
    endif
    set backupdir=~/.tmp/vimbak,.
    set directory=~/.tmp/vimbak,.
endif

" Remember previously used commands.
set history=100

" Default indentation settings
" NOTE: these may be overridden for specific filetypes

set expandtab

set tabstop=4
set softtabstop=4
set shiftwidth=4

set autoindent
set copyindent

" Omnicomplete
set ofu=syntaxcomplete#Complete
set completeopt=longest,menuone

" TeX highlighting
let g:tex_flavor = "latex"

" Syntastic
let g:syntastic_check_on_open = 1
let g:syntastic_enable_balloons = 1

" Vala
let vala_space_errors = 1
autocmd BufRead *.vala,*.vapi set efm=%f:%l.%c-%[%^:]%#:\ %t%[%^:]%#:\ %m

" Slime
let g:slime_target = "tmux"
