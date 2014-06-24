from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
#from django.shortcuts import render
from clutter.models import Node, Item

# Create your views here.
def index(request):
    parents = [o.parent.id for o in Node.objects.all() if o.parent]
    leaves = [o.id for o in Node.objects.exclude(id__in=parents)]

    items = Item.objects.filter(node_id__isnull=False).exclude(node_id__in=leaves).order_by("?")

    if not items:
        items = Item.objects.filter(node__isnull=True).order_by("?")
        print("showing root item")
    
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
    if node.id in leaves:
        new_leaf = Node(parent=node)
        new_leaf.save()
        for i in Item.objects.filter(node=node):
            i.node = new_leaf
            i.save()
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

def merge(request, first_id, second_id):
    """
    Given two nodes, merge them.
    """
    first = Node.objects.get(id__exact=first_id)
    second = Node.objects.get(id__exact=second_id)
    new_node = Node(parent=first.parent)
    new_node.save()

    first.parent = new_node
    second.parent = new_node
    first.save()
    second.save()

    return HttpResponseRedirect(reverse('index'))

def cloud(request, node_id):
    """ 
    Given the url for a node return the image/tag cloud.
    """
    import json
    #from PIL import Image
    #from io import StringIO 
    from nltk.stem.snowball import SnowballStemmer
    from nltk.corpus import stopwords
    stemmer = SnowballStemmer("english")
    node = Node.objects.get(id__exact=node_id)
    words = node.get_items().strip().split()
    words = [w for w in words if not w in stopwords.words('english')]

    counts = {}
    for word in words:
        s = stemmer.stem(word)
        if s not in counts:
            counts[s] = 1
        else:
            counts[s] += 1

    #output = str(counts)
    #print(output)

    #o_image = StringIO()
    #img_grey = Image.new("L", (100,100))
    #img_grey.save(o_image, format="PNG")
    #contents = o_image.getvalue()
    #o_image.close()
    print(json.dumps(counts))

    return HttpResponse(json.dumps(counts), content_type="application/json")
