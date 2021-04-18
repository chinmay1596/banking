from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.contrib import messages
from django.template.loader import render_to_string
from .utils import emailing
from .models import User, Transcations
from django.shortcuts import render, redirect
from .forms import RegistrationForm, TranscationForm, LoginForm, ExportForm
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login
from django.utils.crypto import get_random_string
from django.views.generic import View
import xlwt


class TranscationView(SuccessMessageMixin, View):
    form_class = TranscationForm
    template_name = 'banking/home.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_amount = form.cleaned_data['amount']
            transcation = form.cleaned_data['Transcation_type']

            if transcation == 'Deposit':
                queryset = Transcations.objects.filter(user=self.request.user)
                if not queryset:
                    Transcations.objects.create(user=self.request.user, amount=new_amount, balance=new_amount,
                                                Transcation_type=transcation)
                    messages.success(self.request, "Transcation successfull")
                else:
                    last_transcation = Transcations.objects.filter(user=self.request.user).last()
                    balance = last_transcation.balance
                    new_balance = balance + new_amount
                    Transcations.objects.create(user=self.request.user, amount=new_amount, balance=new_balance,
                                                Transcation_type=transcation)
                    messages.success(self.request, "Transcation successfull")

            elif transcation == 'Withdraw':
                queryset = Transcations.objects.filter(user=self.request.user)
                if not queryset:
                    messages.warning(self.request, "Not enough balance")
                else:
                    last_transcation = Transcations.objects.filter(user=self.request.user).last()
                    balance = last_transcation.balance
                    if new_amount > balance:
                        messages.warning(self.request, "Not enough balance")
                    else:
                        new_balance = balance - new_amount
                        Transcations.objects.create(user=self.request.user, amount=new_amount, balance=new_balance,
                                                    Transcation_type=transcation)
                        messages.success(self.request, "Transcation successfull")
            elif transcation == 'Enquiry':
                last_transcation = Transcations.objects.filter(user=self.request.user).last()
                messages.success(self.request, f'Available Balance {last_transcation.balance}')

            data = Transcations.objects.filter(user=self.request.user).last()

            context = {
                'user': self.request.user,
                'transcation_type': transcation,
                'amount': new_amount,
                'Available_balance': data.balance
            }
            email = self.request.user.email
            mail_subject = 'Transcation Information'
            message = render_to_string('banking/email.html', context)
            emailing.EmailThread(mail_subject, message, context, [email, ]).start()
            return redirect('home')
        return render(request, self.template_name, {'form': form})


class UserRegistrationView(CreateView):
    model = User
    template_name = 'banking/register.html'
    form_class = RegistrationForm

    def form_valid(self, form, *args, **kwargs):
        account_no = get_random_string(length=17, allowed_chars='1234567890')
        form.instance.account_no = account_no
        self.object = form.save()
        return redirect('login')
        return super(UserRegistrationView, self).form_valid(form)


class UserLoginView(CreateView):
    form_class = LoginForm
    template_name = 'banking/login.html'

    def form_valid(self, form, *args, **kwargs):
        user = authenticate(email=form.instance.email, password=form.instance.password)
        login(self.request, user)
        return redirect('home')
        return super().form_valid(form)


class ExportView(View):
    form_class = ExportForm
    template_name = 'banking/export.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Transcations.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Transcations')
            row_num = 0

            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            columns = ['user', 'first_name', 'last_name', 'amount', 'balance', 'Transcation_type', 'date']

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            font_style = xlwt.XFStyle()

            rows = Transcations.objects.filter(user=user, date__range=[start_date, end_date]).values_list('user__email',
                                                                                                          'user__first_name',
                                                                                                          'user__last_name',
                                                                                                          'amount',
                                                                                                          'balance',
                                                                                                          'Transcation_type',
                                                                                                          'date')
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, str(row[col_num]), font_style)

            wb.save(response)
            return response
        return render(request, self.template_name, {'form': form})
