if exists("did_load_filetypes")
    finish
endif

augroup filetypedetect
    " arduino
    au! BufRead,BufNewFile *.pde,*.ino setfiletype cpp
    " glsl
    au! BufRead,BufNewFile *.frag,*.vert,*.fp,*.vp,*.glsl setfiletype glsl
    " lilypond
    au! BufRead,BufNewFile *.ly setfiletype lilypond
    " mutt
    au! BufRead,BufNewFile mutt* setfiletype mail
    " text
    au! BufRead,BufNewFile *.txt setfiletype text
    " vala
    au! BufRead,BufNewFile *.vala,*.vapi setfiletype vala
    " cuda
    au BufNewFile,BufRead *.cu set ft=cu
augroup END
