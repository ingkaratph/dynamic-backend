def arabic_to_roman(number):
    if 0 < number <= 1000:
        roman_numerals = {
            1: 'I', 4: 'IV', 5: 'V', 9: 'IX', 10: 'X', 40: 'XL',
            50: 'L', 90: 'XC', 100: 'C', 400: 'CD', 500: 'D', 900: 'CM',
            1000: 'M'
        }
        result = ''
        for value, numeral in sorted(roman_numerals.items(), reverse=True):
            while number >= value:
                result += numeral
                number -= value
        return result
    else:
        return "ค่าที่รับต้องอยู่ระหว่าง 1 ถึง 1000"

if __name__ == '__main__':
    while True:
        user_input = input("ใส่ตัวเลขที่ต้องการแปลงเป็นตัวเลขโรมัน (พิมพ์ 'exit' เพื่อออกจากโปรแกรม): ")
        if user_input.lower() == 'exit':
            print('ออกจากโปรแกรม')
            break
        try:
            number = int(user_input)
            print(arabic_to_roman(number))
        except ValueError:
            print("ใส่ตัวเลขที่ถูกต้องหรือพิมพ์ 'exit' เพื่อออกจากโปรแกรม'")