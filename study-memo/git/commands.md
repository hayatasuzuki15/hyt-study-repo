# Git commands

## Clone the git repository

```sh
git clone <repository name>
```

Copying files from a remote repository to a working tree

Copy the .git directory

## Add changes to stage

```sh
git add <file name>
git add <directory name>
git add .
```

You can make any changes you want to add to the stage.

## Record changes

```sh
git commit
git commit -m "<message>"
git commit -v
```

You should write the message in plain language.

## 現在の変更状況を確認する

```sh
git status
```

リポジトリとステージの間と、ステージとワークツリーとの間の変更を確認できる

## 変更差分を確認

```sh
# git addする前の変更分
git diff
git diff <file name>
#git addした後の変更分
git diff --staged
```

## 変更履歴を確認

```sh
git log
# 一行表示
git log --oneline
# ファイルの変更差分を表示
git log -p <file name>
#表示するコミット数を制限する
git log -n
```

## ファイルの削除
```sh
git rm <file name>
git rm -r <direntory name>
git rm cached <file name> #リポジトリからだけ削除したい場合
```

## ファイルの移動を記録
```sh
git mv <old> <new>
# same command
mv <old> <new>
git rm <old>
git add <new>
```

## リモートリポジトリを追加する
```sh
git remote add origin <url>
```

## Other commands
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
