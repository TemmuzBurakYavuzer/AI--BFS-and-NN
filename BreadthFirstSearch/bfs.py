import queue

def getWay(prtNode, start, apple):
    way = [apple]
    while way[-1] != start:
        way.append(prtNode[str(way[-1])])
    way.reverse()
    return way

def BreathFirstSearch(size_x, size_y, b_size, visited, apple, start):
    choices = queue.Queue(maxsize = 0)
    choices.put(start)
    prtNode = {}
    while choices.empty() is False:
        look = choices.get()
        if look == apple: break
        elif look in visited: pass
        else:
            newCh = []
            newCh.append([look[0] + b_size, look[1]])
            newCh.append([look[0] - b_size, look[1]])
            newCh.append([look[0], look[1] + b_size])
            newCh.append([look[0], look[1] - b_size])
            visited.append(look)
            for i in newCh:
                if i[0] < 0 or i[1] < 0 or i[0] >= size_x or i[1] >= size_y or i in visited: pass
                else:
                    prtNode[str(i)] = look
                    choices.put(i)
    
    final_way = getWay(prtNode, start, apple)
    return final_way
