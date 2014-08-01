from django.db import models

max_depth = 2 
# Create your models here.

class Item(models.Model):
    content = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
    node = models.ForeignKey("Node", null=True, blank=True,
                             related_name="items")

    def __str__(self):
        if self.node:
            return str(self.content) + "(" +  str(self.node.id) + ")"
        else:
            return str(self.content) + "(" +  str(None) + ")"

class Node(models.Model):
    parent = models.ForeignKey("Node", null=True, blank=True,
                               related_name="children")
    text = models.TextField()
    size = models.IntegerField(default=0)

    def __str__(self):
        return self.children
        output = ""
        for i in self.items:
            output += i.__str__()

        return output

    def prune(self):
        for child in Node.objects.filter(parent=self):
            child.prune()

        if self.depth() >= max_depth:
            for child in Node.objects.filter(parent=self):
                for item in Item.objects.filter(node=child):
                    item.node = self
                    item.save()
                child.delete()
                

    def get_items(self):
        if self.text:
            return self.text

        if Item.objects.filter(node=self.id).count() > 0:
            return [Item.objects.filter(node=self.id).order_by('?')[0].image.url]
        else:
            return Node.objects.filter(parent=self.id).order_by('?')[0].get_items()
        #for o in Item.objects.filter(node=self.id):
        #    output.append(o.image.url)

        #for c in Node.objects.filter(parent=self.id):
        #    output += c.get_items()
            
        return output

    def depth(self):
        if self.parent:
            return 1 + self.parent.depth()
        else:
            return 1

    def num_children(self):
        return len(Node.objects.filter(parent=self))

    def get_tree_structure(self):
        output = {}
        output['name'] = ""
        output['children'] = [c.get_tree_structure() for c in Node.objects.filter(parent=self)]
        output['children'] += [{'name': i.content, 'image': i.image.url, 'size': 1} for i in
         Item.objects.filter(node=self)]

        return output
        


