from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba


def wcl(path):
    text = open(path, 'rb').read()
    word_list = jieba.cut(text, cut_all=True)
    wl = ' '.join(word_list)

    wc = WordCloud(collocations=False,
                   font_path='msyh.ttc',
                   width=1400,
                   height=1400,
                   mask=None,  # 指定词云形状图片，默认为矩形
                   background_color='white',  # 背景颜色，默认黑色black
                   max_words=200,  # 最大词数，默认200
                   scale=5,  # 默认值1，值越大，图像密度越大越清晰
                   stopwords={},  # 不显示的单词
                   margin=2).generate(wl.lower())
    plt.imshow(wc)
    plt.axis('off')
    plt.show()
    wc.to_file('./data/WordCloud.png')


if __name__ == '__main__':
    path = './data/评价.txt'
    wcl(path=path)
