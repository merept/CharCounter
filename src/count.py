import re
import os

import jieba
import wordninja

from src.output import Output


def file_lines_to_lower(file_path):
    return open(file_path, encoding="utf-8").read().lower().splitlines()


def is_chinese(value):
    return re.compile(r'[\u4e00-\u9fa5]+').search(value)


def is_english(value):
    return re.compile(r'[A-Za-z]+').search(value)


def is_word(word):
    return is_chinese(word) or is_english(word)


def is_mixed(line):
    return is_chinese(line) and is_english(line)


def extract_chinese(line):
    pattern = re.compile(r'[^\u4e00-\u9fa5]+')
    return re.sub(pattern, '', line)


def extract_english(line):
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    return re.sub(pattern, '', line)


def is_character(char):
    return True if '\u4e00' <= char <= '\u9fff' or char.isalpha() else False


def char_count_from_lines(values):
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


def word_count_from_lines(values):
    results = {}
    total_words = 0
    for value in values:
        if is_mixed(value):
            chinese = extract_chinese(value)
            english = extract_english(value)
            words = jieba.lcut(chinese)
            words += wordninja.split(english)
        elif is_chinese(value):
            words = jieba.lcut(value)
        else:
            words = wordninja.split(value)
        for word in words:
            if not is_word(word):
                continue
            if word in results:
                results[word] += 1
            else:
                results[word] = 1
            total_words += 1
    return results, total_words


def get_second(element):
    return element[1]


def is_analysis_char(dictionary):
    print(f'1.{dictionary["charAna"]}\n2.{dictionary["wordAna"]}')
    select = input(f'{dictionary["select"]} > ')
    return True if select == '1' else False


def count(file_path, dictionary):
    lines = file_lines_to_lower(file_path)

    is_ana_char = is_analysis_char(dictionary)
    if is_ana_char:
        lines_dict, total_count = char_count_from_lines(lines)
    else:
        lines_dict, total_count = word_count_from_lines(lines)

    output = Output(file_path, is_ana_char, dictionary)
    ls = list(lines_dict.items())
    ls.sort(key=get_second, reverse=True)

    os.system('cls')
    print(f'{dictionary["currentFile"]}: {file_path}\n'
          f'{dictionary["selInfo"]}:\n'
          f'1.{dictionary["terminal"]}\n'
          f'2.{dictionary["csv"]}\n'
          f'3.{dictionary["json"]}\n'
          f'4.{dictionary["yaml"]}\n'
          f'5.{dictionary["xml"]}\n'
          f'6.{dictionary["excel"]}\n'
          f'0.{dictionary["exit"]}')

    select = input(f'{dictionary["select"]} > ')
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
            select = input(f'\n{dictionary["wrongSel"]} > ')
            done = False

    return is_exit
