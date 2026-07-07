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
    
class Fiftyfifty:
    """
    Fiftyfiftyクラス
    クイズの選択肢を半分に減らすライフライン
    """
    def __init__(self,quiz: Quiz) -> None:
        """
        引数:Quizクラス
        戻り値:なし
        答えの選択肢をQuizクラスから取得、
        現在の選択肢から正解とランダムに選ばれた不正解の選択肢以外を削除
        """
        answer = quiz.answer
        self.choices = [False,False,False,False]
        miss = [0,1,2,3]
        miss.remove(answer)

        self.choices[answer] = True  # Trueの選択肢は残る
        self.choices[random.choice(miss)] = True

    def is_collect(self, index:int) -> list:
        """
        引数:int
        戻り値:list
        イニシャライザで作った消す選択肢のリストを返す
        """
        return self.choices[index]


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

        self.fifty = None
        self.fifty_used = False

        self.next_quiz()

    def use_fifty(self):
        """
        50-50を使う関数
        使われたならfifty-usedをTrueにし、2回目の使用を不可能にする。
        """
        if self.fifty_used:
            return  # もし使われているならそのまま出る
        
        if self.fifty is None:
            self.fifty = Fiftyfifty(self.current_quiz)
            self.fifty_used = True

    # --------------------------
    # 次の問題
    # --------------------------
    def next_quiz(self):

        self.current_quiz = random.choice(self.quizzes)
        self.answered = False
        self.message = ""

        self.fifty = None

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

            if self.fifty is not None:
                if not self.fifty.is_collect(i):  # もし使わない選択肢なら、この回のループを終了する
                    continue

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

                if event.key == pygame.K_f:  # Fキーが押されたら50-50を使用
                    self.use_fifty()


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