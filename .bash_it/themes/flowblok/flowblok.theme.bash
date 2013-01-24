#!/bin/bash 

# Adapted from flowblok, to fit my zsh theme.

# ----------------------------------------------------------------- COLOR CONF
D_DEFAULT_COLOR="${normal}"
D_INTERMEDIATE_COLOR="${normal}"
D_USER_COLOR="${red}"
D_SUPERUSER_COLOR="${red}"
D_MACHINE_COLOR="${yellow}"
D_DIR_COLOR="${bold_green}"
D_SCM_COLOR="${yellow}"
D_BRANCH_COLOR="${yellow}"
D_CHANGES_COLOR="${white}"
D_CMDFAIL_COLOR="${red}"
D_VIMSHELL_COLOR="${cyan}"

# ------------------------------------------------------------------ FUNCTIONS
case $TERM in
  xterm*)
      TITLEBAR="\033]0;\w\007"
      ;;
  *)
      TITLEBAR=""
      ;;
esac

is_vim_shell() {
  if [ ! -z "$VIMRUNTIME" ];
  then
    echo "${D_INTERMEDIATE_COLOR}on ${D_VIMSHELL_COLOR}\
vim shell${D_DEFAULT_COLOR} "
  fi
}

mitsuhikos_lastcommandfailed() {
  code=$?
  if [ $code != 0 ];
  then
    echo "${D_INTERMEDIATE_COLOR}exited ${D_CMDFAIL_COLOR}\
$code ${D_DEFAULT_COLOR}" 
  fi
}

# vcprompt for scm instead of bash_it default
flowblok_vcprompt() {
  if [ ! -z "$VCPROMPT_EXECUTABLE" ];
  then
    local D_VCPROMPT_FORMAT="on ${D_SCM_COLOR}%s${D_INTERMEDIATE_COLOR}:\
${D_BRANCH_COLOR}%b %r ${D_CHANGES_COLOR}%m%u ${D_DEFAULT_COLOR}"
    $VCPROMPT_EXECUTABLE -f "$D_VCPROMPT_FORMAT"  
  fi
}

# -------------------------------------------------------------- PROMPT OUTPUT
prompt() {
  local SAVE_CURSOR='$(tput sc)'
  local RESTORE_CURSOR='$(tput rc)'
  local MOVE_CURSOR_RIGHTMOST='$(tput hpa `tput cols`)'
  local MOVE_CURSOR_5_LEFT='$(tput cub 5)'

  if [ $(uname) = "Linux" ];
  then
    PS1="${TITLEBAR}
${SAVE_CURSOR}${MOVE_CURSOR_RIGHTMOST}${MOVE_CURSOR_5_LEFT}\
$(battery_charge)${RESTORE_CURSOR}\
${D_USER_COLOR}\u${D_INTERMEDIATE_COLOR}\
@${D_MACHINE_COLOR}\h ${D_INTERMEDIATE_COLOR}\
in ${D_DIR_COLOR}\w ${D_INTERMEDIATE_COLOR}\
$(mitsuhikos_lastcommandfailed)\
$(flowblok_vcprompt)\
$(is_vim_shell)
${D_INTERMEDIATE_COLOR}$ ${D_DEFAULT_COLOR}"
  else
    PS1="${TITLEBAR}
${D_USER_COLOR}\u ${D_INTERMEDIATE_COLOR}\
at ${D_MACHINE_COLOR}\h ${D_INTERMEDIATE_COLOR}\
in ${D_DIR_COLOR}\w ${D_INTERMEDIATE_COLOR}\
$(mitsuhikos_lastcommandfailed)\
$(flowblok_vcprompt)\
$(is_vim_shell)\
$(battery_charge)
${D_INTERMEDIATE_COLOR}$ ${D_DEFAULT_COLOR}"
  fi

  PS2="${D_INTERMEDIATE_COLOR}$ ${D_DEFAULT_COLOR}"
}

# Runs prompt (this bypasses bash_it $PROMPT setting)
PROMPT_COMMAND=prompt

