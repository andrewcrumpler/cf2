from django.shortcuts import render
from django.views import View

from .calculation import Calculation
from .forms import CalculatorForm


class IndexView(View):

    form_class = CalculatorForm
    template_name = "individual_cf/index.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(label_suffix="")
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, label_suffix="")
        context = {"form": form}
        if form.is_valid():
            context.update({"results": Calculation(form.cleaned_data)})
        return render(request, self.template_name, context)
