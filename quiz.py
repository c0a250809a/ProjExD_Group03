import pygame
import random
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ==========================
# Quizクラス
# ==========================
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer


# ==========================
# Buttonクラス
# ==========================
class Button:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, font, text, color):
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        image = font.render(text, True, (0, 0, 0))
        screen.blit(image, (self.rect.x + 20, self.rect.y + 15))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# ==========================
# QuizGameクラス
# ==========================
class QuizGame:

    def __init__(self):

        pygame.init()

        self.WIDTH = 800
        self.HEIGHT = 600

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("4択クイズ")

        # フォント
        base_dir = os.path.dirname(__file__)
        font_path = os.path.join(
            base_dir,
            "fonts",
            "NotoSansJP-Bold.ttf"
        )

        self.question_font = pygame.font.Font(font_path, 40)
        self.choice_font = pygame.font.Font(font_path, 30)
        self.result_font = pygame.font.Font(font_path, 36)
        self.timer_font = pygame.font.Font(font_path, 36) #　タイマー用のフォントの追加

        # 色
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (220, 220, 220)
        self.GREEN = (120, 230, 120)
        self.RED = (255, 120, 120)

        # 問題
        self.quizzes = [
            Quiz(
                "日本の首都は？",
                ["大阪", "東京", "福岡", "札幌"],
                1
            ),

            Quiz(
                "Pythonを開発した人物は？",
                [
                    "Guido van Rossum",
                    "Bill Gates",
                    "Steve Jobs",
                    "Linus Torvalds"
                ],
                0
            ),

            Quiz(
                "1 + 1 = ?",
                ["1", "2", "3", "4"],
                1
            )
        ]

        # ボタン
        self.buttons = []

        for i in range(4):
            self.buttons.append(
                Button(
                    120,
                    200 + i * 80,
                    560,
                    60
                )
            )

        self.current_quiz = None
        self.answered = False
        self.message = ""

        #　タイマー用の変数
        self.LIMIT_TIME = 10.0
        self.start_time = 0
        self.remaining_time = self.LIMIT_TIME

        self.next_quiz()

    # --------------------------
    # 次の問題
    # --------------------------
    def next_quiz(self):

        self.current_quiz = random.choice(self.quizzes)
        self.answered = False
        self.message = ""
        self.start_time = pygame.time.get_ticks() #　出題したときの時間を記録

    # --------------------------
    # タイマー更新・判定
    # --------------------------
    def update_timer(self):
        """
        未回答の場合に経過時間を計算してカウントダウンし、タイムアップを判定するメソッド
        引数：なし
        戻り値：なし
        """
        if not self.answered:
            elapsed_seconds = (pygame.time.get_ticks() - self.start_time) / 1000
            self.remaining_time = max(0.0, self.LIMIT_TIME - elapsed_seconds)

            #　タイムアップ判定
            if self.remaining_time <= 0:
                self.answered = True
                answer = self.current_quiz.choices[self.current_quiz.answer]
                self.mesage = f"タイムアップ！　正解は「{answer}」"
        else:
            self.remaining_time = 0.0

    # --------------------------
    # 描画
    # --------------------------
    def draw(self):

        self.screen.fill(self.WHITE)

        question = self.question_font.render(
            self.current_quiz.question,
            True,
            self.BLACK
        )

        self.screen.blit(question, (40, 50))

        #　タイマー表示(問題の上に表示。残り3秒になると文字が赤くなる)
        timer_color = self.RED if self.remaining_time <= 3.0 else self.BLACK
        timer_text = self.timer_font.render(
            f"残り時間：{self.remaining_time:.1f}秒",
            True,
            timer_color
        )
        self.screen.blit(timer_text, (40,10))

        for i in range(4):

            color = self.GRAY

            if self.answered and i == self.current_quiz.answer:
                color = self.GREEN

            self.buttons[i].draw(
                self.screen,
                self.choice_font,
                self.current_quiz.choices[i],
                color
            )

        result = self.result_font.render(
            self.message,
            True,
            self.RED
        )

        self.screen.blit(result, (40, 550))

        pygame.display.flip()

    # --------------------------
    # イベント
    # --------------------------
    def event(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if not self.answered:

                    pos = pygame.mouse.get_pos()

                    for i in range(4):

                        if self.buttons[i].is_clicked(pos):

                            self.answered = True

                            if i == self.current_quiz.answer:
                                self.message = "正解！"

                            else:
                                answer = self.current_quiz.choices[
                                    self.current_quiz.answer
                                ]

                                self.message = (
                                    f"不正解！ 正解は「{answer}」"
                                )

            elif event.type == pygame.KEYDOWN:

                if self.answered:

                    if event.key == pygame.K_SPACE:
                        self.next_quiz()

    # --------------------------
    # メインループ
    # --------------------------
    def run(self):

        clock = pygame.time.Clock()

        while True:

            self.event()

            self.update_timer() #　更新・判定をする
    
            self.draw()

            clock.tick(60)


# ==========================
# 実行
# ==========================
if __name__ == "__main__":

    game = QuizGame()
    game.run()