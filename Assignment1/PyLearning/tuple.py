import collections


def named_tuple():
    Row = collections.namedtuple('Row', ['Locus', 'Total_Depth', 'Average_Depth_sample', 'Depth_for_17'])
    r = ['chr1:6484996', '1030', '1030', '1030']
    line = Row(r[0], *map(int, r[1:]))
    #Row(Locus='chr1:6484996', Total_Depth=1030, Average_Depth_sample=1030, Depth_for_17=1030)

    print(line.Total_Depth)


named_tuple()
