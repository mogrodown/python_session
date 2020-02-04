import CaboCha

parser = CaboCha.Parser('-n1')

def parse_sentence(sentence, begin):

    tree = parser.parse(sentence)

    offset = begin
    text = sentence

    for i in range(tree.chunk_size()):
        print('-' * 80)
        chunk = tree.chunk(i)
        chunk_begin = None

        print('chunk:')

        # token_posは、チャンク内の先頭のトークンが、文章全体として何番目のトークンかを格納している。
        for j in range(chunk.token_pos, chunk.token_pos + chunk.token_size):

            # トークンをツリーから取得
            token = tree.token(j)

            # そのトークンが文全体で「何文字目」に位置するか調べる
            token_begin = text.find(token.surface) + offset
            token_end = token_begin + len(token.surface)

            if chunk_begin is None:
                chunk_begin = token_begin

            # トークンの詳細
            fmt = token.feature.split(',')
            print('    token_begin : ', token_begin)
            print('    token_end : ', token_end)
            print('    TEXT : ', token.surface)
            print('    POS1 : ', fmt[0])
            print('    POS2 : ', fmt[1])

            text = text[token_end - offset:]
            offset = token_end


        '''
        # 係先チャンク
        if chunk.link != (-1):
            to_chunk = tree.chunk(chunk.link)
            print('係先')
            for j in range(to_chunk.token_pos, to_chunk.token_pos + to_chunk.token_size):
                token = tree.token(j)
                print(token.surface)
        '''
        
        chunk_end = token_end
        print('    chunk_link: ',   chunk.link)
        print('    chunk_begin: ',  chunk_begin)
        print('    chunk_end: ',    chunk_end)
        print('\n')
        


if __name__ == '__main__':
    # parse_sentence('2019年5月19日、イノナカミュージックの設立メンバーとして同日付でホロライブに加入', 0)

    parse_sentence('ロングヘアの時は 23歳', 0)
