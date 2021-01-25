from django.urls import reverse_lazy
from django.views import generic

from apps.task.models import Schema


class SchemasView(generic.ListView):
    template_name = 'schema/schemas.html'
    context_object_name = 'schemas'

    def get_queryset(self):
        if self.request.user.is_anonymous:
            queryset = Schema.objects.filter(user=None)
        else:
            queryset = Schema.objects.filter(user=self.request.user)
        return queryset


class SchemaUpdateView(generic.UpdateView):
    model = Schema
    template_name = 'schema/_update.html'
    fields = ['name']
    template_name_suffix = 'schema'
    success_url = reverse_lazy('schemas')


class SchemaCreateView(generic.CreateView):
    model = Schema
    template_name = 'schema/_create.html'
    fields = ['name']
    # template_name_suffix = 'schema'
    success_url = reverse_lazy('schemas')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super(SchemaCreateView, self).form_valid(form)


class SchemaDeleteView(generic.DeleteView):
    model = Schema
    template_name = 'schema/_delete.html'
    fields = ['name']
    template_name_suffix = 'schema'
    success_url = reverse_lazy('schemas')
