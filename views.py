from apps.bgtrack.models import GlucoseReading
from django.views.generic import View,TemplateView
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template import RequestContext
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.forms import ValidationError
from datetime import datetime

class CsrfView(View):
    def dispatch(self,*args,**kwargs):
        if len(args) > 0:
            request = args[0]
            self.context = RequestContext(request)
            self.context['request'] = request
        else:
            self.context = None
        return super(CsrfView,self).dispatch(*args,**kwargs)    

class CsrfTemplateView(CsrfView):        
    def render_to_response(self,context):
        return super(CsrfTemplateView,self).render_to_response(self.context if hasattr(self,'context') and self.context else context)

class ProtectedView(CsrfTemplateView):
    @method_decorator(login_required)
    def dispatch(self,*args,**kwargs):
        return super(ProtectedView,self).dispatch(*args,**kwargs)

class LoginView(TemplateView):
    """Login a user. Puts a form on the context."""
    template_name = "home.html"
    def get(self,request):
        """Creates a view for a user logging in"""    
        return login(request, template_name="home.html")

    def post(self,request):        
        return login(request, template_name="home.html")
        
class LogoutView(TemplateView):
    """Logout a user."""
    template_name = "home.html"
    def get(self,request):
        """Creates a view for a user who has logged out."""
        logout(request, template_name="home.html")
        return HttpResponseRedirect("/")
        
class RegisterView(TemplateView):
    template_name = "register.html"
        
    def post(self,request):
        from account_forms import RegisterForm
        from random import choice
        from string import letters
        data = request.POST.copy()
        # Generates a random user name
        data['username'] = ''.join([choice(letters) for i in xrange(30)])
        self.form = RegisterForm(data=data)
        if self.form.is_valid():
            new_user = self.form.save()
            return LoginView().post(request)
        return self.render_to_response(self.get_context_data())
    
    def get(self,request):
        if request.user.is_authenticated():
            return HttpResponseRedirect("/")
        from account_forms import RegisterForm
        self.form = RegisterForm()
        return super(RegisterView,self).get(request)
        
    def get_context_data(self,**kwargs):
        print kwargs
        return {'form' : self.form }   
        
class HomeView(CsrfView):
        
    def get(self,request):
        from apps.bgtrack.forms import ReadingForm
        if not request.user.is_authenticated():
            return LoginView().get(request)
        else:        
            self.context['reading_form'] = ReadingForm()
            add_home_variables(request,self.context)
            return render_to_response("home.html",context_instance=self.context)   

class RecordReadingView(ProtectedView):
    def post(self,request):
        print "POST"
        from apps.bgtrack.forms import ReadingForm
        from apps.bgtrack.shortcuts import record_reading,to_mgdl
        form = ReadingForm(request.POST)
        print request.POST
        if form.is_valid():
            reading,timestamp = float(form.cleaned_data['reading']),form.cleaned_data['timestamp']
            if request.POST['unit'] == "mmol/l":
                print "convert!"
                reading = to_mgdl(reading)
            else:
                reading = int(reading)
            try:
                record_reading(request.user,reading,timestamp)
            except ValidationError,e:
                raise e
            return HttpResponseRedirect("/")
        self.context['reading_form'] = form
        add_home_variables(request,self.context)
        return render_to_response("home.html",context_instance=self.context) 
    def get(self,request):
        return HttpResponseRedirect("/")            
        
def get_readings(request):                
    return list(GlucoseReading.objects.filter(user=request.user).order_by('timestamp'))

def add_home_variables(request,context):
    context['readings'] = get_readings(request)    
    context['now'] = datetime.now().strftime("%Y-%m-%d %H:%M")