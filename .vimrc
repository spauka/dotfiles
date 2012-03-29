set nocompatible

runtime ~/.vim/local.vim

" Load plugins
call pathogen#infect('bundle-enabled')

source ~/.vim/aliases.vim
source ~/.vim/keybindings.vim
source ~/.vim/behaviour.vim
source ~/.vim/interaction.vim
source ~/.vim/display.vim
