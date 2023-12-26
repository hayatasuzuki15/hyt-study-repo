# Git commands

## Clone the git repository

```
git clone <repository name>
```

Copying files from a remote repository to a working tree

Copy the .git directory

## Add changes to stage

```
git add <file name>
git add <directory name>
git add .
```

You can make any changes you want to add to the stage.

## 登録系

```
git config --global user.name "Githubで登録したユーザ名"
git config --global user.email github@example.com
git config --global core.editor "使うエディター"
```

## fileのハッシュIDを表示します

```
git hash-object file
```

## master ブランチ上での最後のコミットが指しているツリーファイルの中身を表示しま

```
git cat-file -p master^{tree}
```
