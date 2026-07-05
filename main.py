import os
import sys
import pickle
import random
import time
import threading
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

COMMENTS = [
    "🔥", "❤️", "👏", "💪", "😍", "🥰", "🔥🔥🔥",
    "класс", "супер", "огонь", "круто", "топ", "вау",
    "кайф", "бомба", "имба", "отлично", "зачет", "кайфово",
    "поддерживаю", "полностью согласен", "так и есть", "правда",
    "а где такое купить?", "как называется?", "это реально?",
    "а можно подробнее?", "лучшее что я видел сегодня",
    "это шедевр", "гениально", "талант", "в тему", "точняк",
    "🔥🔥 огонь", "❤️❤️ класс", "💯 топчик", "👍 хорошо",
    "норм", "классно", "суперски", "красота", "шикарно"
]

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def logo():
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ███████╗████████╗ ██████╗ ███╗   ██╗ █████╗ ██████╗ ██╗║
║   ██╔════╝╚══██╔══╝██╔═══██╗████╗  ██║██╔══██╗██╔══██╗██║║
║   █████╗     ██║   ██║   ██║██╔██╗ ██║███████║██████╔╝██║║
║   ██╔══╝     ██║   ██║   ██║██║╚██╗██║██╔══██║██╔═══╝ ██║║
║   ██║        ██║   ╚██████╔╝██║ ╚████║██║  ██║██║     ██║║
║   ╚═╝        ╚═╝    ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝║
║                                                           ║
║   ███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗ ║
║   ██╔════╝██║   ██║██╔════╝╚══██╔══╝██╔════╝████╗ ████║ ║
║   █████╗  ██║   ██║███████╗   ██║   █████╗  ██╔████╔██║ ║
║   ██╔══╝  ██║   ██║╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║ ║
║   ██║     ╚██████╔╝███████║   ██║   ███████╗██║ ╚═╝ ██║ ║
║   ╚═╝      ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝ ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
                TIKTOK WARMER PRO v2.0 | ETONAPY
    """)


class TikTokWarmer:
    def __init__(self, email, password, proxy=None, login_type="email", day=1):
        self.email = email
        self.password = password
        self.proxy = proxy
        self.login_type = login_type
        self.driver = None
        self.wait = None
        self.running = False
        self.day = day
        self.videos_posted = 0
        self.video_folder = "videos"

    def log(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {msg}")

    def random_sleep(self, min_sec, max_sec):
        time.sleep(random.uniform(min_sec, max_sec))

    def setup_driver(self):
        options = uc.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        if self.proxy:
            options.add_argument(f'--proxy-server={self.proxy}')
        self.driver = uc.Chrome(options=options, version_main=120)
        self.wait = WebDriverWait(self.driver, 20)

    def save_session(self, day):
        try:
            if self.driver:
                cookies = self.driver.get_cookies()
                data = {"cookies": cookies, "day": day, "email": self.email}
                with open(f"session_{self.email}.pkl", "wb") as f:
                    pickle.dump(data, f)
                self.log(f"💾 Сессия сохранена (День {day})")
        except Exception as e:
            self.log(f"⚠️ Ошибка сохранения сессии: {e}")

    def load_session(self):
        try:
            session_file = f"session_{self.email}.pkl"
            if os.path.exists(session_file):
                with open(session_file, "rb") as f:
                    data = pickle.load(f)
                    cookies = data.get("cookies", [])
                    for cookie in cookies:
                        try:
                            self.driver.add_cookie(cookie)
                        except:
                            pass
                    self.day = data.get("day", self.day)
                    self.log(f"📂 Сессия загружена (День {self.day})")
                    return True
            return False
        except Exception as e:
            self.log(f"⚠️ Ошибка загрузки сессии: {e}")
            return False

    def login(self):
        try:
            self.log(f"🔐 Вход в TikTok через {self.login_type}...")
            self.driver.get("https://www.tiktok.com/login")
            self.random_sleep(3, 5)

            if self.login_type == "google":
                google_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Google')]")))
                google_btn.click()
                self.random_sleep(2, 3)
                email_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
                email_input.send_keys(self.email)
                self.random_sleep(1, 2)
                next_btn = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Далее')]")
                next_btn.click()
                self.random_sleep(2, 3)
                pass_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
                pass_input.send_keys(self.password)
                self.random_sleep(1, 2)
                next_btn = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Далее')]")
                next_btn.click()
                self.random_sleep(3, 5)

            elif self.login_type == "facebook":
                fb_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Facebook')]")))
                fb_btn.click()
                self.random_sleep(2, 3)
                email_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='email']")))
                email_input.send_keys(self.email)
                self.random_sleep(1, 2)
                pass_input = self.driver.find_element(By.XPATH, "//input[@id='pass']")
                pass_input.send_keys(self.password)
                self.random_sleep(1, 2)
                login_btn = self.driver.find_element(By.XPATH, "//button[@name='login']")
                login_btn.click()
                self.random_sleep(3, 5)

            else:
                try:
                    email_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Use email')]")))
                    email_tab.click()
                    self.random_sleep(1, 2)
                except:
                    pass
                email_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email']")))
                email_input.clear()
                email_input.send_keys(self.email)
                self.random_sleep(1, 2)
                pass_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Password']")
                pass_input.clear()
                pass_input.send_keys(self.password)
                self.random_sleep(1, 2)
                login_btn = self.driver.find_element(By.XPATH, "//button[contains(@class, 'login-button')]")
                login_btn.click()
                self.random_sleep(5, 10)

            self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'feed')]")))
            self.log("✅ Успешный вход!")
            return True
        except Exception as e:
            self.log(f"❌ Ошибка входа: {e}")
            return False

    def watch_feed(self, minutes, day):
        likes = 0
        comments_count = 0
        videos_watched = 0
        start = time.time()
        end = start + (minutes * 60)

        self.log(f"📺 Просмотр ленты: {minutes} минут")
        while time.time() < end and self.running:
            try:
                videos = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'video-feed')]//div[contains(@class, 'video-container')]")
                if not videos:
                    self.random_sleep(2, 3)
                    continue

                for video in videos[:3]:
                    if time.time() >= end or not self.running:
                        break

                    videos_watched += 1
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", video)
                    self.random_sleep(2, 4)

                    if videos_watched % random.randint(3, 5) == 0 and likes < 20:
                        try:
                            like_btn = video.find_element(By.XPATH, ".//button[contains(@class, 'like')]")
                            if "liked" not in like_btn.get_attribute("class"):
                                like_btn.click()
                                likes += 1
                                self.log(f"❤️ Лайк #{likes}")
                                self.random_sleep(2, 5)
                        except:
                            pass

                    if videos_watched % random.randint(5, 7) == 0 and comments_count < 5:
                        try:
                            comment_btn = video.find_element(By.XPATH, ".//button[contains(@class, 'comment')]")
                            comment_btn.click()
                            self.random_sleep(2, 3)

                            comment_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Add a comment...']")))
                            comment_text = random.choice(COMMENTS)
                            comment_input.send_keys(comment_text)
                            self.random_sleep(1, 2)

                            send_btn = self.driver.find_element(By.XPATH, "//button[contains(@class, 'send')]")
                            send_btn.click()
                            comments_count += 1
                            self.log(f"💬 Комментарий: {comment_text}")
                            self.random_sleep(5, 10)

                            close_btn = self.driver.find_element(By.XPATH, "//button[contains(@class, 'close')]")
                            close_btn.click()
                        except:
                            pass

                    self.random_sleep(5, 15)
            except Exception as e:
                self.log(f"⚠️ Ошибка просмотра: {e}")
                self.random_sleep(5, 10)

        self.log(f"📊 Итог: {likes} лайков, {comments_count} комментариев")

    def fill_profile(self):
        try:
            self.log("✏️ Заполнение профиля...")
            profile_btn = self.driver.find_element(By.XPATH, "//a[contains(@href, '/@')]")
            profile_btn.click()
            self.random_sleep(3, 5)

            edit_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Edit profile')]")))
            edit_btn.click()
            self.random_sleep(2, 3)

            name_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Name']")
            name_input.clear()
            name_input.send_keys(f"User_{random.randint(100, 999)}")
            self.random_sleep(1, 2)

            bio_input = self.driver.find_element(By.XPATH, "//textarea[@placeholder='Bio']")
            bio_input.clear()
            bio_input.send_keys(random.choice(["Life is good ✨", "Just vibing 🌊", "Dream big 💫", "Stay positive 🌟"]))
            self.random_sleep(1, 2)

            save_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Save')]")
            save_btn.click()
            self.random_sleep(3, 5)
            self.log("✅ Профиль заполнен!")
        except Exception as e:
            self.log(f"❌ Ошибка профиля: {e}")

    def post_video(self):
        try:
            self.log("📹 Публикация видео...")
            if not os.path.exists(self.video_folder):
                os.makedirs(self.video_folder)
                self.log(f"📁 Создана папка {self.video_folder}")

            videos = [f for f in os.listdir(self.video_folder) if f.endswith(('.mp4', '.mov', '.avi'))]
            if not videos:
                self.log(f"⚠️ Нет видео в папке '{self.video_folder}'")
                return False

            video_path = os.path.join(self.video_folder, random.choice(videos))

            plus_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/upload')]")))
            plus_btn.click()
            self.random_sleep(2, 3)

            upload_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            upload_input.send_keys(os.path.abspath(video_path))
            self.random_sleep(10, 15)

            next_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]")))
            next_btn.click()
            self.random_sleep(3, 5)

            desc_input = self.driver.find_element(By.XPATH, "//textarea[@placeholder='Describe your video...']")
            desc_input.send_keys(f"#{random.choice(['топ', 'круто', 'огонь', 'жизнь', 'день', 'fun', 'vibe'])}")
            self.random_sleep(2, 3)

            post_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Post')]")))
            post_btn.click()
            self.random_sleep(5, 10)

            self.videos_posted += 1
            self.log("✅ Видео опубликовано!")
            return True
        except Exception as e:
            self.log(f"❌ Ошибка публикации: {e}")
            return False

    def reply_comments(self):
        try:
            self.log("💬 Ответы на комментарии...")
            notif_btn = self.driver.find_element(By.XPATH, "//a[contains(@href, '/notifications')]")
            notif_btn.click()
            self.random_sleep(3, 5)

            comments = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'notification')]//span[contains(text(), 'commented')]")
            for i, comment in enumerate(comments[:3]):
                try:
                    comment.click()
                    self.random_sleep(2, 3)

                    reply_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Add a reply...']")))
                    reply_input.send_keys(random.choice(["Спасибо!", "👍", "🔥", "❤️", "Согласен!", "Круто!"]))
                    self.random_sleep(1, 2)

                    send_btn = self.driver.find_element(By.XPATH, "//button[contains(@class, 'send')]")
                    send_btn.click()
                    self.log(f"📩 Ответ на комментарий #{i+1}")
                    self.random_sleep(3, 5)
                except:
                    pass
        except Exception as e:
            self.log(f"⚠️ Ошибка ответа: {e}")

    def add_link(self):
        try:
            if random.random() < 0.3:
                self.log("🔗 Добавление ссылки в профиль...")
                self.driver.get("https://www.tiktok.com/@.../edit")
                link_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Instagram or YouTube link']")
                link_input.send_keys("https://instagram.com/example")
                save_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Save')]")
                save_btn.click()
                self.log("✅ Ссылка добавлена")
        except:
            pass

    def run_day(self):
        if self.day == 1:
            self.log(f"📅 День 1: просмотр 15-20 минут")
            self.watch_feed(random.randint(15, 20), 1)
        elif self.day in [2, 3]:
            self.log(f"📅 День {self.day}: просмотр 20-25 минут")
            self.watch_feed(random.randint(20, 25), self.day)
        elif self.day in [4, 5]:
            self.log(f"📅 День {self.day}: профиль + 1 видео")
            self.fill_profile()
            self.random_sleep(2, 3)
            if self.post_video():
                self.watch_feed(random.randint(15, 20), self.day)
        elif self.day in [6, 7]:
            self.log(f"📅 День {self.day}: 1-2 видео + комментарии")
            video_count = random.randint(1, 2)
            for _ in range(video_count):
                if self.post_video():
                    self.watch_feed(random.randint(15, 20), self.day)
                self.random_sleep(5, 10)
            self.reply_comments()
            self.add_link()
        self.day += 1

    def start(self, resume=False):
        self.running = True
        self.setup_driver()

        if resume:
            self.driver.get("https://www.tiktok.com")
            self.random_sleep(2, 3)
            if not self.load_session():
                self.log("⚠️ Не удалось загрузить сессию, выполняю вход...")
                if not self.login():
                    self.log("❌ Ошибка входа. Прогрев отменён")
                    return
        else:
            if not self.login():
                self.log("❌ Ошибка входа. Прогрев отменён")
                return

        while self.day <= 7 and self.running:
            self.run_day()
            self.save_session(self.day)

        if self.running:
            self.log("🎉 Прогрев завершён! Аккаунт прогрет.")

        if self.driver:
            self.driver.quit()

    def stop(self):
        self.running = False
        self.log("⏹️ Останавливаю прогрев...")
        if self.driver:
            self.driver.quit()


def check_session(email):
    session_file = f"session_{email}.pkl"
    if os.path.exists(session_file):
        try:
            with open(session_file, "rb") as f:
                data = pickle.load(f)
                day = data.get("day", 1)
                if day > 7:
                    return None, "завершена"
                return day, f"найдена (День {day})"
        except:
            return None, "повреждена"
    return None, "не найдена"


def main():
    clear()
    logo()

    email = input("📧 Введите почту: ").strip()
    password = input("🔑 Введите пароль: ").strip()

    if not email or not password:
        print("❌ Почта и пароль обязательны!")
        return

    proxy = input("🌐 Прокси (опционально, Enter для пропуска): ").strip() or None

    print("\nВыберите способ входа:")
    print("1. Email")
    print("2. Google")
    print("3. Facebook")
    login_choice = input("Введите номер (1-3): ").strip()

    if login_choice == "2":
        login_type = "google"
    elif login_choice == "3":
        login_type = "facebook"
    else:
        login_type = "email"

    clear()
    logo()

    day, status = check_session(email)

    if status == "завершена":
        print(f"✅ Аккаунт {email} уже полностью прогрет (7 дней)")
        input("\nНажмите Enter для выхода...")
        return

    if day:
        print(f"📦 Сессия: {status}")
        print(f"📅 Текущий день: {day}/7")
        resume = input("\n🔄 Продолжить с Дня {day}? (y/n): ").strip().lower()
        if resume == 'y':
            warmer = TikTokWarmer(email, password, proxy, login_type, day)
            warmer.start(resume=True)
            input("\n✅ Прогрев завершён! Нажмите Enter для выхода...")
            return

    print("▶️ Запуск прогрева с Дня 1...")
    warmer = TikTokWarmer(email, password, proxy, login_type, 1)
    warmer.start(resume=False)

    input("\n✅ Прогрев завершён! Нажмите Enter для выхода...")


if __name__ == "__main__":
    main()
