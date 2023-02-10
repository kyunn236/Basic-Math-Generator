from basicmathgen import ProblemSet
from reportlab.pdfgen import canvas

my_canvas = canvas.Canvas("problemset.pdf")
probset = ProblemSet(my_canvas, font_size=18)
"""
Add:
up to 999 = 35 problems/page
up to 99 = 42 problems/page
"""
probset.generateProblemSet('multiply', num_prob=42*2,
                           num1_range=(10, 99), num2_range=(10, 99))
probset.save()
