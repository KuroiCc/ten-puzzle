from itertools import product
from operator import add, sub, mul, truediv
from copy import deepcopy


def make10(q):
    """make10(q) --> result: list

    make 10 from 4 numbers without change the order of number.

    Return all combinations of anwser if it's existed or a empty list.


    q : String, ex)'9999'


    make10('9999') --> ['(9+9*9)/9', '(9*9+9)/9']

    make10('0000') --> []
    """
    q = [float(i) for i in q]
    o = [add, sub, mul, truediv]
    o_string = ['+', '-', '*', '/']

    # すべての演算子コンビネーション
    O_combination = [i for i in product(range(4), repeat=3)]

    # カッコ付け方・計算順番　のすべてのパターン
    O_order = [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 1, 0)]

    # 誤差の許容範囲
    TOL = 0.001

    res = []

    for i in O_combination:
        for o1, o2, o3 in O_order:
            # 計算の順番o1 -> o2 -> o3

            # tは問題のコピー
            t = deepcopy(q)

            # 結果を計算
            try:
                result = o[i[o1]](t[o1], t[o1 + 1])
                t.pop(o1)
                t.pop(o1)
                t.insert(o1, result)
                if o2 < o3:
                    result = o[i[o3]](o[i[o2]](t[0], t[1]), t[2])
                else:
                    result = o[i[o3]](t[0], o[i[o2]](t[1], t[2]))
            except ZeroDivisionError:
                continue

            if abs(result - 10) < TOL:
                # 10になる組み合わせを余計のカッコを除いて文字列に変える

                if [o1, o2, o3] != [0, 2, 1]:
                    # (A o B) o (C o D)以外のパターン

                    # add_paren　はカッコの中は+-計算、かつ、外は*/計算の時、中の計算式に()をつける
                    def add_paren(p, first_o, second_o):
                        if first_o in [0, 1] and second_o in [2, 3]:
                            return '(' + p + ')'
                        else:
                            return p

                    if o1 < o2:
                        p = add_paren('%d%s%d', i[o1], i[o2]) + '%s%d'
                    else:
                        if i[o2] in [1, 3]:
                            # 前が-/のとき後ろに()をつける
                            p = '%d%s(%d%s%d)'
                        else:
                            p = '%d%s' + add_paren('%d%s%d', i[o1], i[o2])

                    if o3 == 2:
                        p = add_paren(p, i[o2], i[o3]) + '%s%d'
                    else:
                        if i[o3] in [1, 3]:
                            # 前が-/のとき後ろに()をつける
                            p = '%d%s(' + p + ')'
                        else:
                            p = '%d%s' + add_paren(p, i[o2], i[o3])
                else:
                    # (A o B) o (C o D)のパターン
                    if i[o3] in [2, 3]:

                        # add_paren2　はカッコの中が+-計算のときのみ、計算式のカッコをつける
                        def add_paren2(p, o):
                            if o in [0, 1]:
                                return '(' + p + ')'
                            else:
                                return p

                        p = '%d%s%d'
                        if i[o3] == 3:
                            # 前が/のとき後ろに()をつける
                            p = add_paren2(p, i[o1]) + '%s(' + p + ')'
                        else:
                            p = add_paren2(p, i[o1]) + '%s' + add_paren2(p, i[o2])
                    elif i[o3] == 1:
                        # 前が-のとき後ろに()をつける
                        p = '%d%s%d%s(%d%s%d)'
                    else:
                        p = '%d%s%d%s%d%s%d'

                # 値と演算子を代入
                p = p % (q[0], o_string[i[0]], q[1], o_string[i[1]], q[2], o_string[i[2]], q[3])
                # print(p)

                if p not in res:
                    res.append(p)

    return res


if __name__ == '__main__':

    def log(out_file, content):
        with open(out_file, 'a', encoding='utf-8') as add:
            add.write(content)

    def output_all():
        res = []
        fal = []
        all_num = [i for i in product([str(x) for x in range(10)], repeat=4)]

        for q in all_num:
            q = ''.join(q)

            if q[1:] == '000':
                print(q)

            t = make10(q)

            if t != []:
                # テストケース,python精度の引っかかったケースを出力
                for i in t:
                    if abs(eval(i) - 10) != 0:
                        print('=====', i)

                log('res.csv', '\n'.join(t) + '\n')
                log('res_ture.csv', q + '\n')
                res.extend(t)
            else:
                log('res_false.csv', q + '\n')
                fal.append(q)
                # print(q)

        # print(len(fal))
        print('done')

    # output_all()
    string = input("input qusetion:")
    while string != 'exit()':
        if make10(string) != []:
            print("なる")
        else:
            print("ならない")

        print()
        string = input("input qusetion:")
