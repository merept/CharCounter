from output import Output


def file_lines_to_lower(file_path):
    return open(file_path, encoding="utf-8").read().lower().splitlines()


def is_character(char):
    return True if '\u4e00' <= char <= '\u9fff' or char.isalpha() else False


def get_count_from_lines(values):
    results = {}
    total_chars = 0
    for value in values:
        for char in value:
            if not is_character(char):
                continue
            if char in results:
                results[char] += 1
            else:
                results[char] = 1
            total_chars += 1
    return results, total_chars


def get_second(element):
    return element[1]


def count(file_path):
    lines = file_lines_to_lower(file_path)
    output = Output(file_path)
    lines_dict, total_count = get_count_from_lines(lines)
    ls = list(lines_dict.items())
    ls.sort(key=get_second, reverse=True)
    print(f'当前文件: {file_path}\n'
          '选择以何种方式查看结果:\n'
          '1.在终端显示结果\n'
          '2.导出为 CSV 文件\n'
          '3.导出为 JSON 文件\n'
          '4.导出为 YAML 文件\n'
          '5.导出为 XML 文件\n'
          '6.导出为 Excel 文件\n'
          '0.退出')
    select = input('请输入选项 > ')
    done = False
    is_exit = False
    while not done:
        done = True
        if select == '1':
            print(output.to_string(ls, total_count))
        elif select == '2':
            output.to_csv(ls, total_count)
        elif select == '3':
            output.to_json_yaml(ls, total_count)
        elif select == '4':
            output.to_json_yaml(ls, total_count, is_yaml=True)
        elif select == '5':
            output.to_xml(ls, total_count)
        elif select == '6':
            output.to_xlsx(ls, total_count)
        elif select == '0':
            is_exit = True
        else:
            select = input('\n输入错误, 请重新输入 > ')
            done = False

    return is_exit
