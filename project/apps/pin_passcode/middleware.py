from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


class PinPasscodeMiddleware:
    def process_request(self, request):
        allowed_urls = (
            reverse('pin_form'),
            reverse('pin_auth'),
            reverse('admin:index')
        )
        if not request.user.is_authenticated() and request.path not in allowed_urls:
            return HttpResponseRedirect("%s?next=%s" % (reverse('pin_form'), request.path))
