def find_max_index(arr):
    max_num = arr[0]  # เริ่มต้นให้ max_num เป็นค่าแรกในอาร์เรย์
    max_index = 0  # เริ่มต้นให้ max_index เป็น 0
    
    for i in range(1, len(arr)):  # ลูปตั้งแต่ index 1 ถึงสุดท้ายของอาร์เรย์
        if arr[i] > max_num:  # เช็คว่าตัวเลขใน index ปัจจุบันมากกว่า max_num หรือไม่
            max_num = arr[i]  # ถ้าใช่ ให้ max_num เป็นค่าใน index ปัจจุบัน
            max_index = i  # และให้ max_index เป็น index ปัจจุบัน
    
    return max_index

arr = [1, 2, 1, 3, 5, 6, 4 , 7 , 9 , 15 , 20]
max_index = find_max_index(arr)
print("Index ของตัวเลขที่มีค่ามากที่สุด:", max_index)
