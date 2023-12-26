import requests
import json
from datetime import datetime
import os
import git

# リモートリポジトリの変更を検知し、変更があればWebhookUR(teams)に投稿をする処理

# ENV CONSTANTS
REPO_PATH = "" # Git repository path
WEBHOOK_URL = "" # Webhook URL
LAST_COMMIT_FILE = "" # 前回のリモート HEAD の位置を保存するファイルのパス
MAX_POST_SIZE = 10240 # teamsに投稿する変更履歴のバイト数 teamsに投稿できるのは26KBまで。推奨は10KB

# FUNCTIONS
def is_binary_string(bytes):
    """バイナリファイルかどうか"""
    return b'\0' in bytes

def truncate_message(message, max_size=MAX_POST_SIZE):
    """メッセージを指定された最大サイズに切り詰める"""
    if len(message.encode('utf-8')) > max_size:
        while len(message.encode('utf-8')) > max_size:
            message = message.rsplit('<br>', 2)[0] + '<br>'
        message = message + 'ファイル変更履歴の表示上限を超えました。直接確認ください<br>'
    return message

def custom_diff_format(diff_text):
    """各行を解析してカスタム形式に変換"""
    lines = diff_text.split('\n')
    new_lines = []
    for line in lines:
        if line.startswith('+'):
            new_line = f'<span style="color: red;">削変＞ {line[1:]}</span><br>'
        elif line.startswith('-'):
            new_line = f'<span style="color: green;">追加＞ {line[1:]}</span><br>'
        else:
            continue  # コンテキスト行は無視
        new_lines.append(new_line)
    return '\n'.join(new_lines)

# MAIN
def main():
    repo = git.Repo(REPO_PATH)
    origin = repo.remotes.origin
    origin.fetch()

    last_commit_id = None
    if os.path.exists(LAST_COMMIT_FILE):
        with open(LAST_COMMIT_FILE, 'r', encoding='utf-8') as file:
            last_commit_id = file.read().strip()
    
    remote_head = origin.refs.main.commit
    if last_commit_id:
        commits = list(repo.iter_commits(rev=f"{last_commit_id}~1..{remote_head.hexsha}", max_count=10))
    else:
        commits = [remote_head]
    print(commits)
    if not commits or (len(commits) == 1 and commits[0].hexsha == last_commit_id):
        print("新しいコミットはありません。")
    else:
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_text = f"投稿日時: {current_datetime}\n\n--------------------------------\n"
        message_text += f"<h1>変更ファイル一覧</h1>\n\n"
        # 最新のコミットのdiffを表示
        
        latest_diff = commits[0].diff('HEAD~1', create_patch=True)
        for diff_item in latest_diff:
            file_path = diff_item.a_path if diff_item.deleted_file else diff_item.b_path
            diff_text = custom_diff_format(diff_item.diff.decode('utf-8', errors='ignore'))
            
            if diff_item.renamed:
                    message_text += f"移動ファイル：{diff_item.a_path} が {diff_item.b_path} に移動されました<br>"
            elif diff_item.deleted_file: # deleted_fileとnew_fileの挙動がおかしい、逆にする
                message_text += f"**新規ファイル：{file_path}**\n\n"
                message_text += f"{diff_text}\n\n--------------------------------\n"
            else:
                if diff_item.new_file: # deleted_fileとnew_fileの挙動がおかしい、逆にする
                    message_text += f"**削除ファイル：{file_path}**\n\n"
                else:
                    message_text += f"**変更ファイル：{file_path}**\n\n"
                    message_text += f"{diff_text}\n\n--------------------------------\n"
        message_text = truncate_message(message_text)

        # 過去10回分のコミット情報を表示
        message_text += f"--------------------------------\n\n<h1>コミット履歴一覧</h1>\n\n"
        for commit in reversed(commits[:-1]):
            message_text += f"コミットID: {commit.hexsha}<br>"
            message_text += f"作者: {commit.author.name}<br>"
            message_text += f"日時: {datetime.fromtimestamp(commit.committed_date).strftime('%Y-%m-%d %H:%M:%S')}<br>"
            message_text += f"メッセージ: {commit.message}<br>"
            message_text += "--------------------------------<br>"

        json_data = {"text": message_text}
        requests.post(WEBHOOK_URL, headers={"Content-Type": "application/json"}, data=json.dumps(json_data))
        origin.pull()
        with open(LAST_COMMIT_FILE, 'w', encoding='utf-8') as file:
            file.write(commits[0].hexsha)
        

if __name__ == '__main__':
    main()