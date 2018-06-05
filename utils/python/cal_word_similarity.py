def find_lcs(S,T):
    """
    find the longest common substring
    """
    m = len(S)
    n = len(T)
    counter = [[0]*(n+1) for x in range(m+1)]
    longest = 0
    lcs_set = set()
    for i in range(m):
        for j in range(n):
            if S[i] == T[j]:
                c = counter[i][j] + 1
                counter[i+1][j+1] = c
                if c > longest:
                    lcs_set = set()
                    longest = c
                    lcs_set.add(S[i-c+1:i+1])
                elif c == longest:
                    lcs_set.add(S[i-c+1:i+1])
    return lcs_set

def cal_edit_distance(S, T):
    m = len(S)
    n = len(T)
    dp = [[0]*(n+1) for x in range(m+1)]
    for i in range(1, m+1):
        dp[i][0] = i
    for j in range(1, n+1):
        dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            if S[i-1] == T[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = min(dp[i-1][j-1] + 1, dp[i][j-1] + 1, dp[i-1][j] + 1)
    return dp[m][n]
    
def get_seg_emb(word_emb_dict, segs):
    """
    Args:
        word_emb_dict: dict, e.g. {"word": np.array(), }
        segs: list of string
    Return:
        seg_emb: np.array
    """
    emb_size = iter(word_emb_dict.values()).__next__().size
    seg_emb = np.zeros(emb_size, dtype=np.float32)
    print_str = ""
    for seg in segs:
        if seg in word_emb_dict:
            seg_emb += word_emb_dict[seg]
            print_str += "%s*|" %(seg)   # '*' means seg in word_emb_dict
        else:
            print_str += "%s|" %(seg)
    print("seg_emb: %s" % (print_str))
    return seg_emb

def cal_word_emb_cosine_similarity(word_emb_dict, word1, word2):
    """
    Args:
        word_emb_dict: dict, e.g. {"word": np.array(), }
        word1: string
        word2: string
    Returns:
        cosine_sim: float
    """
    import jieba
    seg1 = jieba.cut(word1)
    seg1_emb = get_seg_emb(word_emb_dict, seg1)
    seg2 = jieba.cut(word2)
    seg2_emb = get_seg_emb(word_emb_dict, seg2)
    cosine_sim = np.dot(seg1_emb, seg2_emb) / np.linalg.norm(seg1_emb) / np.linalg.norm(seg2_emb)
    return cosine_sim
