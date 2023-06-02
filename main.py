import os
import yaml
import json

from src import count


def read_lang_cfg():
    setting = ''
    with open(r'.\lang\setting', mode='r', encoding='utf-8') as file:
        setting_dict = yaml.load(file, yaml.FullLoader)
        setting = setting_dict['language']

    with open(rf'.\lang\{setting}', mode='r', encoding='utf-8') as file:
        lang_dict = json.load(file)

    return lang_dict, setting_dict


def change_language(language, new_lang):
    language["language"] = new_lang
    with open(r'.\lang\setting', mode='w', encoding='utf-8') as file:
        yaml.dump(language, file, indent=2)
    os.system('cls')
    main()


def main():
    dictionary, language = read_lang_cfg()
    print(f'{dictionary["enterPath"]}\n'
          f'{dictionary["changeLang"]}\n'
          f'----------------------------------------')
    path = input('> ')
    if path in ('zh-cn', 'en'):
        change_language(language, path)
    if '"' in path:
        path = path[1:-1]
    is_exit = False
    os.system('cls')
    while not is_exit:
        is_exit = count.count(path, dictionary)


if __name__ == '__main__':
    main()
