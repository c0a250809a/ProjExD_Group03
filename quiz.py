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

        self.next_quiz()

    # --------------------------
    # 次の問題
    # --------------------------
    def next_quiz(self):

        self.current_quiz = random.choice(self.quizzes)
        self.answered = False
        self.message = ""

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
            self.draw()

            clock.tick(60)


# ==========================
# 実行
# ==========================
if __name__ == "__main__":

    game = QuizGame()
    game.run()