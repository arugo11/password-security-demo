import hashlib
import time
import random
import string
import itertools

# ユーザデータを保存する辞書
users = {}

def generate_salt(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def hash_password(password, salt=None):
    if salt is None:
        salt = generate_salt()
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}${hashed}"

def verify_password(stored_password, provided_password):
    salt, hashed = stored_password.split('$')
    return stored_password == hash_password(provided_password, salt)

def register_user(username, password):
    if username in users:
        return False
    hashed_password = hash_password(password)
    users[username] = hashed_password
    return True

def authenticate_user(username, password):
    if username not in users:
        return False
    return verify_password(users[username], password)

def list_users():
    return list(users.keys())

def display_hashed_passwords():
    print("\n=== ハッシュ化されたパスワード ===")
    for username, hashed_password in users.items():
        salt, hash_value = hashed_password.split('$')
        print(f"ユーザー名: {username}")
        print(f"  ソルト: {salt}")
        print(f"  ハッシュ値: {hash_value}")
        print()

def crack_password(username):
    if username not in users:
        return None, 0
    
    stored_password = users[username]
    salt, _ = stored_password.split('$')
    
    charset = string.ascii_lowercase + string.digits + string.ascii_uppercase + string.punctuation
    
    start_time = time.time()
    attempts = 0
    
    for length in range(1, 20):  # 20文字までのパスワードを試行
        print(f"\n{length}文字のパスワードを試行中...")
        for attempt in itertools.product(charset, repeat=length):
            current_time = time.time()
            if current_time - start_time > 30:  # 30秒を超えたら終了
                return None, 30
            
            password_attempt = ''.join(attempt)
            attempts += 1
            
            if attempts % 10000 == 0:  # 10000回試行ごとに進捗を表示
                print(f"試行回数: {attempts}, 経過時間: {current_time - start_time:.2f}秒")
                print(f"現在の試行: {password_attempt}")
            
            if verify_password(stored_password, password_attempt):
                end_time = time.time()
                return password_attempt, end_time - start_time
    
    return None, 30  # 30秒以内にクラックできなかった場合

def main():
    while True:
        print("\n1. ユーザ登録\n2. ログイン\n3. ユーザ一覧\n4. クラッキング\n5. ハッシュ表示\n6. 終了")
        choice = input("選択してください: ")

        if choice == '1':
            username = input("ユーザ名を入力: ")
            password = input("パスワードを入力: ")
            if register_user(username, password):
                print("ユーザが正常に登録されました！")
            else:
                print("ユーザ名が既に存在します！")

        elif choice == '2':
            username = input("ユーザ名を入力: ")
            password = input("パスワードを入力: ")
            if authenticate_user(username, password):
                print("ログイン成功！")
            else:
                print("無効なユーザ名またはパスワードです！")

        elif choice == '3':
            print("登録済みユーザ:", list_users())

        elif choice == '4':
            username = input("クラックするユーザ名を入力: ")
            print("クラッキングを開始します...")
            result, time_taken = crack_password(username)
            if result:
                print(f"パスワードがクラックされました: {result}, 所要時間: {time_taken:.2f}秒")
            else:
                print(f"クラッキング失敗, 所要時間: {time_taken:.2f}秒")

        elif choice == '5':
            display_hashed_passwords()

        elif choice == '6':
            print("終了します...")
            break

        else:
            print("無効な選択です。もう一度お試しください。")

if __name__ == "__main__":
    main()
