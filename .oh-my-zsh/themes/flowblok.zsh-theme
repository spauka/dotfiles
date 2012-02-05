# vim:ft=zsh

function battery_charge {
    battery-charge 2>/dev/null
}

function hg_prompt_info {
    hg prompt --angle-brackets "\
< %{$fg_bold[black]%}[hg]%{$reset_color%} on %{$fg_bold[blue]%}<branch>%{$reset_color%}>\
%{$fg_bold[red]%}<status|modified>%{$fg[magenta]%}<status|unknown>%{$fg[green]%}<update>%{$reset_color%}\
< at %{$fg_bold[magenta]%}<tags|%{$reset_color%}, %{$fg_bold[magenta]%}>%{$reset_color%}>\
" 2>/dev/null
}

function hg_prompt_patches {
    hg prompt --angle-brackets "
<patches: <patches|join( → )\
|pre_applied(%{$fg_bold[yellow]%})\
|post_applied(%{$reset_color%})\
|pre_unapplied(%{$fg_bold[black]%})\
|post_unapplied(%{$reset_color%})>>" 2>/dev/null
}

VIRTUAL_ENV_DISABLE_PROMPT=true
function virtualenv_info {
    [ $VIRTUAL_ENV ] && echo '('`basename $VIRTUAL_ENV`') '
}

local who='%{$fg[red]%}%n%{$reset_color%}@%{$fg[yellow]%}%m%{$reset_color%}'
local where='%{$fg_bold[green]%}${PWD/#$HOME/~}%{$reset_color%}'

local return_status="%{$fg_bold[red]%}%(?..↪ %?)%{$reset_color%}"

local insert_mode="%{$fg_bold[blue]%}\$%{$reset_color%}"
local command_mode="%{$fg_bold[magenta]%}\$%{$reset_color%}"
function vi_mode_prompt_info() {
    if [ "$KEYMAP" != "vicmd" ]; then
        echo $insert_mode
    else
        echo $command_mode
    fi
}

autoload -U add-zsh-hook
add-zsh-hook precmd vcs_info

PROMPT="$return_status
$who in $where"'$(hg_prompt_info)$(git_prompt_info)$(hg_prompt_patches)
$(virtualenv_info)$(vi_mode_prompt_info) '
RPROMPT='$(battery_charge)'

ZSH_THEME_GIT_PROMPT_PREFIX=" %{$fg_bold[black]%}[git]%{$reset_color%} on %{$fg_bold[blue]%}"
ZSH_THEME_GIT_PROMPT_SUFFIX="%{$reset_color%}"
ZSH_THEME_GIT_PROMPT_DIRTY="%{$fg_bold[red]%}!"
ZSH_THEME_GIT_PROMPT_UNTRACKED="%{$fg_bold[magenta]%}?"
ZSH_THEME_GIT_PROMPT_CLEAN=""

