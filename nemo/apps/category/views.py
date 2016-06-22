from django.views.generic import TemplateView
from category.models import Category, SubCategory, Params


class CategoryView(TemplateView):

    template_name = 'category/list.html'

    def get(self, request):
        category = SubCategory.objects.all()
        return self.render_to_response({'categories': category})


class ItemView(TemplateView):

    template_name = 'category/item.html'

    def get(self, request, id):
        item = Params.objects.get(pk=id)
        return self.render_to_response({'item': item})


class SubCategoryView(TemplateView):

    template_name = 'category/sub_category_list.html'

    def get(self, request, id):

        category_lists = Params.objects.filter(subcategory_id=id)
        return self.render_to_response({'category_lists': category_lists})
