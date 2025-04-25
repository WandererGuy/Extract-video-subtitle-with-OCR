

def split_into_n(lst, n):
    # base size for each of the first n-1 chunks
    size = len(lst) // n
    chunks = []
    for i in range(n - 1):
        chunks.append(lst[i*size : (i+1)*size])
    # last chunk takes all remaining elements
    chunks.append(lst[(n-1)*size :])
    return chunks

annotate_ls = [1,2,3,4,5,6,7,8,9,10]
chunks = split_into_n(annotate_ls, 3)
print (chunks)