from api import get_friends

import igraph


def get_network(users_ids, as_edgelist=True):
    edgelist = []
    matrix = [[0] * len(users_ids) for _ in users_ids]

    for i in range(len(users_ids)):
        friends = get_friends(users_ids[i], '')
        if friends is None:
            continue

        for j in range(i + 1, len(users_ids)):
            if users_ids[j] in friends:
                if as_edgelist:
                    edgelist.append((i, j))
                else:
                    matrix[i][j] = 1
                    matrix[j][i] = 1

    if as_edgelist:
        return edgelist
    return matrix


def plot_graph(graph, analysed_user_index):
    N = len(graph.vs)
    visual_style = dict()
    visual_style["layout"] = graph.layout_fruchterman_reingold(
        maxiter=1000,
        area=N ** 3,
        repulserad=N ** 3)

    visual_style['vertex_size'] = 17
    visual_style['vertex_label_size'] = 9
    visual_style['edge_width'] = 0.3

    graph.simplify(multiple=True, loops=True)
    communities = graph.community_edge_betweenness(directed=False)
    clusters = communities.as_clustering()
    graph.delete_vertices(analysed_user_index)

    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    graph.vs['color'] = pal.get_many(clusters.membership)
    igraph.plot(graph, **visual_style)


if __name__ == "__main__":
    analysed_user = 222620376

    friends = get_friends(analysed_user, 'first_name')
    friends_ids = [friends[i]['id'] for i in range(len(friends))]
    edgelist = get_network(friends_ids, as_edgelist=True)

    vertices = [i for i in range(len(friends_ids))]
    vertices.append(len(friends_ids))

    # с именами пользователей
    # vertices = [friends[i]['first_name'] + ' ' + friends[i]['last_name'] for i in range(len(friends))]
    # vertices.append('analysed user')

    edgelist.extend([(len(friends_ids), i) for i in range(len(friends_ids))])
    friends_graph = igraph.Graph(vertex_attrs={"label": vertices}, edges=edgelist, directed=False)
    plot_graph(friends_graph, len(friends_ids))
