from django.shortcuts import redirect


class PhoneVerifactionRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_phone_verified:
            return redirect('phone_verifaction')
        return super(PhoneVerifactionRequiredMixin, self).dispatch(request, *args, **kwargs)
