def count_trailing_zeros(n):
    count_zeros = 0
    divisor = 5
    
    while n >= divisor:
        count_zeros += n // divisor
        divisor *= 5
    
    return count_zeros

# ตัวอย่างการใช้งาน
num = 7028
num_zeros = count_trailing_zeros(num)
print(f"{num}! มีเลข 0 ต่อท้าย {num_zeros} ตัว")