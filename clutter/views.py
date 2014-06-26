from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
#from django.shortcuts import render
from clutter.models import Node, Item

max_depth = 4

# Create your views here.
def index(request):
    parents = [o.parent.id for o in Node.objects.all() if o.parent]
    leaves = [o.id for o in Node.objects.exclude(id__in=parents)]

    # randomly pick non leave items
    items = Item.objects.exclude(node_id__in=leaves).order_by("?")

    # Force categorization of non root node items first.
    #items = Item.objects.filter(node_id__isnull=False).exclude(node_id__in=leaves).order_by("?")
    #if not items:
    #    items = Item.objects.filter(node__isnull=True).order_by("?")
    #    print("showing root item")
    
    if not items:
        item = None
        nodes = None
        template = loader.get_template('clutter/done.html')
        context = RequestContext(request, {})
        return HttpResponse(template.render(context))

    else:
        item = items[0]

        if item.node == None:
            nodes = Node.objects.filter(parent__isnull=True).order_by('-size',
                                                                     'text')
        else:
            nodes = Node.objects.filter(parent=item.node).order_by('-size',
                                                                   'text')

    template = loader.get_template('clutter/index.html')
    context = RequestContext(request, {'item': item, 'nodes': nodes,
                                       'remaining': len(items)})

    return HttpResponse(template.render(context))

def new(request, item_id):
    parents = [o.parent.id for o in Node.objects.all() if o.parent]
    leaves = [o.id for o in Node.objects.exclude(id__in=parents)]
    item = Item.objects.get(id__exact=item_id)

    if not item.node in leaves:
        node = Node()
        node.text = item.content
        node.size += 1
        if item.node:
            node.parent = item.node
        node.save()
        item.node = node
        item.save()

    return HttpResponseRedirect(reverse('index'))

def insert(request, item_id, node_id):
    """
    Given the item and the node, insert the item into the node.
    """
    parents = [o.parent.id for o in Node.objects.all() if o.parent]
    leaves = [o.id for o in Node.objects.exclude(id__in=parents)]
    item = Item.objects.get(id__exact=item_id)
    node = Node.objects.get(id__exact=node_id)

    if node and not item.node in leaves:
        if node.id in leaves or node.depth() >= max_depth:
            new_parent = Node(parent=node.parent)
            new_parent.text = node.text + " " + item.content
            new_parent.size = node.size + 1
            new_parent.save()
            node.parent = new_parent
            node.save()

            new_leaf = Node(parent=new_parent)
            new_leaf.text = item.content
            new_leaf.size += 1
            new_leaf.save()
            item.node = new_leaf
            item.save()
        else:
            item.node = node
            node.text = node.text + " " + item.content
            node.size += 1
            item.save()
            node.save()

    return HttpResponseRedirect(reverse('index'))

def split(request, node_id):
    """
    Given a node, split it and promote the children to the parent.
    """
    node = Node.objects.get(id__exact=node_id)

    if node:
        for c in Node.objects.filter(parent=node):
            c.parent = node.parent
            c.save()
        for i in Item.objects.filter(node=node):
            i.node = node.parent
            i.save()

        node.delete()

    return HttpResponseRedirect(reverse('index'))

def merge(request):
    """
    Given two nodes, merge them.
    """
    if request.GET.getlist('merge'):
        first = Node.objects.get(id__exact=request.GET.getlist('merge')[0])

        if first.parent and len(request.GET.getlist('merge')) == first.parent.num_children():
            return HttpResponseRedirect(reverse('index'))

        new_node = Node(parent=first.parent)
        new_node.save()
        #print(new_node.parent)
        
        for i in request.GET.getlist('merge'):
            node = Node.objects.get(id__exact=i)
            if node:
                node.parent = new_node
                node.save()
                new_node.text = new_node.text + " " + node.text
                new_node.size += node.size

        new_node.save()

    return HttpResponseRedirect(reverse('index'))

def cloud(request, node_id):
    """ 
    Given the url for a node return the image/tag cloud.
    """
    import json
    from nltk import regexp_tokenize
    from nltk.stem.snowball import SnowballStemmer
    #from nltk.corpus import stopwords
    
    stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
                 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him',
                 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it',
                 'its', 'itself', 'they', 'them', 'their', 'theirs',
                 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
                 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be',
                 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
                 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
                 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for',
                 'with', 'about', 'against', 'between', 'into', 'through',
                 'during', 'before', 'after', 'above', 'below', 'to', 'from',
                 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under',
                 'again', 'further', 'then', 'once', 'here', 'there', 'when',
                 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few',
                 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
                 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
                 'can', 'will', 'just', 'don', 'should', 'now']
    stemmer = SnowballStemmer("english")
    reverse_stem = {}

    node = Node.objects.get(id__exact=node_id)

    #words = regexp_tokenize(node.get_items().lower().strip(), r"[a-z]+")
    words = [w for w in regexp_tokenize(node.get_items().lower().strip(),
                                        r"[a-z]+") if not w in stopwords]

    counts = {}
    count = 0.0
    max_count = 1.0
    for word in words:
        #s = word
        s = stemmer.stem(word)
        if s in reverse_stem:
            s = reverse_stem[s]
        else:
            reverse_stem[s] = word
            s = word

        if s not in counts:
            counts[s] = 1
        else:
            counts[s] += 1
            if counts[s] > max_count:
                max_count = counts[s]
        count += 1

    #counts = {w:(1.0 * counts[w])/count for w in counts}
    counts = [{'word': w, 'frequency': 1.0 * counts[w] / count} for w in counts]
    #print(counts)

    return HttpResponse(json.dumps(counts), content_type="application/json")

def tree(request):
    """
    Return the entire tree in a JSON structure.
    """
    import json

    output = {}
    output['name'] = ""
    output['children'] = [c.get_tree_structure() for c in
                          Node.objects.filter(parent__isnull=True)]

    return HttpResponse(json.dumps(output), content_type="application/json")

def visualize(request):
    template = loader.get_template('clutter/visualize.html')
    context = RequestContext(request)

    return HttpResponse(template.render(context))
