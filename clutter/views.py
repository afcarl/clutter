from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
#from django.shortcuts import render
from clutter.models import Node, Item

max_depth = 2 

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
            nodes = Node.objects.filter(parent__isnull=True).order_by("?")
        else:
            nodes = Node.objects.filter(parent=item.node).order_by("?")

    template = loader.get_template('clutter/index.html')
    context = RequestContext(request, {'item': item, 'nodes': nodes})

    return HttpResponse(template.render(context))

def new(request, item_id):
    item = Item.objects.get(id__exact=item_id)
    node = Node()
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
    if node.id in leaves or node.depth() >= max_depth:
        new_parent = Node(parent=node.parent)
        new_parent.save()
        node.parent = new_parent
        node.save()
        new_leaf = Node(parent=new_parent)
        new_leaf.save()
        item.node = new_leaf
        item.save()
    else:
        item.node = node
        item.save()

    return HttpResponseRedirect(reverse('index'))

def split(request, node_id):
    """
    Given a node, split it and promote the children to the parent.
    """

    node = Node.objects.get(id__exact=node_id)

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

        if len(request.GET.getlist('merge')) == first.parent.num_children():
            #print("MERGED ALL THE CHILDREN!?!?")
            return HttpResponseRedirect(reverse('index'))

        new_node = Node(parent=first.parent)
        new_node.save()
        
        for i in request.GET.getlist('merge'):
            node = Node.objects.get(id__exact=i)
            node.parent = new_node
            node.save()

    return HttpResponseRedirect(reverse('index'))

def cloud(request, node_id):
    """ 
    Given the url for a node return the image/tag cloud.
    """
    import json
    from nltk import regexp_tokenize
    #from nltk.stem.snowball import SnowballStemmer
    from nltk.corpus import stopwords
    #stemmer = SnowballStemmer("english")
    node = Node.objects.get(id__exact=node_id)
    words = regexp_tokenize(node.get_items().lower().strip(), r"[a-z]+")
    words = [w for w in words if not w in stopwords.words('english')]

    counts = {}
    count = 0.0
    max_count = 1.0
    for word in words:
        s = word
        #s = stemmer.stem(word)
        if s not in counts:
            counts[s] = 1
        else:
            counts[s] += 1
            if counts[s] > max_count:
                max_count = counts[s]
        count += 1

    counts = {w:(1.0 * counts[w])/count for w in counts}
    counts = [{'word': w, 'frequency': counts[w]} for w in counts]

    return HttpResponse(json.dumps(counts), content_type="application/json")
