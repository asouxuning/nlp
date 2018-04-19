from collections import Counter, OrderedDict

words = []

with open('corpus/text8') as f:
  s = f.read()
  words = s.strip().lower().split()
  #bs = 4096
  #lw = '' # record the last word of every read block

  #while True:
  #  s = f.read(bs)
  #  if s == '':
  #    break
  #  s = lw + s
  #  ws = s.strip().lower().split()

  #  # 由于每个block的最后一个单词有被截断的可能,
  #  # 为了保持单词的完整性,将最后一个单词,
  #  # 与下一个block拼接进行统计,
  #  # 而不是在本次统计一个有可能残缺的单词
  #  lw = ws[-1]

  #  # 最后一个单词之前的所有单词加入词频统计
  #  c.update(ws[:-1])

  #  words += ws[:-1]
    

unknown_token = '<UNK>'
pad_token = '<PAD>'
max_df = 5

# 用二元组列表来统计记录词频
word_freq = [(unknown_token, -1), (pad_token, 0)]

c = Counter(words)
word_freq.extend(c.most_common()) 

# 最终的词典用OrderedDict来表示,
# 有序词典用来生成one hot独热词向量
word_freq = OrderedDict(word_freq)

# 词典word2idx记录每个单词的序号
# 序号0和序1被分配给了<UNK>和<PAD>
# 后续单词序号的分配则从2开始
word2idx = { unknown_token: 0, pad_token: 1 }
# 序号-单词的倒排表
idx2word = { 0: unknown_token, 1: pad_token }

# 单词序号的分配,从2开始
idx = 2
for w in word_freq:
  f = word_freq[w]
  if f >= max_df:
    word2idx[w] = idx
    idx2word[idx] = w
    idx += 1
  else:
    # map the rare word into the unkown token
    word2idx[w] = 0
    # increment the number of unknown tokens
    word_freq[unknown_token] += 1

# 把文本由单词转译成数字序号
data = [word2idx[w] for w in words]
# for reduce mem use
del words

vocabulary_size = len(word_freq)
most_common_words = list(word_freq.items())[:5]
print("Most common words (+UNK):", most_common_words)
print("Sample data:", data[:10], [idx2word[i] for i in data[:10]])
