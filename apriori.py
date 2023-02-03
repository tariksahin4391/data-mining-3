import string

items = open('items.txt', 'r')
threshold = 0.3
temp_result_current = open('temp_result_1.txt', 'w')

# step 1
for item in items:
    item_count = 0
    transaction_count = 0
    transactions = open('transactions.txt', 'r')
    for transaction in transactions:
        transaction_count += 1
        transaction_arr = transaction.replace('\n', '').split(',')
        item_id = item.split(',')[0]
        if item_id in transaction_arr:
            item_count += 1
    transactions.close()
    item_rate = item_count / transaction_count
    if item_rate >= threshold:
        arr = item.split(',')
        temp_result_current.write(arr[0] + ';' + str(item_count) + ';' + str(item_rate) + '\n')
temp_result_current.close()


def calculate_by_threshold(before_file, current_file):
    c1 = 0
    before = open(before_file, 'r')  # bir önceki iterasyondaki sonuçlar
    clean = open(current_file, 'w')
    clean.truncate()
    clean.close()
    for item1 in before:
        c2 = c1 + 1
        c3 = 0
        before2 = open(before_file, 'r')
        for item2 in before2:
            if c3 < c2:
                c3 += 1
                continue
            item1_row_arr = item1.replace('\n', '').split(';')
            item2_row_arr = item2.replace('\n', '').split(';')
            c3 += 1
            item1_arr = item1_row_arr[0].split(',')
            item2_arr = item2_row_arr[0].split(',')
            if len(item1_arr) < 2:
                rate = search_items_in_transactions(item1_arr + item2_arr)
                if rate >= threshold:
                    current = open(current_file, 'a')  # bu iterasyonda oluşan sonuçlar
                    current.write(item1_arr[0] + ',' + item2_arr[0] + ';' + str(rate) + '\n')
                    current.close()
            else:
                merged = list(set(item1_arr + item2_arr))
                if not search_item_in_file(merged, current_file):
                    if len(merged) == len(item1_arr) + 1:
                        # prune
                        if not prune(merged, before_file):
                            rate = search_items_in_transactions(merged)
                            if rate >= threshold:
                                current = open(current_file, 'a')  # bu iterasyonda oluşan sonuçlar
                                current.write(array_to_string(merged) + ';' + str(rate) + '\n')
                                current.close()
        before2.close()
        c1 += 1
    before.close()
    check_file = open(current_file, 'r')
    counter = 0
    for c in check_file:
        counter += 1
    check_file.close()
    if counter > 0:
        calculate_by_threshold(current_file, before_file)


def array_to_string(arr):
    res = ''
    for i in range(0, len(arr)):
        res = res + arr[i]
        if i != len(arr) - 1:
            res = res + ','
    return res


def search_items_in_transactions(merged_items):
    transactions2 = open('transactions.txt', 'r')
    tr_count = 0
    found_count = 0
    for t in transactions2:
        tr_count += 1
        found = True
        a = t.replace('\n', '').split(',')
        for i in merged_items:
            if not i in a:
                found = False
                break
        if found:
            found_count += 1
    transactions2.close()
    return found_count / tr_count


def search_item_in_file(item_array, file_name):
    found = False
    file = open(file_name, 'r')
    for f in file:
        found = True
        a = f.replace('\n', '').split(';')[0].split(',')
        for i in item_array:
            if not i in a:
                found = False
                break
    file.close()
    return found


def prune(merged, file_name):
    found = True
    for i in range(0, len(merged)):
        sub = merged[0:i] + merged[i + 1:len(merged)]
        file = open(file_name, 'r')
        sub_found = True
        for f in file:  # [A,B] [C,D]
            a = f.replace('\n', '').split(';')[0].split(',')  # [A,B]
            sub_found = True
            for s in sub:  # [A,C]
                if not s in a:
                    sub_found = False
                    break
            if sub_found:
                break
        if not sub_found:
            found = False
            break
    if not found:
        print('pruned item ', merged)
    return not found  # bulunamadıysa prune yap


calculate_by_threshold('temp_result_1.txt', 'temp_result_2.txt')
items.close()
