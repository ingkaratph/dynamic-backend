def thai_text(number):
    if 0 <= number < 10_000_000:
        thai_number = ('ศูนย์', 'หนึ่ง', 'สอง', 'สาม', 'สี่', 'ห้า', 'หก', 'เจ็ด', 'แปด', 'เก้า')
        thai_units = ('', 'สิบ', 'ร้อย', 'พัน', 'หมื่น', 'แสน', 'ล้าน')
        
        s_number = str(number)[::-1]
        n_list = [s_number[i:i + 6].rstrip('0') for i in range(0, len(s_number), 6)]
        result = unit_process(n_list.pop(0), thai_number, thai_units)

        for i in n_list:
            result = unit_process(i, thai_number, thai_units) + 'ล้าน' + result

        return result
    else:
        return 'ค่าที่รับต้องอยู่ระหว่าง 0 ถึง 9,999,999'

def unit_process(val, thai_number, thai_units):
    length = len(val) > 1
    result = ''
    for index, current in enumerate(map(int, val)):
        if current:
            if index:
                result = thai_units[index] + result
            if length and current == 1 and index == 0:
                result += 'เอ็ด'
            elif index == 1 and current == 2:
                result = 'ยี่' + result
            elif index != 1 or current != 1:
                result = thai_number[current] + result
    return result

if __name__ == '__main__':
    while True:
        user_input = input("ใส่ตัวเลขที่ต้องการแปลงเป็นข้อความภาษาไทย (พิมพ์ 'exit' เพื่อออกจากโปรแกรม): ")
        if user_input.lower() == 'exit':
            print('ออกจากโปรแกรม')
            break
        try:
            number = int(user_input)
            print(thai_text(number))
        except ValueError:
            print("ใส่ตัวเลขที่ถูกต้องหรือพิมพ์ 'exit' เพื่อออกจากโปรแกรม'")