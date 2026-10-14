"""Publica a árvore estática em gh-pages sem worktree ou alteração do checkout."""
import subprocess

def git(*args,**kwargs):
    return subprocess.check_output(['git',*args],text=True,**kwargs).strip()

tree=git('rev-parse','HEAD:web/decisoes')
remote=git('ls-remote','origin','refs/heads/gh-pages')
parent=None
if remote:
    parent=remote.split()[0]
    git('fetch','origin','gh-pages')
    if git('rev-parse',parent+'^{tree}')==tree:
        print('Painel já publicado com a mesma árvore de arquivos.')
        raise SystemExit(0)
args=['commit-tree',tree,'-m','deploy: publica painel de decisoes']
if parent:args.extend(['-p',parent])
commit=git(*args)
git('push','origin',commit+':refs/heads/gh-pages')
print('Árvore estática enviada para gh-pages:',commit)
