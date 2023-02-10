# from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import random
from math import floor

PROBLEM_HEIGHT_TO_FONT_SIZE = 6


class ProblemSet():
    my_canvas = None
    fontwidth = 9.6
    start_idx = 0
    next_idx = 0
    start_idy = 0
    next_idy = 0
    font_size = 16
    largest_prob_width = 0
    problem_height = 0
    new_page_before_draw = False

    def __init__(self, canvas: canvas, font_size: int = 16):
        # default canvas A4 size if 612 wide by 792 long
        self.my_canvas = canvas
        self.font_size = font_size
        self._setCanvasState()

    def _drawSubtractProblem(self, num1: int, num2: int):
        if self.new_page_before_draw:
            self.my_canvas.showPage()
            self._setCanvasState()
            self.new_page_before_draw = False
        num1_width = len(str(num1)) * self.fontwidth
        num2_width = len(str(num2)) * self.fontwidth
        num1_idx = self.next_idx + (self.largest_prob_width - num1_width)
        num2_idx = self.next_idx + (self.largest_prob_width - num2_width)
        self.my_canvas.drawString(num1_idx, self.next_idy, str(num1))
        self.my_canvas.drawString(
            num2_idx, self.next_idy-self.font_size, str(num2))
        self.my_canvas.drawString(
            self.next_idx, self.next_idy-self.font_size, '-')
        self.my_canvas.line(self.next_idx, self.next_idy-self.font_size-4,
                            self.next_idx+self.largest_prob_width, self.next_idy-self.font_size-4)
        self._goNextProb(self.largest_prob_width)

    def _drawAdditionProblem(self, num1: int, num2: int):
        if self.new_page_before_draw:
            self.my_canvas.showPage()
            self._setCanvasState()
            self.new_page_before_draw = False
        num1_width = len(str(num1)) * self.fontwidth
        num2_width = len(str(num2)) * self.fontwidth
        num1_idx = self.next_idx + (self.largest_prob_width - num1_width)
        num2_idx = self.next_idx + (self.largest_prob_width - num2_width)
        self.my_canvas.drawString(num1_idx, self.next_idy, str(num1))
        self.my_canvas.drawString(
            num2_idx, self.next_idy-self.font_size, str(num2))
        self.my_canvas.drawString(
            self.next_idx, self.next_idy-self.font_size, '+')
        self.my_canvas.line(self.next_idx, self.next_idy-self.font_size-4,
                            self.next_idx+self.largest_prob_width, self.next_idy-self.font_size-4)
        self._goNextProb(self.largest_prob_width)

    def _drawMultiplicationProblem(self, num1: int, num2: int):
        if self.new_page_before_draw:
            self.my_canvas.showPage()
            self._setCanvasState()
            self.new_page_before_draw = False
        num1_width = len(str(num1)) * self.fontwidth
        num2_width = len(str(num2)) * self.fontwidth
        num1_idx = self.next_idx + (self.largest_prob_width - num1_width)
        num2_idx = self.next_idx + (self.largest_prob_width - num2_width)
        self.my_canvas.drawString(num1_idx, self.next_idy, str(num1))
        self.my_canvas.drawString(
            num2_idx, self.next_idy-self.font_size, str(num2))
        self.my_canvas.drawString(
            self.next_idx, self.next_idy-self.font_size, 'x')
        self.my_canvas.line(self.next_idx, self.next_idy-self.font_size-4,
                            self.next_idx+self.largest_prob_width, self.next_idy-self.font_size-4)
        self._goNextProb(self.largest_prob_width)

    def _setCanvasState(self):
        self.my_canvas.setLineWidth(1)
        self.my_canvas.setFont('Courier', self.font_size)
        self.fontwidth = self.my_canvas.stringWidth(
            '1', 'Courier', self.font_size)

    def _goNextProb(self, last_width):
        self.next_idx += (last_width * 1.8)
        # check if the problem set will go near the end of the page, then go to next line
        if(self.next_idx + last_width * 1.8 > floor(self.my_canvas._pagesize[0]) - 36):
            self.next_idx = self.start_idx
            self.next_idy = self.next_idy - self.problem_height
        if(self.next_idy - self.problem_height < 0):
            self.new_page_before_draw = True
            self.next_idx = self.start_idx
            self.next_idy = self.start_idy

    def save(self):
        self.my_canvas.save()

    def _setProblemDimension(self, num1_range, num2_range, prob_type: str = "add"):
        longest = max(len(str(num1_range[0])), len(str(num1_range[1])), len(
            str(num2_range[0])), len(str(num2_range[1])))
        self.largest_prob_width = (longest+2) * self.fontwidth
        self.problem_height = self.font_size * PROBLEM_HEIGHT_TO_FONT_SIZE
        if prob_type == "multiply":
            # additional room for larger multiplicand range
            self.problem_height += self.font_size * \
                (len(str(num2_range[1])) - 2)

    def _setInitialStart(self):
        if self.largest_prob_width <= 0:
            return
        # magic margin 0.5 inch which is equivalent to 36, then times 2 for both left and right, top and bottom
        content_width = floor(self.my_canvas._pagesize[0]) - 72
        content_height = floor(self.my_canvas._pagesize[1]) - 72
        self.start_idx = 36 + \
            ((content_width % (self.largest_prob_width * 1.8)) / 2)
        self.start_idy = floor(
            self.my_canvas._pagesize[1]) - 36 - ((content_height % self.problem_height) / 2)
        self.next_idx, self.next_idy = self.start_idx, self.start_idy

    def _generateSubtractProblem(self, minuend_range: tuple[int, int], subtrahend_range: tuple[int, int], negative: bool = False):
        minuend = random.randint(*minuend_range)
        if not negative:
            if minuend == subtrahend_range[0]:
                subtrahend = minuend
            elif minuend > subtrahend_range[1]:
                subtrahend = random.randint(*subtrahend_range)
            else:
                subtrahend = random.randint(subtrahend_range[0], minuend-1)
        else:
            subtrahend = random.randint(*subtrahend_range)
        return (minuend, subtrahend)

    def _generateAdditionProblem(self, base_range: tuple[int, int], addend_range: tuple[int, int]):
        return (random.randint(*base_range), random.randint(*addend_range))

    def _generateMultiplyProblem(self, multiplier_range: tuple[int, int], multiplicand_range: tuple[int, int]):
        return (random.randint(*multiplier_range), random.randint(*multiplicand_range))

    def generateProblemSet(self, prob_type: str = 'add', num_prob: int = 20, sub_neg: bool = False, num1_range: tuple[int, int] = None, num2_range: tuple[int, int] = None):
        if num1_range is None or num2_range is None:
            raise ValueError("number range is required!")
        self._setProblemDimension(num1_range, num2_range, prob_type)
        self._setInitialStart()
        if prob_type == 'add':
            for i in range(num_prob):
                prob = self._generateAdditionProblem(num1_range, num2_range)
                self._drawAdditionProblem(*prob)
        elif prob_type == 'subtract':
            for i in range(num_prob):
                prob = self._generateSubtractProblem(
                    num1_range, num2_range, sub_neg)
                self._drawSubtractProblem(*prob)
        elif prob_type == 'multiply':
            for i in range(num_prob):
                prob = self._generateMultiplyProblem(num1_range, num2_range)
                self._drawMultiplicationProblem(*prob)
        else:
            raise NotImplementedError(
                f"Problem type [{prob_type}] not implemented yet")


def generate(path):
    my_canvas = canvas.Canvas(path)
    probset = ProblemSet(my_canvas, font_size=18)
    probset.generateProblemSet('multiply', 50, (10, 9999), (10, 999))
    probset.save()


if __name__ == '__main__':
    generate('problemset.pdf')
