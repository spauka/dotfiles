#!/usr/bin/env bash

# colored grep
export GREP_COLOR='1;33'

if [[ -f "$HOME/.dir_colors" ]]; then
    eval $(dircolors "$HOME/.dir_colors")
fi

# Load the theme
if [[ $BASH_IT_THEME ]]; then
    source "$BASH_IT/themes/$BASH_IT_THEME/$BASH_IT_THEME.theme.bash"
fi
