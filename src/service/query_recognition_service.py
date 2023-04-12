import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import torch
from transformers import AutoTokenizer, AutoModel


tokenizer = AutoTokenizer.from_pretrained('sberbank-ai/sbert_large_nlu_ru')
model = AutoModel.from_pretrained('sberbank-ai/sbert_large_nlu_ru')

# В принципе неплохо справляется но не отслеживает варианты слов "задание" | "работа" | "лабораторная"  итд и сильно цепляется за них
# Можно использовать если забить в модели вручную все ети варианты, но... так делать плохо.
# tokenizer = AutoTokenizer.from_pretrained('DeepPavlov/rubert-base-cased')
# model = AutoModel.from_pretrained('DeepPavlov/rubert-base-cased')


class QueryService:
    queries = [
        'Моя работа принята?',

        # 'Какая разбалловка по дисциплине?',
        'Сколько баллов за семестр по предмету?',

        # 'Какие сроки по лабораторным?',
        # 'Какие сроки сдачи работ?',
        'Какие крайние сроки сдачи работ?',

        'Сколько у меня баллов?',

        'Какое у меня задание?',

        'Когда следующее занятие?',

        # 'Как зовут преподавателя?',
        'Как зовут преподавателя по ',

        'Какая сейчас неделя по счёту?',

        'Когда будет зачётная/контрольная неделя?',


        'gitlab аккаунт',
        'github аккаунт',

        'Какая почта',
    ]

    baseline = 0.47

    def __init__(self):
        tokens = self.__getTokens__(self.queries)
        embeddings = self.__getEmbeddings__(tokens)
        mask = self.__getMask__(tokens, embeddings)
        self.meanPooled = self.__meanPooling__(embeddings, mask)
        self.meanPooled = self.meanPooled.detach().numpy()

    def __getTokens__(self, queries):
        tokens = {'input_ids': [], 'attention_mask': []}

        for sentence in queries:
            newTokens = tokenizer.encode_plus(sentence, max_length=128, truncation=True,
                                              padding='max_length', return_tensors='pt')
            tokens['input_ids'].append(newTokens['input_ids'][0])
            tokens['attention_mask'].append(newTokens['attention_mask'][0])

        tokens['input_ids'] = torch.stack(tokens['input_ids'])
        tokens['attention_mask'] = torch.stack(tokens['attention_mask'])

        return tokens

    def __getEmbeddings__(self, tokens):
        outputs = model(**tokens)
        embeddings = outputs.last_hidden_state

        return embeddings

    def __getMask__(self, tokens, embeddings):
        attentionMask = tokens['attention_mask']
        mask = attentionMask.unsqueeze(-1).expand(embeddings.size()).float()

        return mask

    def __meanPooling__(self, embeddings, mask):
        maskedEmbeddings = embeddings * mask
        summed = torch.sum(maskedEmbeddings, 1)
        summedMask = torch.clamp(mask.sum(1), min=1e-9)
        meanPooled = summed / summedMask

        return meanPooled

    def evaluate(self, userQuery):
        tokens = self.__getTokens__([userQuery])
        embeddings = self.__getEmbeddings__(tokens)
        mask = self.__getMask__(tokens, embeddings)
        meanPooled = self.__meanPooling__(embeddings, mask)
        result = meanPooled.detach().numpy()

        similarity = cosine_similarity(
            result,
            self.meanPooled
        )
        similarity = similarity.flatten()

        if similarity.max() < self.baseline:
            return (
                f'Запрос не распознан! Максимальная оценка: {similarity.max()}',
                similarity.max()
            )

        idx_max = np.argmax(similarity)

        return self.queries[idx_max], similarity[idx_max]
