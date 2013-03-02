" Enable syntax highlighting
syntax on

" Choose color scheme
if &t_Co >= 256
    colorscheme inkpot
else
    colorscheme default
endif

" Show the line/column positions at the bottom
set ruler

" Display as much as possible of the last line of text
" (instead of displaying an @ character)
set display+=lastline

" Show line numbers on the side
set number

" Display current mode and partially typed commands
set showmode
set showcmd

" Show the filename title in xterms
set title

" Allow splits to have 0 height (use C-W _)
set wmh=0

" Always keep a few lines of context around the cursor
set scrolloff=3

" Highlight search terms (cancel with space)
set hlsearch

" Show whitespace
set list
set listchars=tab:>.,trail:.,extends:#,nbsp:.

au Syntax * :RainbowParenthesesLoadRound
au Syntax * :RainbowParenthesesLoadSquare
au Syntax * :RainbowParenthesesLoadBraces
let g:rbpt_colorpairs = [
    \ ['brown',       'RoyalBlue3'],
    \ ['Darkblue',    'SeaGreen3'],
    \ ['darkgray',    'DarkOrchid3'],
    \ ['darkgreen',   'firebrick3'],
    \ ['darkcyan',    'RoyalBlue3'],
    \ ['darkred',     'SeaGreen3'],
    \ ['darkmagenta', 'DarkOrchid3'],
    \ ['brown',       'firebrick3'],
    \ ['gray',        'RoyalBlue3'],
    \ ['black',       'SeaGreen3'],
    \ ['darkmagenta', 'DarkOrchid3'],
    \ ['Darkblue',    'firebrick3'],
    \ ['darkgreen',   'RoyalBlue3'],
    \ ['darkcyan',    'SeaGreen3'],
    \ ['darkred',     'DarkOrchid3'],
    \ ['red',         'firebrick3'],
\ ]

