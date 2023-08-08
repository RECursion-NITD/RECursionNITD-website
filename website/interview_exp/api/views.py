from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mass_mail
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters import rest_framework as filters
from decouple import config
from .filters import ExperiencesFilter
from interview_exp.models import Experiences, Revisions
from user_profile.models import Profile
from user_profile.utils import ThreadedMailing
from user_profile.utils_permissions import ViewUpdatePermission, IsMemberOrAbove

from .serializers import (
    IESerializer,
    RevisionSerializer
)

# email only for trial purposes
# TRIAL_REC_MAIL = 'jiwegaw290@randrai.com'
TRIAL_REC_MAIL = settings.TRIAL_REC_MAIL


class IEListView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = IESerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = ExperiencesFilter
    search_fields = ['company', 'user__username', 'year']
    ordering_fields = ['updated_at', 'total_Compensation', 'year']

    def get_queryset(self):
        qs = Experiences.objects.all()
        user = self.request.user
        if user.profile.role == '3':
            return qs.filter(Q(user=user) | Q(verification_Status='Approved'))
        return qs

    def perform_create(self, serializer):
        # TODO
        # send thank you mail for posting
        user = self.request.user
        exp = serializer.save(user=user, verification_Status='Review Pending')

        ### mailing part

        # # region old mailing
        # profiles = Profile.objects.filter(~Q(role = '3'))
        # messages = ()
        # f=exp
        # for profile in profiles:
        #     user = profile.user
        #     current_site = get_current_site(self.request)
        #     subject = 'New Activity in Interview Experiences Section'
        #     message = render_to_string('new_experience_entry_email.html', {
        #         'user': user,
        #         'domain': current_site.domain,
        #         'experience': Experiences.objects.get(pk=f.id),
        #     })
        #     msg = (subject, message, 'webmaster@localhost', [TRIAL_REC_MAIL,])
        #     if msg not in messages:
        #         messages += (msg,)
        # result = send_mass_mail(messages, fail_silently=False)
        # # endregion

        # region new mailing
        member_users = User.objects.filter(~Q(profile__role='3'))
        domain = get_current_site(self.request).domain
        subject = 'New Activity in Interview Experiences Section'
        messages = [
            EmailMessage(
                subject,
                render_to_string(
                    'new_experience_entry_email.html',
                    {
                        'user': user,
                        'domain': domain,
                        'experience': exp,
                    }
                ),
                to=[TRIAL_REC_MAIL, ],

            )
            for user in member_users
        ]
        # uncomment below to mail
        threaded_mail = ThreadedMailing(messages, fail_silently=False, verbose=1)
        threaded_mail.start()
        # endregion


class RetrieveUpdateIEView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = IESerializer
    permission_classes = (ViewUpdatePermission,)
    lookup_field = 'id'
    lookup_url_kwarg = 'slug'

    def get_queryset(self):
        user = self.request.user
        qs = Experiences.objects.all()
        if user.profile.role == '3':
            return qs.filter(Q(user=user) | Q(verification_Status='Approved'))
        return qs

    def perform_update(self, serializer):
        exp = serializer.save()
        curr_status = exp.verification_Status
        emails = []
        if curr_status == 'Approved':
            exp.verification_Status = 'Review Pending'
        elif curr_status == 'Changes Requested':
            revision = Revisions.objects.filter(experience=exp)
            if revision.exists():
                revision = revision.first()
                reviewer = revision.reviewer
            else:  # send the mail to a random member/superuser(exceptional case that revision is not found)
                reviewer = Profile.objects.filter(~Q(role='3')).first()
            ## mailing part
            domain = get_current_site(self.request).domain
            subject = 'New Activity in Interview Experiences Section'
            messages = [
                EmailMessage(
                    subject,
                    render_to_string(
                        'update_experience_email.html',
                        {
                            'user': reviewer,
                            'domain': domain,
                            'experience': exp,
                        }
                    ),
                    to=[TRIAL_REC_MAIL, ],  # to=[reviewer.email, ]
                )
            ]
            # uncomment below to mail
            threaded_mail = ThreadedMailing(messages, fail_silently=True, verbose=1)
            threaded_mail.start()
        else:
            member_users = User.objects.filter(~Q(profile__role='3'))
            domain = get_current_site(self.request).domain
            subject = 'New Activity in Interview Experiences Section'
            messages = [
                EmailMessage(
                    subject,
                    render_to_string(
                        'update_Experience_to_all_email.html',
                        {
                            'user': user,
                            'domain': domain,
                            'experience': exp,
                        }
                    ),
                    to=[TRIAL_REC_MAIL, ],  # to=[reviewer.email, ]
                )
                for user in member_users
            ]
            # uncomment below to mail
            threaded_mail = ThreadedMailing(messages, fail_silently=True, verbose=1)
            threaded_mail.start()
        exp.save()


class RevisionsListView(ListAPIView):
    serializer_class = RevisionSerializer

    permission_classes = (IsMemberOrAbove,)

    def get_queryset(self):
        qs = Revisions.objects.prefetch_related('experience').prefetch_related('reviewer').all()
        return qs


class RetrieveUpdateRevisionView(RetrieveUpdateAPIView):
    serializer_class = RevisionSerializer
    permission_classes = (IsMemberOrAbove,)
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        qs = Revisions.objects.prefetch_related('experience').prefetch_related('reviewer').all()
        return qs


class CreateRevision(CreateAPIView):
    serializer_class = RevisionSerializer
    permission_classes = (IsMemberOrAbove,)

    def perform_create(self, serializer):
        """
        the review codes are:
        `acc` -> Accepted
        `rev` -> Review Pending
        `chg` -> Changes Requested
        """
        req = self.request
        curr_user = req.user
        exp_id = self.kwargs.get('exp_id')
        exp = get_object_or_404(Experiences, pk=exp_id)
        review_code = self.kwargs.get('review_code', '')
        print(self.kwargs)
        if review_code == 'acc':  # Accepted
            exp.verification_Status = 'Accepted'
            exp.verifier = curr_user
            # TODO
            # Send mail to the author about publication
            exp.save()
            revisions = Revisions.objects.filter(experience=exp)
            revisions.delete()
        else:
            msg = serializer.validated_data.get('message')

            if not msg:
                raise ValidationError('Must provide message if not being accepted.')
            domain = get_current_site(self.request).domain
            exp_author = exp.user
            subject = 'New Activity in Interview Experiences Section'
            messages = [
                EmailMessage(
                    subject,
                    render_to_string(
                        'changes_requested_email.html',
                        {
                            'user': exp.user,
                            'domain': domain,
                            'experience': exp,
                        }
                    ),
                    to=[TRIAL_REC_MAIL, ],  # exp.user.email

                )
            ]

            if review_code == 'rev':
                # doesn't make sense at all
                exp.verification_Status = 'Review Pending'
            elif review_code == 'chg':
                exp.verification_Status = 'Changes Requested'
                exp.save()
                revision, rev_created = Revisions.objects.get_or_create(experience=exp,
                                                                        defaults={'reviewer': curr_user,
                                                                                  'message': msg})
            else:
                raise ValidationError("Invalid code for verification status.")

            # uncomment below to mail
            threaded_mail = ThreadedMailing(messages, verbose=1)
            threaded_mail.start()
