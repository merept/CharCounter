import csv
import datetime
import json
import os
from xml.dom.minidom import Document

import pandas as pd
import yaml


def time_now():
    return datetime.datetime.now().strftime('%y%m%d%H%M%S')


def output_full_path(output_path):
    return os.path.abspath(output_path)


class Output:
    @property
    def file_name(self):
        name, ext = os.path.splitext(self.file_path)
        return name.split('\\')[-1].replace(' ', '_')

    @property
    def prefix(self):
        return 'cc' if self.is_analysis_char else 'cw'

    def __init__(self, file_path, is_analysis_char, dictionary):
        self.file_path = file_path
        self.is_analysis_char = is_analysis_char
        self.dictionary = dictionary

    def to_string(self, value, count):
        res = f'{self.dictionary["terFile"]}: {self.file_path}\n{self.dictionary["totalCount"]}: {count}\n'
        for v in value:
            if v[1] < 2:
                continue
            res += f'"{v[0]}":\n\t' \
                   f'{self.dictionary["count"]}: {v[1]}\n\t' \
                   f'{self.dictionary["per"]}: {round(v[1] / count, 4)}\n'
        return res

    def to_date_frame(self, value, count):
        index = []
        df_dict = {
            f'{self.dictionary["count"]}': [],
            f'{self.dictionary["per"]}': []
        }
        for v in value:
            index.append(v[0])
            df_dict[f'{self.dictionary["count"]}'].append(v[1])
            df_dict[f'{self.dictionary["per"]}'].append(round(v[1] / count, 4))
        index.append("总计")
        df = pd.DataFrame(df_dict, index=index)
        df.append()
        print(f'文件: {self.file_path}\n' + df)

    def to_csv(self, value, count):
        filename = rf'.\output\{self.prefix}_res_{self.file_name}.csv'
        csvfile = open(filename, mode='w', newline='', encoding='utf_8_sig')
        fieldnames = [f'{self.dictionary["char"]}', f'{self.dictionary["count"]}', f'{self.dictionary["per"]}']
        write = csv.DictWriter(csvfile, fieldnames=fieldnames)
        write.writeheader()
        for v in value:
            write.writerow({
                f'{self.dictionary["char"]}': v[0],
                f'{self.dictionary["count"]}': v[1],
                f'{self.dictionary["per"]}': round(v[1] / count, 4)
            })
        print(f'{self.dictionary["success"]} {output_full_path(filename)}\n')

    def to_json_yaml(self, value, count, is_yaml=False):
        filename = rf'.\output\{self.prefix}_res_{self.file_name}.{"yaml" if is_yaml else "json"}'
        result_dict = {
            "totalCount": count,
            "characterCount": []
        }
        for v in value:
            character_dict = {v[0]: {
                'times': v[1],
                'percentage': round(v[1] / count, 4)
            }}
            result_dict["characterCount"].append(character_dict)
        with open(filename, mode='w', encoding='utf-8') as file:
            if is_yaml:
                yaml.dump(result_dict, file, indent=2, allow_unicode=True)
            else:
                json.dump(result_dict, file, indent=2, ensure_ascii=False)

        print(f'{self.dictionary["success"]} {output_full_path(filename)}\n')

    def to_xml(self, value, count):
        filename = rf'.\output\{self.prefix}_res_{self.file_name}.xml'

        dom = Document()
        article = dom.createElement('Article')
        article.setAttribute('totalCount', f'{count}')
        dom.appendChild(article)

        for v in value:
            character = dom.createElement('Character')
            character.setAttribute('name', v[0])

            times = dom.createElement('Times')
            times_text = dom.createTextNode(f'{v[1]}')
            times.appendChild(times_text)

            percentage = dom.createElement('Percentage')
            percentage_text = dom.createTextNode(f'{round(v[1] / count, 4)}')
            percentage.appendChild(percentage_text)

            character.appendChild(times)
            character.appendChild(percentage)

            article.appendChild(character)

        with open(filename, mode='w', encoding='utf-8') as file:
            dom.writexml(file, indent='\t', newl='\n', addindent='\t')

        print(f'{self.dictionary["success"]} {output_full_path(filename)}\n')

    def to_xlsx(self, value, count):
        filename = rf'.\output\{self.prefix}_res_{self.file_name}.xlsx'
        df_dict = {
            f'{self.dictionary["char"]}': [],
            f'{self.dictionary["count"]}': [],
            f'{self.dictionary["per"]}': []
        }
        for v in value:
            df_dict[f'{self.dictionary["char"]}'].append(v[0])
            df_dict[f'{self.dictionary["count"]}'].append(v[1])
            df_dict[f'{self.dictionary["per"]}'].append(round(v[1] / count, 4))
        df = pd.DataFrame(df_dict)
        df.to_excel(filename, index=False)
        print(f'{self.dictionary["success"]} {output_full_path(filename)}\n')
