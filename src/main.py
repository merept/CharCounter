import os
import yaml
import json

from service import count


def read_lang_cfg():
    with open(r'.\res\setting', mode='r', encoding='utf-8') as file:
        setting_dict = yaml.load(file, yaml.FullLoader)
        setting = setting_dict['language']

    with open(rf'.\res\lang\{setting}', mode='r', encoding='utf-8') as file:
        lang_dict = json.load(file)

    return lang_dict, setting_dict


def change_language(language, new_lang):
    language["language"] = new_lang
    with open(r'.\res\setting', mode='w', encoding='utf-8') as file:
        yaml.dump(language, file, indent=2)
    os.system('cls')
    main()


def read_file():
    dictionary, language = read_lang_cfg()
    print(f'{dictionary["enterPath"]}\n'
          f'{dictionary["changeLang"]}\n'
          f'----------------------------------------')
    path = input('> ')
    if path in ('zh-cn', 'en'):
        change_language(language, path)
    if '"' in path:
        path = path[1:-1]
    return path, dictionary


def main():
    path, dictionary = read_file()
    is_exit = False
    os.system('cls')
    while not is_exit:
        is_exit, re_read_file = count.count(path, dictionary)
        if re_read_file:
            path = read_file()[0]
            os.system('cls')
    exit(0)


if __name__ == '__main__':
    os.system('cls')
    main()
