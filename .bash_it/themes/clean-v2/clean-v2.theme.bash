# git theming
ZSH_THEME_GIT_PROMPT_PREFIX="${bold_blue}(${yellow}%B"
ZSH_THEME_GIT_PROMPT_SUFFIX="%b${bold_blue})${reset_color} "
ZSH_THEME_GIT_PROMPT_CLEAN=""
ZSH_THEME_GIT_PROMPT_DIRTY="${bold_red}✗"

function prompt_command() {

    if [ "$(whoami)" = root ]; then no_color=$bold_red; else no_color=$bold_green; fi

    PS1="${no_color}\u@\h${reset_color}:${cyan}\w/${reset_color} $ "
    RPROMPT='[\t]'
}

PROMPT_COMMAND=prompt_command;
