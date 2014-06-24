from django.db import models

# Create your models here.

class Item(models.Model):
    content = models.CharField(max_length=200)
    node = models.ForeignKey("Node", null=True, blank=True,
                             related_name="items")

    def __str__(self):
        return str(self.content)

class Node(models.Model):
    parent = models.ForeignKey("Node", null=True, blank=True,
                               related_name="children")

    def __str__(self):
        return self.children
        output = ""
        for i in self.items:
            output += i.__str__()

        return output

    def get_items(self):
        output = ""
        for o in Item.objects.filter(node=self.id):
            output += str(o) + " "

        for c in Node.objects.filter(parent=self.id):
            output += c.get_items() + " "
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
        if not Node.objects.filter(parent=self):
            output['name'] = str(Item.objects.filter(node=self)[0])
            output['size'] = len(Item.objects.filter(node=self))
        else:
            output['name'] = ""
            output['children'] = [c.get_tree_structure() for c in Node.objects.filter(parent=self)]
            output['children'] += [{'name': i.content, 'size': 1} for i in
             Item.objects.filter(node=self)]
        return output
        


