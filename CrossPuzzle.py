# coding: utf-8
import numpy as np

### CONST VALUE ###
DELETE_OBJ = 'D' # 削除予定文字
OUTER_OBJ = 'O' # 外周文字（外周が十字に含まれるらしいので１周分枠を用意、おそらく不要だがNULL配列参照の処理を諦めて対処）
EMPTY_OBJ = '.' # 仕様書規定の空白ピース文字
TABLE_COLMN = 7 # 外周を含めた列数

### GLOBAL VALUE ###
Table_Row = ''
########

def make_table(input_data):
    global Table_Row
    table = []
    table_row = []

    for count in range(len(input_data) + 1):
        if count == 0 or count == Table_Row - 1:
            if count == 0:
                Table_Row = int(input_data[count]) + 2

            # count == 0 上外周を作成する
            # count == Table_Row - 1 下外周を作成する
            for count in range(TABLE_COLMN):
                table_row.append(OUTER_OBJ)
        else:
            table_row.append(OUTER_OBJ) # 左外周
            for char in input_data[count]:
                table_row.append(char)
            table_row.append(OUTER_OBJ) # 右外周
        table.append(table_row)
        table_row = []

    return table

def delete_cross_match(table):
    while True:
        table_update_flag = False
        for row in range(1, Table_Row - 1):
            # tableの行毎に十字を探索する、１行目と最終行は外周文字しかない為探索から除外
            for column in range(1, TABLE_COLMN - 1):
                # tableの列毎に十字を探索する、１列目と最終行は外周文字しかない為探索から除外
                ref_char = table[row][column]
                if ref_char == EMPTY_OBJ:
                    continue

                result = check_match(table, row, column - 1, ref_char) # 左の探索
                if result:
                    result = check_match(table, row, column + 1, ref_char) # 右の探索
                if result:
                    result = check_match(table, row - 1, column, ref_char) # 上の探索
                if result:
                    result = check_match(table, row + 1, column, ref_char) # 下の探索
                if result:
                    # 上下左右が探索文字と一致している十字か、外周に吸われたトかＬ字の為削除予定文字に置き換える
                    table = replace_delete_obj(table, row, column)
                    table = replace_delete_obj(table, row - 1, column)
                    table = replace_delete_obj(table, row + 1, column)
                    table = replace_delete_obj(table, row, column - 1)
                    table = replace_delete_obj(table, row, column + 1)
                    while True:
                        # 削除予定文字の隣人も削除予定文字にする、削除予定文字になった隣人も探索対象になるため対象が無くなるまでwhileで回す
                        table, replace_flag = delete_neighbor(table, ref_char)
                        if replace_flag:
                            table_update_flag = True
                        if not replace_flag or ref_char == DELETE_OBJ or ref_char == OUTER_OBJ or ref_char == EMPTY_OBJ:
                            break
                    while True:
                        # ピースを落下させる
                        table, replace_flag = fall_pieces(table)
                        if replace_flag:
                            table_update_flag = True
                        if not replace_flag:
                            break
        if not table_update_flag:
            break

    return table

def replace_delete_obj(table, row, column):
    # 削除予定文字に置き換える、外周文字なら置き換えない
    if table[row][column] != OUTER_OBJ:
        table[row][column] = DELETE_OBJ
    return table

def fall_pieces(table):
    # 削除予定文字を空白文字に置き換える
    replace_flag = False
    for row in range(Table_Row - 2, 1, -1):
        for column in range(1, TABLE_COLMN - 1):
            if table[row][column] == DELETE_OBJ:
                for count in range(row):
                    current_row = row - count
                    if table[current_row - 1][column] == OUTER_OBJ:
                        table[current_row][column] = EMPTY_OBJ
                    else:
                        table[current_row][column] = table[current_row - 1][column]
                replace_flag = True
                break
        
        if replace_flag:
            break

    return table, replace_flag

def delete_neighbor(table, ref_char):
    # 削除予定文字の隣人も削除予定文字にする
    replace_flag = False
    for row in range(1, Table_Row - 1):
        for column in range(1, TABLE_COLMN - 1):
            if table[row][column] == DELETE_OBJ:
                result = check_match(table, row, column - 1, ref_char)
                if result == DELETE_OBJ: # 左の削除（外周でなければ）
                    table = replace_delete_obj(table, row, column - 1)
                    replace_flag = True

                result = check_match(table, row, column + 1, ref_char)
                if result == DELETE_OBJ: # 右の削除（外周でなければ）
                    table = replace_delete_obj(table, row, column + 1)
                    replace_flag = True

                result = check_match(table, row - 1, column, ref_char)
                if result == DELETE_OBJ: # 上の削除（外周でなければ）
                    table = replace_delete_obj(table, row - 1, column)
                    replace_flag = True

                result = check_match(table, row + 1, column, ref_char)
                if result == DELETE_OBJ: # 下の削除（外周でなければ）
                    table = replace_delete_obj(table, row + 1, column)
                    replace_flag = True
    return table, replace_flag

def check_match(table, row, column, ref_char):
    # 入力文字が検索対象文字と一致しているか判定する、一致の場合は削除予定文字を返す、外周は対象と一致することにする
    ret = ''
    if table[row][column] == ref_char:
        ret = DELETE_OBJ
    elif table[row][column] == OUTER_OBJ:
        ret = OUTER_OBJ
    else:
        ret = ''
    return ret

def create_result(table):
    # 追加した要らない外周以外を出力する
    for row in range(len(table)):
        for piece in table[row]:
            if piece != OUTER_OBJ:
                print(piece, end='')
        if row != 0:
            print()
    return

def input_data():
    input_line = []
    input_row = input()
    input_line.append(input_row)
    for count in range(int(input_row)):
        input_text = input()
        input_line.append(input_text)
    return input_line

def main():
    input_line = input_data()
    puzzule_table = make_table(input_line)
    puzzule_table = delete_cross_match(puzzule_table)
    create_result(puzzule_table)
    return

if __name__ == '__main__':
    main()