from flask import Flask, render_template, request
import re

class complex_numbers:
    def __init__(self, real, img):
        self.real = real
        self.img = img

    def shownumber(self):
        img_part = f"{abs(self.img)}i" if self.img != 0 else ""
        sign = "+" if self.img > 0 else "-" if self.img < 0 else ""
        return f"{self.real}{sign}{img_part}" if self.img != 0 else f"{self.real}"

    def __add__(self, num2):
        newreal = self.real + num2.real
        newimg = self.img + num2.img
        return complex_numbers(newreal, newimg)

    def __sub__(self, num2):
        newreal = self.real - num2.real
        newimg = self.img - num2.img
        return complex_numbers(newreal, newimg)

    def __mul__(self, num2):
        newreal = self.real * num2.real - self.img * num2.img
        newimg = self.real * num2.img + self.img * num2.real
        return complex_numbers(newreal, newimg)

    def __truediv__(self, num2):
        conj = complex_numbers(num2.real, -num2.img)
        numerator = self.__mul__(conj)
        denominator = num2.real * num2.real + num2.img * num2.img
        newreal = round(numerator.real / denominator, 3)
        newimg = round(numerator.img / denominator, 3)
        return complex_numbers(newreal, newimg)

def parse_complex_number(num_str):
    num_str = num_str.replace(" ", "")
    if 'i' not in num_str:
        num_str += '+0i'
    elif num_str.endswith('i'):
        if '+' not in num_str and '-' not in num_str[1:]:
            num_str = num_str.replace('i', '+1i')
        elif num_str.endswith('i'):
            num_str = re.sub(r'(?<![0-9.])[i]$', '1i', num_str)
    if num_str == 'i':
        num_str = '0+1i'
    elif num_str == '-i':
        num_str = '0-1i'

    match = re.match(r"([-+]?\d*\.?\d+)?([+-]\d*\.?\d+)?i$", num_str)
    if match:
        real = float(match.group(1)) if match.group(1) else 0
        img = float(match.group(2).replace('i', '')) if match.group(2) else 0
        return complex_numbers(real, img)
    else:
        raise ValueError("Invalid complex number format")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    num1_str = request.form['num1']
    num2_str = request.form['num2']
    operation = request.form['operation']

    try:
        num1 = parse_complex_number(num1_str)
        num2 = parse_complex_number(num2_str)
    except ValueError as e:
        return render_template('index.html', result=str(e))

    if operation == 'add':
        result = num1 + num2
    elif operation == 'subtract':
        result = num1 - num2
    elif operation == 'multiply':
        result = num1 * num2
    elif operation == 'divide':
        try:
            result = num1 / num2
        except ZeroDivisionError:
            return render_template('index.html', result="Division by zero is not allowed")
    else:
        return render_template('index.html', result="Invalid Operation")

    result_str = result.shownumber()
    return render_template('index.html', result=result_str)

if __name__ == '__main__':
    app.run(debug=True)
