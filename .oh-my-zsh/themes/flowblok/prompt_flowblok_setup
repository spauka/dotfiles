# Authors:
#   Peter Ward <peteraward@gmail.com>
#
# Screenshots:
#

function virtualenv_info() {
    if [[ -n "$VIRTUAL_ENV" ]]; then
        print "(%F{magenta}${VIRTUAL_ENV:t}%f)"
    fi
}

function prompt_flowblok_precmd() {
    if [[ -n "$__PROMPT_FLOWBLOK_VCS_UPDATE" ]] ; then
        # Check for untracked files or updated submodules since vcs_info doesn't.
        if [[ ! -z $(git ls-files --other --exclude-standard 2> /dev/null) ]]; then
            __PROMPT_FLOWBLOK_VCS_UPDATE=1
            fmt_branch="(%F{blue}%b%f%u%c%F{magenta}●%f)"
        else
            fmt_branch="(%F{blue}%b%f%u%c)"
        fi
        zstyle ':vcs_info:*:prompt:*' formats "${fmt_branch}"

        vcs_info 'prompt'
        __PROMPT_FLOWBLOK_VCS_UPDATE=''
    fi
}

function prompt_flowblok_preexec() {
    case "$(history $HISTCMD)" in
        (*(bzr|git|hg|svn)*)
            __PROMPT_FLOWBLOK_VCS_UPDATE=1
            ;;
        esac
}

function prompt_flowblok_chpwd() {
    __PROMPT_FLOWBLOK_VCS_UPDATE=1
}

function prompt_flowblok_setup() {
    setopt LOCAL_OPTIONS
    unsetopt XTRACE KSH_ARRAYS
    prompt_opts=(cr percent subst)

    autoload -Uz add-zsh-hook
    autoload -Uz vcs_info

    add-zsh-hook precmd prompt_flowblok_precmd
    add-zsh-hook preexec prompt_flowblok_preexec
    add-zsh-hook chpwd prompt_flowblok_chpwd

    __PROMPT_FLOWBLOK_VCS_UPDATE=1

    # Enable VCS systems you use.
    zstyle ':vcs_info:*' enable bzr git hg svn

    # check-for-changes can be really slow.
    # You should disable it if you work with large repositories.
    zstyle ':vcs_info:*:prompt:*' check-for-changes true

    # Formats:
    # %b - branchname
    # %u - unstagedstr (see below)
    # %c - stagedstr (see below)
    # %a - action (e.g. rebase-i)
    # %R - repository path
    # %S - path in the repository
    local fmt_branch="(%F{cyan}%b%f%u%c)"
    local fmt_action="(%F{green}%a%f)"
    local fmt_unstaged="%F{red}●%f"
    local fmt_staged="%F{yellow}●%f"

    zstyle ':vcs_info:*:prompt:*' unstagedstr   "${fmt_unstaged}"
    zstyle ':vcs_info:*:prompt:*' stagedstr     "${fmt_staged}"
    zstyle ':vcs_info:*:prompt:*' actionformats "${fmt_branch}${fmt_action}"
    zstyle ':vcs_info:*:prompt:*' formats       "${fmt_branch}"
    zstyle ':vcs_info:*:prompt:*' nvcsformats   ""

    local who='%F{red}%n%f@%F{yellow}%m%f'
    local where='%B%F{green}${PWD/#$HOME/~}%f%b'

    zstyle ':omz:completion' indicator '%B%F{red}...%f%b'
 #   zstyle ':omz:prompt' vicmd '%F{yellow}❮%f%B%F{red}❮%f%b%F{red}❮%f'

    VIRTUAL_ENV_DISABLE_PROMPT=true
    PROMPT="
$who in $where "'${vcs_info_msg_0_}'"
"'$(virtualenv_info)'"$ "
#  PROMPT='%F{cyan}%1~%f${git_prompt_info} %(!.%B%F{red}#%f%b.%B%F{green}❯%f%b) '
    RPROMPT='%(?::%B%F{red}$? ↩%f%b)${VIM:+" %B%F{green}V%f%b"}'
    SPROMPT='zsh: correct %F{red}%R%f to %F{green}%r%f [nyae]? '
}

prompt_flowblok_setup "$@"

