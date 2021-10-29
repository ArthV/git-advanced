# Git advanced workshop

## Requirements:

git cli ~2.30.1 
python ~3.8.10

## Useful git commands

Before to start, let me introduce you several useful commands that you'll need to use to understand the actions you'll perform.

```bash

git log  # Display the git history of your current branch

git log --pretty=oneline --graph --decorate --all # Display the git history of our repository using graphs 

git help # Display every command available with git

git <command> --help # Display complete documentation about a command and provide example

```

### resource

https://learngitbranching.js.org to learn interactively how to use complex git concept. 

## 1/ Merge with a strategy 

In this exercice there is two branch, merge-strategy and merge-branch

In this two there is one file called my_files which has different content in each branch.

### Strategy ours

To start, go to the branch merge-strategy 

```
git checkout merge-strategy
```

Create a new branch from merge-strategy

```
git checkout -b merge-strategy-ours 
```

Then merge the branch merge-branch using the strategy ours

```
git merge -X ours merge-branch
```

then look at the file.

### Strategy theirs

Go back the to the branch merge-strategy

and then create a new branch from merge-strategy

```
git checkout -b merge-strategy-theirs
```

Then merge the branch merge-branch using the strategy theirs

```
git merge -X theirs merge-branch
```

then look at the file.


## 2/ Complexe rebase through multiple branches

move to the branch bug fix 
```
git checkout bug-fix
```

and use the command to display the git history 

Then use this command to rebase the bug-fix onto master
```
git rebase --onto master dev bug-fix
```

have a look again at you git history to understand what happened

## 3/ Cherry pick a useful commit 

```
git checkout dev
```

Now wwe want to apply our bug fix commit to our dev branch, then will find the sha of the commit using git log and cherry-pick it to the dev branch using the new command

```
git cherry-pick #replace-commit-sha
```

## 4/ Bisect with a script 

Go to the bisect-branch
```
git checkout bisect-branch
```

We start a bisect session in the CLI
```
git bisect start
```

We define the HEAD of the current branch as bad commit
```
git bisect bad
```

We choose among the other commits a one where the error isn't raised
```
git bisect good <commit-sha>
```

Run the command and see what happened ;) 

```
git bisect run python manage.py test
```