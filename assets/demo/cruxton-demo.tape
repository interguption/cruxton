Output assets/demo/cruxton-demo.gif
Output assets/demo/cruxton-demo.mp4

Require rg

Set Shell "bash"
Set FontSize 20
Set Width 1200
Set Height 700
Set LineHeight 1.25
Set TypingSpeed 18ms
Set Theme "GitHub Dark"

Hide
Type "export PS1='$ '; clear"
Enter
Show

Type "# Agent: move reports/ to decisions/ for a cleaner tree"
Enter
Sleep 1s

Type "rg -l 'move to a .*decisions/.* directory was rejected' reports/DEC-*.md"
Enter
Sleep 1s

Type "rg '^decision:|^human_crux:' reports/DEC-records-stay-put.md | cut -c 1-190 | fold -sw 88"
Enter
Sleep 4s

Type "# Agent: settled decision found — keeping reports/ in place"
Enter
Sleep 3s
