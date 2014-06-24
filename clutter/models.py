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
        if not Node.objects.filter(parent=self.id):
            output = ""
            for o in Item.objects.filter(node=self.id):
                output += str(o)
            return output

        output = ""
        for c in Node.objects.filter(parent=self.id):
            output += c.get_items()
        return output



