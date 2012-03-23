set_xterm_title () {
    local title="$1"
    printf '\e]0;%s\007' "$title"
}

precmd () {
    set_xterm_title "${USER}@${HOSTNAME} `dirs -0` $PROMPTCHAR"
}

preexec () {
    set_xterm_title "$1 {`dirs -0`} (${USER}@${HOSTNAME})"
}

preexec_install
