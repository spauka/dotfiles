" Make backspace sensible
set backspace=indent,eol,start

" Make the autocompletion of filenames,etc behave like bash
set wildmode=longest,list

" Match search results as you type
set incsearch

" Ignore case when searching
set ignorecase

" Ignore the ignorecase character if search contains uppercase chars
set smartcase

" Mouse options
" we make it only available in insert mode, since in command mode there are
" much better ways of selecting text.
" also, for terminals which don't support shift-drag, this provides an easier
" way to copy-paste at terminal level rather than vim level
set mouse=vi
set mousehide

