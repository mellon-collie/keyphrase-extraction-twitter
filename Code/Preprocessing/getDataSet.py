import cPickle
from collections import Counter


def getTweetTags(filename):
    with open(filename) as f:
        datalist,taglist=[],[]
        for line in f:
            line=line.strip()
            datalist.append(line.split('\t')[0])
            taglist.append(line.split('\t')[1])    
    return datalist,taglist

def getDictionaries(filenames):
    trnTweet,testTweet=filenames
    sentence_list=getTweetTags(trnTweet)[0]+getTweetTags(testTweet)[0]
    words2idx=1,{}
    words=[]

    for sentence in sentence_list:
        word_list=sentence.split()
        words.extend(word_list)

    word_counts=Counter(words)
    words2idx={word[0]:i+1 for i,word in enumerate(word_counts.most_common())}

    labels2idx = {'O': 1, 'B': 2, 'I': 3, 'E': 4, 'S': 5}
    dicts = {'words2idx': words2idx, 'labels2idx': labels2idx}

    return dicts

def getIndices(sentenceList,tagList,words2idx,labels2idx):
    lex,y,z=[],[],[]
    bad_cnt=0
    for s,tag in zip(sentenceList,tagList):
        wordList=s.split()
        tList=tag.split()

        emb=map(lambda x:words2idx[x],wordList)
        begin=-1
        for i in range(len(wordList)):
            ok=True
            for j in range(len(tList)):
                if wordList[i+j]!=tList[j]:
                    ok=False;
                    break
            if ok==True:
                begin=i
                break

        if begin==-1:
            bad_cnt+=1
            continue

        lex.append(emb)

        labels_y=[1]*len(wordList)
        for i in range(len(tList)):
            labels_y[begin+i]=2
        y.append(labels_y)

        labels_z=[0]*len(wordList)
        if len(tList)==1:
            labels_z[begin]=labels2idx['S']
        elif len(tList)>1:
            labels_z[begin]=labels2idx['B']

            for i in range(len(tList)-2):
                labels_z[begin+i+1]=labels2idx['I']
            labels_z[begin+len(tList)-1]=labels2idx['E']

        z.append(labels_z)
    return lex,y,z


def getTrainingAndTestingDicts(filenames):
    trnTweetCnn, testTweetCnn= filenames
    dicts=getDictionaries([trnTweetCnn,testTweetCnn])

    trn_data=getTweetTags(trnTweetCnn)
    test_data=getTweetTags(testTweetCnn)

    trn_sentence_list,trn_tag_list=trn_data
    test_sentence_list,test_tag_list=test_data
    
    words2idx=dicts['words2idx']
    labels2idx=dicts['labels2idx']
    
    trainSentences, trainKeyword, trainKeyPhrase = getIndices(trn_sentence_list,trn_tag_list, words2idx,labels2idx)
    testSentences, testKeyword, testKeyPhrase = getIndices(test_sentence_list,test_tag_list,words2idx,labels2idx)
    train = [trainSentences, trainKeyword, trainKeyPhrase]
    test = [testSentences, testKeyword, testKeyPhrase]
    data_set = [train, test, dicts]
    with open('data_set8.pkl', 'w') as f:
        cPickle.dump(data_set, f)
    return data_set


if __name__ == '__main__':
    data_folder = ["original_data/trnTweet","original_data/testTweet"]
    data_set = getTrainingAndTestingDicts(data_folder)



      




        






















