from django.http import JsonResponse
from django.views.decorators.http import require_GET
from nltk.tree import Tree
from random import shuffle


@require_GET
def paraphrase(request):
    tree_str = request.GET.get('tree')
    limit = int(request.GET.get('limit', 20))

    # перевірка вхідних даних
    if not tree_str:
        return JsonResponse({'error': 'No tree provided'})
    if not 0 < limit <= 20:
        limit = 20

    tree_nltk = Tree.fromstring(tree_str)

    # повертає нове синтаксичне дерево з перефразуванням 'NP'
    def tree_paraphrase(tree):
        new_tree = tree.copy(deep=True)

        def children_shuffle(sub):
            # перемішування елементів з тегом 'NP' у субдереві включаючи розміщення ',' і 'СС'
            new_childrens = list(sub)
            nps = []
            nps_index = []
            for index, child in enumerate(new_childrens):
                if child.label() == 'NP':
                    nps.append(child)
                    nps_index.append(index)
            shuffle(nps)
            for index, shuffled_child in zip(nps_index, nps):
                new_childrens[index] = shuffled_child
            return new_childrens

        for pos in tree.treepositions():
            subtree = tree[pos]
            if isinstance(subtree, Tree) and subtree.label() == 'NP':
                # Перевірка, чи є дочірні елементи NP розділені комами або CC
                children = [child for child in subtree if isinstance(child, Tree)]
                if len(children) > 1 and any(',' in child.label() or 'CC' in child.label() for child in children) and \
                        any('NP' in child.label() for child in children):
                    # додання зміненого субдерева підпадаючого під умови
                    new_tree[pos] = Tree(new_tree[pos].label(), children_shuffle(subtree))

        return new_tree

    # створення json для відповіді
    response_data = {'paraphrases': [], }
    for _ in range(limit):
        response_data['paraphrases'].append({'tree': str(tree_paraphrase(tree_nltk))})

    return JsonResponse(response_data)
