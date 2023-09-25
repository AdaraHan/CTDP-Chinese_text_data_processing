"""author: Adara 2023/6/2
按照id值合并title
"""
import pandas as pd

input_file = 'compareResultList_final_0602.csv'
match_file = 'souyun_song.csv'
output_file = 'compareResultList_final_merge_title_0602.csv'


def main():
    df1 = pd.read_csv(input_file, encoding='UTF-8-SIG')
    df2 = pd.read_csv(match_file, encoding='UTF-8-SIG')

    # df3 = pd.concat([df1, df2], keys=['id_souyun'])
    df3 = pd.merge(df1, df2, how='left', on='id_souyun')
    df3.to_csv(output_file, index=False, encoding='UTF-8-SIG')
    print('Done!')


if __name__ == '__main__':
    main()
